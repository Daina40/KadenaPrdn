from django.urls import path
from . import views

urlpatterns = [
    path('style_add/', views.style_info_add, name='style_info_add'),
    path('', views.add_style_overview, name='add_style_overview'),
    path('delete_add_style_overview/<int:id>/', views.delete_add_style_overview, name='delete_add_style_overview'),
    path('edit_add_style_overview/<int:id>/', views.edit_add_style_overview, name='edit_add_style_overview'),

    path('style/<int:style_id>/', views.style_detail, name='style_detail'),
    path('style/<int:style_id>/save_comments/', views.save_comments, name='save_comments'),
    path('style/<int:style_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('style/<int:style_id>/save/', views.save_style_info, name='save_style_info'),
    path('saved-table/', views.style_saved_table, name='style_saved_table'),
    path("style_saved_table_delete/<int:style_id>/", views.style_saved_table_delete, name="style_saved_table_delete"),
    path("style_saved_table_edit/<int:style_id>/", views.style_saved_table_edit, name="style_saved_table_edit"),
    
    path('upload-style-image/', views.upload_style_image, name='upload_style_image'),
    path('delete-style-image/<int:image_id>/', views.delete_style_image, name='delete_style_image'),
    
    path('style_view/<int:style_id>/', views.style_view, name='style_view'),

    path('download_style_excel/<int:style_id>/', views.download_style_excel, name='download_style_excel'),

]