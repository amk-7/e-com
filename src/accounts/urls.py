from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
]
