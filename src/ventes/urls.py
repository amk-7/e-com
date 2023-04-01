from django.urls import path
from . import views

app_name = "ventes"
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('articles/', views.articles, name='articles'),
    path('article/<int:id>/', views.details, name='article'),
    path('article/delete/<int:id>/', views.delete_article, name='article-delete'),
    path('categories/', views.categories, name='categories'),
    path('categorie/create', views.create_categorie, name='create-categorie'),
    path('categorie/delete/<int:id>', views.delete_categorie, name='delete-categorie'),
]


"""
Compte administrateur
- Avoir le nombre de client
- Avoir le nombre achat
- Voir le benéfice réalisé.
- Voir le nombre de visite.
- Voir le nombre de client qui ont acheté.
- VOir l'article le plus vendue.

- Voir la liste des clients
- Voir la liste des articles
- Voir la liste des postes
- Voir la liste des commands
- Voir la liste du personnel

"""