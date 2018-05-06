from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('provinces-admin/', views.provinces_admin, name='provinces-admin'),
    path('province-create/', views.province_create, name='province-create'),
    path('district-create/', views.district_create, name='district-create'),
    path('province-admin-view/<int:id>/', views.province_admin_view,
             name='province-admin-view'),
    path('province-admin-edit/<int:id>/', views.province_admin_edit,
             name='province-admin-edit'),
    path('district-edit/<int:id>/', views.district_edit,
             name='district-edit'),
    path('upload-records/', views.upload_records, name='upload-records'),
    path('sms-balance/', views.sms_balance, name='sms-balance'),
]