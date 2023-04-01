from django.urls import path
from . import views

app_name = "postes"
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.createPost, name='create'),
    path('liker/<int:id>', views.liker, name='liker'),
<<<<<<< HEAD:src/postes/urls.py
    path('delete/<int:id>', views.delete, name='delete'),
=======
    path('posteForm',views.post,name='post'),
>>>>>>> 5e6b98819a20c3fab602370bcd58bbe1d79cfc66:commerce_project/postes/urls.py
]
