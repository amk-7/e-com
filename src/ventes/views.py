from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ventes.models import Article, Categorie
from django.shortcuts import get_object_or_404
from . import otherViews as ov
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage

LOGIN_URL = '/accounts/login'

@login_required(redirect_field_name=LOGIN_URL)
def dashboard(request):
    data = {
        'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),
        'is_delivery' : Group.objects.filter(name="delivery")[0] in request.user.groups.all(),
        'is_shopper' : Group.objects.filter(name="shopper")[0] in request.user.groups.all(),
        'statistics' : ov.getStatistics(),
        }
    return render(request, "welcome.html", context=data)

def index(request):
    data = {
        'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),
        'is_delivery' : Group.objects.filter(name="delivery")[0] in request.user.groups.all(),
        'is_shopper' : Group.objects.filter(name="shopper")[0] in request.user.groups.all(),
        'categories': Categorie.objects.all(),
        'phone_number' : '+228 93561240'
        }
    data['articles'] = Article.objects.all()
    
    if request.method == 'POST':
        designation = request.POST.get('search')
        categorie_id = request.POST.get('categorie')
        if categorie_id:
            categorie = get_object_or_404(Categorie, pk=categorie_id)
            data['articles'] = Article.objects.filter(subcategorie=categorie).filter(designation__icontains=designation)
        else:
            categorie = None
            data['articles'] = Article.objects.filter(designation__icontains=designation)

    return render(request, 'store/index.html', context=data)

@login_required(redirect_field_name=LOGIN_URL)
def articles(request):
    data = {
        'categories' : Categorie.objects.all(),
        'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),
        'is_delivery' : Group.objects.filter(name="delivery")[0] in request.user.groups.all(),
        'is_shopper' : Group.objects.filter(name="shopper")[0] in request.user.groups.all(),
        }
    if request.method=="POST": 
        designation = request.POST.get('designation')
        pricePurchase = request.POST.get('pricePurchase')
        benefitPercentage = request.POST.get('benefitPercentage')
        stock = request.POST.get('stock')
        sub_categorie_id = request.POST.get('categorie')
        description = request.POST.get('description')

        url = ""
        if 'media' in request.FILES:
            image_file = request.FILES['media']
            fs = FileSystemStorage()
            filename = fs.save("articles/"+image_file.name, image_file)
            url = fs.url(filename)
        
        input_data = {
            'designation': designation, 
            'pricePurchase' : pricePurchase, 
            'benefitPercentage': benefitPercentage, 
            'stock': stock, 
            'sub_categorie_id': sub_categorie_id, 
            'description': description,
            'media' : url,
        }

        if "id" in request.POST and request.POST['id'] != '':
            _article = get_object_or_404(Article, pk=request.GET.get('id'))
            if url=="":
                input_data['media'] = _article.thumbnail.url
            result = ov.validateArticle(input_data)
            input_data = result[0]
            errors = result[1]
            if errors:
                for field, error in errors.items():
                    messages.error(request, error, extra_tags=field)
                
                article = Article()
                article.id = request.POST.get('id')
                article.designation = input_data['designation']
                article.pricePurchase = input_data['pricePurchase']
                article.benefitPercentage = input_data['benefitPercentage']
                article.description = input_data['description']
                article.thumbnail = _article.thumbnail
                data['article'] = article
                data['categorie'] = _article.subcategorie
                return render(request, 'store/create_article.html', context=data)
            
            id = request.POST.get('id')
            article = get_object_or_404(Article, pk=id)
            article.designation = input_data['designation']
            article.pricePurchase = input_data['pricePurchase']
            article.benefitPercentage = input_data['benefitPercentage']
            article.description = input_data['description']
            if url!="":
                article.thumbnail = url[6:len(url)]
            article.save()

        else :
    
            result = ov.validateArticle(input_data)
            input_data = result[0]
            errors = result[1]
            if errors:
                #print("\n", errors, "\n")
                for field, error in errors.items():
                    messages.error(request, error, extra_tags=field)
                if url == "":
                    fs = FileSystemStorage()
                    url = fs.url('default.png')
                article = Article()
                article.id = ""
                article.designation = input_data['designation']
                article.pricePurchase = input_data['pricePurchase']
                article.benefitPercentage = input_data['benefitPercentage']
                article.stock = input_data['stock']
                article.description = input_data['description']
                article.thumbnail = url
                data['article'] = article
                return render(request, 'store/create_article.html', context=data)
            print(sub_categorie_id)
            categorie = get_object_or_404(Categorie, pk=sub_categorie_id) 
            article = Article(
                designation=designation,
                pricePurchase=float(pricePurchase),
                benefitPercentage=benefitPercentage,
                stock=stock,
                subcategorie=categorie,
                thumbnail=url[6:len(url)],
                description=description,
            )
            article.save()
        return redirect('ventes:index')
    
    if 'id' in request.GET:
        data['article'] = get_object_or_404(Article, pk=request.GET.get('id'))
    
    return render(request, 'store/create_article.html', context=data)    

@login_required(redirect_field_name=LOGIN_URL)
def delete_article(request, id):
    article = get_object_or_404(Article, pk=id)
    article.delete()
    return redirect('ventes:index')

def details(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'store/details.html', context={'article' : article})

@login_required(redirect_field_name=LOGIN_URL)
def create_categorie(request):
    if request.method == "POST":
        wording = request.POST.get("wording")
        if 'id' in request.POST and request.POST.get('id') != '':
            categorie = get_object_or_404(Categorie, pk=request.POST.get('id'))
            categorie.wording = wording
            categorie.save()
            return JsonResponse({"result": wording, "id": categorie.id})
        categorie = Categorie(wording=wording)
        categorie.save()
        return redirect('ventes:categories')

@login_required(redirect_field_name=LOGIN_URL)       
def categories(request):
    data = {
        'categories': Categorie.objects.all(),
        'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),
        'is_delivery' : Group.objects.filter(name="delivery")[0] in request.user.groups.all(),
        'is_shopper' : Group.objects.filter(name="shopper")[0] in request.user.groups.all(),
        }
    return render(request, 'store/categories.html', data)

@login_required(redirect_field_name=LOGIN_URL)
def delete_categorie(request, id):
    categorie = get_object_or_404(Categorie, pk=id)
    categorie.delete()
    return redirect('ventes:categories')
