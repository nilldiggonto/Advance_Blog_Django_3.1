from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DeleteView
# Create your views here.

################################## Function Based ###################################
def post_list(request):
    
    object_list = Post.published.all()
    template_name = 'post/list.html'
    paginator = Paginator(object_list,2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'page':page,
        'posts':posts
    }






    return render(request,template_name,context)


#detail view
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug = post, status='published',
                                publish__year= year, publish__month= month, publish__day= day)
    template_name = 'post/detail.html'
    context = {
        'post':post
    }
    return render(request,template_name,context)
