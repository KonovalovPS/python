from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import auth
from django.core.paginator import Paginator
# Create your views here.

from blog.models import User, Blogg, Post, Comment
from blog.forms import CommentForm, NewBlogForm, NewPostForm, EditPostForm, NewUserForm
    
def index(request):
    blogs = Blogg.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blog/index.html', context)
    
def my_blogs(request):
    username = request.user.username
    id = request.user.id
    blogs = Blogg.objects.filter(user_id = id)
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    context = {'blogs': blogs,
               'num_visits': num_visits,
               'username': username
               }
    return render(request, 'blog/my_blogs.html', context)
    
class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        username = self.request.user.username
        context['appropriate_blog'] = Post.objects.filter(blog_id = pk)
        context['name_blog'] = Blogg.objects.get(id = pk).blog_name
        context['username'] = Blogg.objects.get(id = pk).user_id.username
        context['post_add_url'] = '/blog/{}/post_add'.format(Blogg.objects.get(id = pk).id)
        return context
    
class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    paginate_by = 3
    
    def comment_list(self):
        comments = self.object.comment_set.all().order_by('pub_date')
        paginator = Paginator(comments, 10)
        page = self.request.GET.get('page')
        return paginator.get_page(page)
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        post_obj = Post.objects.get(id = pk)
        post_obj.views += 1
        post_obj.save()
        #context['appropriate_comment'] = Comment.objects.filter(post_id = pk)
        context['comments'] = self.comment_list
        context['post_edit_url'] = '/blog/posts/{}/post_edit'.format(Post.objects.get(id = pk).id)
        return context
    
    
class CommentAdd(CreateView):
    template_name = 'blog/comment_add.html'
    form_class = CommentForm
    def get_initial(self):
        user_id = self.request.user.id
        return {
            "post_id": self.kwargs['post_pk'],
            "user_id": user_id
    }
    
    def get_success_url(self):
        return "/blog/posts/{}/".format(self.kwargs['post_pk'])
        
class BlogAdd(CreateView):
    template_name = 'blog/blog_add.html'
    form_class = NewBlogForm
    
    def get_success_url(self):
        return "/blog/"
        
    def get_initial(self):
        user_id = self.request.user.id
        return {
            "user_id": user_id
    }
        
class PostAdd(CreateView):
    model = Blogg
    template_name = 'blog/post_add.html'
    form_class = NewPostForm
    
    def get_success_url(self):
        return "/blog/"
        
    def get_initial(self):
        user_id = self.request.user.id
        return {
            "user_id": user_id,
            "blog_id": self.kwargs['blog_pk']                  
        }
        
def user_add(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # url = user.get_url()
            return redirect('/blog/accounts/login/')
    else:
        form = NewUserForm()
    return render(request, 'blog/registration.html', {
        'form': form
    })
        
class PostEdit(UpdateView):
   
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = EditPostForm
    
    def get_success_url(self):
        return "/blog/posts/{}/".format(self.kwargs['pk'])


