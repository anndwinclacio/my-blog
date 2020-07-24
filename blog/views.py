from django.shortcuts import render, get_object_or_404
from .models import Post  # this will include thd model we have written in another file
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect #this is used to immediately go to the post_detail page after creating a post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST": 
        form = PostForm(request.POST) # to construct the PostForm with the data from the form
        if form.is_valid(): # to check if the form is correct and all required fields are set
            post = form.save(commit=False) # we save the form using form.save and the commit=False means that we don't want to save the Post model yet.
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) # to redirect to the post_detail to see the recent blogpost
    else:
        form = PostForm()
    
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request,pk):
    post = get_object_or_404 (Post, pk=pk)
    if request.method == "POST":
        form = PostForm (request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) # to redirect to the post_detail to see the recent blogpost
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})    
    