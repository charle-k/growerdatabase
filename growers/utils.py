from .models import Grower, District, Province


def check_record_size(f):
    errors = []
    contents = f.read().splitlines()
    cleaned_records = []
    count = 0
    for l in contents:
        count += 1
        fields = str(l).split(',')
        t = 0
        while t < len(fields):
            fields[t] = fields[t].strip().title()
            t += 1

        fields = list([_f for _f in fields if _f])
        if len(fields) == 5:
            fields[2] = fields[2].upper()
            fields[3] = fields[3].title()
            fields[4] = fields[4].title()
            fields.insert(0, count)
            cleaned_records.append(fields)
        else:
            errors.append([count,
             'Line does not have the requisite number of fields'])

    return (
     cleaned_records, errors)


def check_data_integrity(records, errors):
    districts = get_districts()
    cleaned_records = []
    for p in records:
        print(p)

    for rec in records:
        is_clean = True
        if len(rec[1]) > 200:
            is_clean = False
            errors.append([rec[0],
             'The name is too long'])
        z, rec[2] = check_id_number(rec[2])
        if not z:
            is_clean = False
            errors.append([rec[0],
             'The ID Number is invalid'])
        z, rec[2] = check_mobile_number(rec[2])
        if not z:
            is_clean = False
            errors.append([rec[0],
             'Please check cellphone number'])
        dkey = rec[3] + rec[4]
        if dkey not in list(districts.keys()):
            errors.append([rec[0],
         'Check Province, District name, and if district is in that Province'])
            is_clean = False

        if is_clean:
            cleaned_records.append(rec)
    return  cleaned_records, errors, districts


def check_id_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in (' ', '-'):
            r += p

    n = r
    r = ''
    for p in n:
        if p not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
            is_clean = False
        else:
            r += p

    n = r
    if len(r) == 11:
        if r[8] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            is_clean = False
        r = r[0:8] + r[9:12]
        for p in r:
            if p not in '1234567890':
                is_clean = False

    else:
        is_clean = False
    return (
     is_clean, n)


def get_districts():
    districts = District.objects.all()
    places = dict()
    for d in districts:
        dkey = d.name + d.province.name
        places[dkey] = d

    return places


def check_mobile_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in (' ', '+'):
            r += p

    n = r
    r = ''
    for p in n:
        if p not in '1234567890':
            is_clean = False
        else:
            r += p

    n = r.lstrip('0')
    if n.find('263') != 0:
        n = '263' + n
    if len(n) == 12:
        if n[0:5] not in ('26377', '26371', '26373'):
            is_clean = False
    else:
        is_clean = False
    return (
     is_clean, n)


def check_duplicate_id_numbers(records, errors):
    return errors