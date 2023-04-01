from django.db import models
from accounts.models import Personne
from django.core.validators import MinValueValidator, MaxValueValidator
from .exception import ShopperNotFoundException, CommandeNoteFoundException, CommandeLineNoteFoundException
from postes.models import Post

class Manager(Personne):
    state = models.IntegerField(default=0, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    class Meta:
        verbose_name_plural = "Managers"
    def __str__(self):
        return super().__str__()
    
    def changeState(self):
        if self.state == 0:
            self.state = 1
        else :
            self.state = 0
        self.save()

    def isEnable(self):
        return self.state == 1
    
    def showState(self): 
        if self.state == 0 :
            return 'désactivé'
        return 'activé'

class Shopper(Personne):
    # Ajouter les attributs nécessaire au payements et à la livraison
    class Meta:
        verbose_name_plural = "Shoppers"
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
    def setArticleNote(self, article, note):
        shopperArticles, created = ShopperArticle.objects.get_or_create(article=article, shopper=self)
        shopperArticles.setNote(note)
        article.calculateNote()

    def likePost(self, post):
        shopper_poste, created = ShopperPost.objects.get_or_create(shopper=self, post=post)
        #print("Created::::: ", shopper_poste.liked)
        if created or shopper_poste.liked==False:
            shopper_poste.liked = True
            shopper_poste.post.incrementNbLike()
            shopper_poste.save()
        else:
            shopper_poste.liked = False
            shopper_poste.post.decrementNbLike()
            shopper_poste.save()
    
    def getCurrentCommande(self):
        commandes = Commande.objects.filter(shopper=self, state=-1)
        if commandes:
            return commandes[0]
        return 
    
    def deleteCommande(self):
        commandes = Commande.objects.filter(shopper=self, state=-1)
        if len(commandes) < 1:
            raise CommandeNoteFoundException
        commande = commandes[0]
        #Avant de supprimer on ramème ce qui avait avant.
        commande.delete()

    def addLineToCommande(self, _article, _quantity):
        # _ (c'est une convension) signifie que la variable "_" ne sera jamais utilisé
        commande, _ = Commande.objects.get_or_create(shopper=self, state=-1)
        line, created = CommandeBasket.objects.get_or_create(commande=commande, article=_article)
        line.setQuantity(_quantity)
            
    def changeCmdState(self):
        commandes = Commande.objects.filter(shopper=self, state=-1)
        if len(commandes) < 1:
            raise CommandeNoteFoundException
        commande = commandes[0]
        commande.setState(0)
        
     

class Categorie(models.Model):
    wording = models.CharField(max_length=128)
    def __str__(self):
        return self.wording

class SubCategorie(models.Model):
    wording = models.CharField(max_length=128)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    def __str__(self):
        return self.wording
        

class ShopperPost(models.Model):
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)

class Article(models.Model):
    designation = models.CharField(max_length=128, unique=True, default="")
    pricePurchase = models.FloatField(default=0.0)
    benefitPercentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock = models.IntegerField(default=0)
    reduction = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    note = models.FloatField(default=0.0, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    thumbnail = models.ImageField(upload_to="articles", blank=True, null=True)
    subcategorie = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.IntegerField(default=0, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.designation
    
    def changeState(self):
        if self.state == 0:
            self.state = 1
        else :
            self.state = 0
        self.save()

    def isEnable(self):
        return self.state == 1
    
    def showState(self): 
        if self.state == 0 :
            return 'désactivé'
        return 'activé'
    
    def getFakePrice(self):
        return self.price*0.3

    def getSalePrice(self):
        if self.pricePurchase!=0.0 or self.benefitPercentage!=0:
            return self.pricePurchase + (self.pricePurchase*self.benefitPercentage/100)
        return 0
    
    def showSubCategorie(self):
        if self.subcategorie:
            return self.subcategorie
        return "Aucune"
    
    def showCategorie(self):
        if self.subcategorie:
            return self.subcategorie.categorie
        return "Aucune"
    
    def augmentQuantity(self, _quantity):
        if _quantity >= 0:
            self.stock += _quantity
        else:
            raise ValueError
        self.save()

    def diminueQuantity(self, _quantity):
        if _quantity >= 0:
            self.stock -= _quantity
        else:
            raise ValueError
        self.save()

    def calculateNote(self):
        shopperArticles = ShopperArticle.objects.filter(article=self)
        mean = 0
        for shopperArticle in shopperArticles:
            mean += shopperArticle.note
        self.note = mean/len(shopperArticles)
        self.save()

    
"""
class Supply(models.Model):
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.manager.username}({self.date})"

class SupplyBasket(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.article.designation}({self.quantity})"
"""

class ShopperArticle(models.Model):
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    note = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def setNote(self, note):
        self.note = note
        self.save()

class Commande(models.Model):
    shopper = models.ForeignKey(Shopper, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, blank=True)
     # 1 : client reçoit cmd. 0 : cmd en cours de livraisons. -1 : cmd créer
    state = models.IntegerField(default=-1, validators=[MinValueValidator(-1), MaxValueValidator(1)]) 
    isSold = models.BooleanField(default=False, null=True)
    delivery = models.ForeignKey(Manager, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.shopper.user.username}({self.date})"
    
    def showDate(self):
        return self.date.strftime("%A %d %B %Y %H:%M")
    
    def modifieIsSoldValue(self, _sold):
        self.isSold = _sold
        self.save()
    
    def setIsSold(self):
        commande_lines = CommandeBasket.objects.filter(commande=self)
        nomber_commande_line = len(commande_lines) 
        nomber_is_sign = 0
        for line in commande_lines:
            if line.signed:
                nomber_is_sign += 1

        self.isSold = (nomber_commande_line == nomber_is_sign)
        if self.isSold:
            self.state = 1
        
        self.save()
    
    def showIsSold(self):
        self.setIsSold()
        if self.isSold:
            return "oui"
        return "non"
    
    def setState(self, state):
        self.state = state 
        self.save()
    
    def showStat(self):
        if self.state == -1:
            return "En création"
        if self.state == 0:
            return "En cours"
        return "Réception"
    
    def calculateTotalAmount(self):
        amount = 0
        commande_lines = CommandeBasket.objects.filter(commande=self)
        for line in commande_lines:
            amount += line.calculateAmount()
        return amount
    
    def calculateTotalAmountWithoutBenef(self):
        amount = 0
        commande_lines = CommandeBasket.objects.filter(commande=self)
        for line in commande_lines:
            amount += line.calculateAmountWithoutBenef()
        return amount
    
    def delete(self):
        commande_lines = CommandeBasket.objects.filter(commande=self)
        for line in commande_lines:
            line.article.augmentQuantity(line.quantity)
        super().delete()

class CommandeBasket(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    signed = models.IntegerField(default=0, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])

    """def delete(self):
        self.article.augmentQuantity(self.quantity)
        super().delete()"""
   
    def __str__(self):
        return f"{self.article.designation}({self.quantity})"

    def sign(self):
        if self.signed == 0:
            self.signed = 1
            self.save()
    
    def calculateAmount(self):
        return self.quantity*self.article.getSalePrice()
    
    def calculateAmountWithoutBenef(self):
        return self.quantity*self.article.pricePurchase 

    def setQuantity(self, _quantity):
        self.quantity = _quantity
        try:
            self.article.diminueQuantity(_quantity)
        except ValueError as ve:
            raise ve
        self.save()

    def updateQuantity(self,_quantity):
        setValue = _quantity - self.quantity
        self.quantity += setValue
        try:
            if setValue > 0:
                self.article.diminueQuantity(setValue)
            else:
                self.article.diminueQuantity(setValue*-1)
        except ValueError as ve:
            print("##########################")
        self.save()
       
