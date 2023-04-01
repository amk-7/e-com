
from .models import Shopper, Manager, SubCategorie, Article, Commande, ShopperPost
from postes.models import Post

def getStatistics():
    statistics = {
        'total_clients' : len(Shopper.objects.all()),
        'total_personnels' : len(Manager.objects.all()),
        'total_articles' : len(Article.objects.all()),
        'total_commands' : len(Commande.objects.all()),
        'sold' : sum([cmd.calculateTotalAmount() for cmd in Commande.objects.all()]),
        'benefice' : 0,
        'commande_paye' : len(Commande.objects.filter(isSold=True)),
        'commande_non_paye' : len(Commande.objects.filter(isSold=False)),
    }
    statistics['benefice'] = statistics['sold']-sum([cmd.calculateTotalAmountWithoutBenef() for cmd in Commande.objects.all()])
    return statistics

def getLikeNumberByPost(post: Post) -> int:
    return len(ShopperPost.objects.filter(post=post, like=True))

def validateArticle(input_data):
    input_error_value = {
        'designation': 'Veuillez saisir une désignation.', 
        'pricePurchase' : 'Veuillez saisir un nombre valide pour le prix d\'achat.', 
        'benefitPercentage': 'Veuillez saisir un pourcentage de bénefice valide.', 
        'stock': 'Veuillez saisir un nombre valide pour la quantité en stock.', 
        'sub_categorie': 'Veuillez sélectionner une sous catégorie.', 
        'description': 'Veuillez saisir une description.',
        'media': 'Veuillez selectionner une iamge',
        }
    errors = {}
    if not input_data['designation']:
        errors['designation'] = input_error_value['designation']
    
    if not input_data['description']:
        errors['description'] = input_error_value['description']
    
    if not input_data['media']:
        errors['media'] = input_error_value['media']

    if not input_data['pricePurchase']:
        errors['pricePurchase'] = input_error_value['pricePurchase']
    else:
        try:
            input_data['pricePurchase'] = float(input_data['pricePurchase'])
            if input_data['pricePurchase'] < 1 :
                raise ValueError
        except ValueError:
            input_data['pricePurchase'] = 0.0
            errors['pricePurchase'] = input_error_value['pricePurchase']

    if not input_data['benefitPercentage']:
        errors['benefitPercentage'] = input_error_value['benefitPercentage']
    else:
        try:
            input_data['benefitPercentage'] = float(input_data['benefitPercentage'])
            if input_data['benefitPercentage'] < 1  or input_data['benefitPercentage'] > 100:
                raise ValueError
        except ValueError:
            input_data['benefitPercentage'] = 0
            errors['benefitPercentage'] = input_error_value['benefitPercentage']


    return input_data, errors

def validateUser(input_data):
    input_error_value = {
        'first_name': 'Veuillez saisir un nom de famille.',
        'last_name': 'Veuillez saisir un prénom.',
        'username': 'Veuillez saisir un nom d\'utilisateur.',
        'username_already_exist': 'Ce nom d\'utilisateur est déjà pris',
        'email': 'Veuillez saisir une adresse e-mail valide.',
        'password': 'Veuillez saisir un mot de passe.',
        'confirm_password': 'Veuillez confirmer votre mot de passe.',
        'adresse': 'Veuillez saisir une adresse.',
        'contact': 'Veuillez saisir un numéro de contact.',
        'confirm_password_not_match': 'Vos mots passe ne correspondent pas',
        'user_already_exist' : 'Cet utilisateur exist déjà.',
        'town': 'Veuillez saisir une ville.',
        'neighborhood': 'Veuillez saisir un quartier.',
        'reference_place': 'Veuillez saisir un lieu reconnue.',
    }

    errors = {}
    
    if not input_data['first_name']:
        errors['first_name'] = input_error_value['first_name']
    
    if not input_data['last_name']:
        errors['last_name'] = input_error_value['last_name']
    
    if not input_data['username']:
        errors['username'] = input_error_value['username']
    
    if not input_data['email']:
        errors['email'] = input_error_value['email']
    else:
        # Utiliser une expression régulière pour vérifier si l'email est valide
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, input_data['email']):
            errors['email'] = input_error_value['email']
    
    if not input_data['password']:
        errors['password'] = input_error_value['password']
    
    if not input_data['confirm_password']:
        errors['confirm_password'] = input_error_value['confirm_password']

    elif input_data['password'] != input_data['confirm_password']:
        errors['confirm_password'] = 'Les mots de passe ne correspondent pas.'
    
    if not input_data['adresse']:
        errors['adresse'] = input_error_value['adresse']
    
    if not input_data['contact']:
        errors['contact'] = input_error_value['contact']
    
    if input_data['password'] and input_data['confirm_password']:
        if not (len(input_data['password']) > 7 and input_data['password'].strip() == input_data['confirm_password'].strip()):
            errors['confirm_password'] = input_error_value['confirm_password_not_match']

    if input_data['username'] and verifyIfUsermameAlreadyEsxit(input_data['username']):
        errors['username'] = input_error_value['username_already_exist']
    
    if input_data['email'] and input_data['contact']:
        if verifyIfUserAlreadyEsxit(input_data['email'], input_data['contact']):
            errors['user_already_exist'] = input_error_value['user_already_exist'] 
    if input_data['adresse']:
        print(input_data['adresse'])
        if len(input_data['adresse'])==3:
            if input_data['adresse'][0].strip() == '':
                errors['town'] = input_error_value['town']
            if input_data['adresse'][1].strip() == '':
                errors['neighborhood'] = input_error_value['neighborhood']
            if input_data['adresse'][2].strip() == '':
                errors['reference_place'] = input_error_value['reference_place']
        else:
            errors['town'] = input_error_value['town']
            errors['neighborhood'] = input_error_value['neighborhood']
            errors['reference_place'] = input_error_value['reference_place']
    
    return input_data, errors

def findShopper(user: object) -> Shopper:
    if user.is_authenticated:
        return Shopper.objects.filter(user=user)[0]
    return None

def findManager(user: object) -> Manager:
    if user.is_authenticated:
        return Manager.objects.filter(user=user)[0]
    return None

def verifyIfUserAlreadyEsxit(email, contact):
    # Verify then with email and contact
    shoppers = Shopper.objects.all()
    managers = Manager.objects.all()
    personnes = [shopper for shopper in shoppers] + [manager for manager in managers]
    for personne in personnes:
        if personne.user.email==email or personne.contact==contact:
            return True
    return False

def verifyIfUsermameAlreadyEsxit(username):
    shoppers = Shopper.objects.all()
    managers = Manager.objects.all()
    usernames = [shopper.user.username for shopper in shoppers] + [manager.user.username for manager in managers]
    return username in usernames

def verifyIfContactAlreadyEsxit(contact):
    shoppers = Shopper.objects.all()
    managers = Manager.objects.all()
    contacts = [shopper.contact for shopper in shoppers] + [manager.contact for manager in managers]
    return contact in contacts

def findKeyInArrayDictonnary(key, array):
    i=0
    for dictionnary in array:
        if key in dictionnary:
            return (True, i)
        i+=1
    return (False,-1)

def getAllKeyInArrayDictonnary(array):
    keys = []
    for dictionnary in array:
        keys.append(list(dictionnary.keys())[0])
    return keys

def formatCartList(articles, array):
    orders = []
    for article in articles:
        orders.append({
            'name' : article.designation,
            'thumbnail' : article.thumbnail.url,
            'price' : article.getSalePrice(),
            'categorie' : str(article.showSubCategorie())+" "+str(article.showSubCategorie()),
            'id': article.id,
            'quantity' : array[findKeyInArrayDictonnary(str(article.id), array)[1]][str(article.id)],
        })
    return orders