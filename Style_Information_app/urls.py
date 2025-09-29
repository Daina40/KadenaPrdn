from django.urls import path
from . import views

urlpatterns = [
    path('style_summary/<int:id>/', views.style_summary, name='style_summary'),
    path('style/<int:style_id>/', views.style_detail, name='style_detail'),
    path('style_add/', views.style_info_add, name='style_info_add'),
    path('', views.add_style_overview, name='add_style_overview'),
    path('delete_add_style_overview/<int:id>/', views.delete_add_style_overview, name='delete_add_style_overview'),
    path('add_comments/', views.add_comments, name='add_comments'),
]
