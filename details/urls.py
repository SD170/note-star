from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('college-details/', views.college_details, name='college_details'),
    path('new-note-create/', views.new_note_create, name='new_note_create'),
    path('file-upload-form/', views.file_upload_form, name='file_upload_form'),
    path('file-upload/', views.file_upload, name='file_upload'),
    path('search-note-1/', views.search_note_1, name='search_note_1'),
    path('search-note-2/', views.search_note_2, name='search_note_2'),
    path('search-note-3/', views.search_note_3, name='search_note_3'),
    path('search-note-4/', views.search_note_4, name='search_note_4'),
    path('part-result/', views.part_result, name='part_result'),
    path('user-notes/<str:pk>/', views.user_notes, name='user_notes'),
]