"""
1.  Develop a Django App which be able to import CSV files containing grower
    details then produce a report showing growers per district. The format of
    the CSV file as as follows:

        GrowerName,National_ID,MobileNo,District, Province

    The app should allow a user to capture Provinces and Districts before
    uploading CSV files. Use at least Django 2.0 and Python3. This App should
    also automatically generate a GrowerNumber.

2.  Using the App developed in Task 1, integrate this App with Bulk SMS. You
    can use the code available from
    http://portal.bulksmsweb.com/sample/samplepy.html as a starting point for
    BulkSMS integration. This integration should allow the App to send SMS to
    every grower in the CSV informing them of their grower number.
"""


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Province, District
from .forms import ProvinceForm, DistrictForm, FileForm
from .utils import check_record_size, check_data_integrity


@login_required
def index(request):
    return render(request, 'growers/index.html')


@login_required
def provinces_admin(request):
    provinces = Province.objects.all()
    return render(request, 'growers/provinces_admin.html',
                 {'provinces': provinces})


@login_required
def province_create(request):
    if request.method == "POST":
        form = ProvinceForm(request.POST)
        if form.is_valid():
            province = form.save(commit=False)
            province.save()
            return redirect('province-admin-view', id=province.id)
    else:
        form = ProvinceForm()
    return render(request, 'growers/province_create.html', {'form': form})


@login_required
def province_admin_view(request, id):
    province = get_object_or_404(Province, id=id)
    districts = District.objects.filter(province=province)
    return render(request, 'growers/province_admin_view.html',
                 {'province': province, 'districts': districts})


@login_required
def province_admin_edit(request, id):
    province = get_object_or_404(Province, id=id)
    if request.method == "POST":
        form = ProvinceForm(request.POST, instance=province)
        if form.is_valid():
            province = form.save(commit=False)
            province.save()
            return redirect('province-admin-view', id=province.id)
    else:
        form = ProvinceForm(instance=province)
    return render(request, 'growers/province_admin_edit.html', {'form': form,
                        'province': province})


@login_required
def district_create(request):
    if request.method == "POST":
        form = DistrictForm(request.POST)
        if form.is_valid():
            district = form.save(commit=False)
            district.save()
            return redirect('province-admin-view', id=district.province.id)
    else:
        form = DistrictForm()
    return render(request, 'growers/district_create.html', {'form': form})


@login_required
def district_edit(request, id):
    district = get_object_or_404(District, id=id)
    if request.method == "POST":
        form = DistrictForm(request.POST, instance=district)
        if form.is_valid():
            province = form.save(commit=False)
            province.save()
            return redirect('province-admin-view', id=district.province.id)
    else:
        form = DistrictForm(instance=district)
    return render(request, 'growers/district_edit.html', {'form': form,
                        'district': district})


@login_required
def upload_records(request):
    errors = []
    records = []
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            records, errors = check_record_size(request.FILES['upload'])

            records, errors, provinces = check_data_integrity(records, errors)

            errors = check_duplicate_id_numbers(records, errors)

            messages.success(request, 'File has been uploaded')
    else:
        form = FileForm()
    return render(request, 'growers/upload_records.html', {'form': form,
                        'errors': errors, 'records': records})


