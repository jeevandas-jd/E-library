from django.contrib import admin
from django.urls import path
from library_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Homepage URL
    path("materials/",views.study_materials,name="materials"),
    path('materials/<int:material_id>/', views.download_file, name='download_file'),
    path('upload_file/', views.upload_file, name='upload_file'),

]
