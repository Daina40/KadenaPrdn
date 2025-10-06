from django.urls import path
from . import views

urlpatterns = [
    path('style_add/', views.style_info_add, name='style_info_add'),
    path('', views.add_style_overview, name='add_style_overview'),
    path('delete_add_style_overview/<int:id>/', views.delete_add_style_overview, name='delete_add_style_overview'),
    
    path('style/<int:style_id>/', views.style_detail, name='style_detail'),
    path('style/<int:style_id>/save_comments/', views.save_comments, name='save_comments'),
    path('style/<int:style_id>/save/', views.save_style_info, name='save_style_info'),
    path('saved-table/', views.style_saved_table, name='style_saved_table'),
]
