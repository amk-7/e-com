from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate 
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, HttpResponse
from ventes.models import Shopper, Manager
from ventes import otherViews as ov
from django.contrib import messages

User = get_user_model()

def signup(request):
    data = {
        'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),
        'is_delivery' : Group.objects.filter(name="delivery")[0] in request.user.groups.all(),
        'is_shopper' : Group.objects.filter(name="shopper")[0] in request.user.groups.all(),
    }
    if request.method == "POST":
        if 'id' in request.POST and request.POST.get('id').strip() not in ['', 'None']:
            data['manager'] = get_object_or_404(Manager, pk=request.POST.get('id'))
        else :
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            confirm_password = request.POST.get('confirm_password')
            password = request.POST.get('password')
            adresse = request.POST.getlist('adresse[]')
            contact = request.POST.get('contact')
            
            input_data = {
                'first_name': first_name, 
                'last_name' : last_name, 
                'username': username, 
                'email': email, 
                'confirm_password': confirm_password, 
                'password': password,
                'adresse' : adresse,
                'contact': contact,
            }
            
            result = ov.validateUser(input_data)
            input_data = result[0]
            errors = result[1]
            if errors:
                for field, error in errors.items():
                    messages.error(request, error, extra_tags=field)
                
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                #print(adresse)
                #return HttpResponse(adresse)
                
                if request.user.is_authenticated:
                    manager = Manager(user=user, adresse=adresse, contact=contact)
                    data['personne'] = manager
                else:
                    shopper = Shopper(user=user, adresse=adresse, contact=contact)
                    data['personne'] = shopper
                
                return render(request, 'accounts/signup.html', context=data)

            #Verifier si le username exist déjà.
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            shopper, _ = Shopper.objects.get_or_create(contact=contact, adresse=adresse, user=user)
            #Vérifier si l'utilisateur à été bien créé.
            cart = request.session.get('cart')
            if cart!=None and len(cart) > 0:
                return redirect('ventes:purchase-cart')
            return redirect('ventes:index')
    data['operation'] = "create"
    return render(request, 'accounts/signup.html', context=data)

def login_user(request):
    if request.method == "POST":
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        shoppers = Shopper.objects.all()
        managers = Manager.objects.all()
        username = ""
        personnes = [shopper for shopper in shoppers] + [manager for manager in managers]
        for personne in personnes:
            if personne.contact==contact:
                username = personne.user.username
        print(username)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            cart = request.session.get('cart')
            if cart!=None and len(cart) > 0:
                return redirect('ventes:purchase-cart')
            return redirect('ventes:index')
        
        error = "Les identifiants de connection ne sont pas valide"
        field = "authentification_error"
        messages.error(request, error, extra_tags=field)
    return render(request, 'accounts/login.html', context={})

def logout_user(request):
    logout(request)
    return redirect('ventes:index')

def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    shopper = ov.findShopper(request.user)

    return HttpResponse(user)