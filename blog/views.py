from django.shortcuts import render,get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DeleteView
from .forms import MailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

################################## EMAIL FORM ######################################
def post_share(request,post_id):
    post = get_object_or_404(Post, id =post_id, status= 'published')
    sent = False

    if request.method == 'POST':
        form = MailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@gmail.com',[cd['to']])
            sent = True
    else:
        form = MailPostForm()
    template_name = 'post/share.html'
    context = {
        'post':post,
        'form':form,
        'sent':sent,
    }
    return render(request,template_name,context)


################################## Function Based ###################################
def post_list(request,tag_slug=None):
    
    object_list = Post.published.all()
    #tag
    tag = None
    if tag_slug:
        tag         = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in =[tag])


    ##
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
        'page_obj':page,
        'posts':posts,
        'tag':tag,
    }






    return render(request,template_name,context)


#detail view
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug = post, status='published',
                                publish__year= year, publish__month= month, publish__day= day)
    # comment_form = CommentForm()
    ####comment
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    #### Similar Posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:4]

    template_name = 'post/detail.html'
    context = {
        'post':post,
        'new_comment':new_comment,
        
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts':similar_posts,
    }
    return render(request,template_name,context)
#############################################################
# CLASS BASED VIEW
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'post/list.html'