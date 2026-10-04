from django.contrib import admin
from django.urls import path
from . import views
from . views import contact_list ,contact_create,contact_edit,contact_delete 
urlpatterns  = [
    path('admin/', admin.site.urls),
    path('', contact_list, name='contact_list'),
    path('add/', contact_create, name='contact_create'),
    path('edit/<int:id>/', contact_edit, name='contact_edit'),
    path('delete/<int:id>/', contact_delete, name='contact_delete'),
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/add', views.deal_create, name='deal_create'),
    path('deals/edit/<int:id>/', views.deal_edit, name='deal_edit'),
    path('deals/delete/<int:id>/', views.deal_delete, name='deal_delete'),
    path(
    'deals/update-stage/<int:id>/<str:stage>/',
    views.update_deal_stage,
    name='update_deal_stage'),
    path('deals/ai-email/<int:id>/', views.ai_email, name='ai_email'),
]