from django.contrib import admin
from ventes.models import Manager, Shopper, Article, Categorie, SubCategorie, Commande, CommandeBasket, ShopperArticle, ShopperPost

admin.site.register(Categorie)
admin.site.register(Manager)
admin.site.register(Shopper)
admin.site.register(Article)
admin.site.register(Commande)
admin.site.register(SubCategorie)
admin.site.register(CommandeBasket)
admin.site.register(ShopperArticle)
admin.site.register(ShopperPost)