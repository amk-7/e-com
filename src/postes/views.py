from django.shortcuts import render, get_object_or_404, redirect
from postes.models import Post
from django.urls import reverse
from django.http import JsonResponse
from ventes import otherViews as ov
from django.db.models import Max
from django.contrib.auth.models import Group

def index(request):
    postes = Post.objects.all().order_by('-id')
    return render(request, 'postes/index.html', context={'postes':postes, 'is_manager' : Group.objects.filter(name="manager")[0] in request.user.groups.all(),})

def createPost(request):
    data = {'post' : ""}
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        media = request.FILES
        description = request.POST.get('description')
        print(media)
        if id :
            post = get_object_or_404(Post, pk=id)
            post.name = title
            post.description = description
            if 'media' in media:
                post.media = media.get('media')
            post.save()
        else:
            post = Post.objects.create(name=title, description=description, media=media.get('media'))

        return redirect('postes:index')

    if 'id' in request.GET:
        data['post'] = get_object_or_404(Post, pk=request.GET.get('id'))
    return render(request, 'postes/create.html', context=data)

def liker(request, id):
    post = get_object_or_404(Post, pk=id)
    shopper = ov.findShopper(request.user)
    if shopper:
        shopper.likePost(post)
        return JsonResponse({"result" : post.loveNumber==0})
    #return JsonResponse({"result" : False})

def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('postes:index')