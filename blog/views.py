from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,DetailView
from .models import BlogPost,Like,Comment
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.edit import FormView
from .forms import CommentForm
class Home(ListView):
    model = BlogPost
    template_name ='blog/home.html'
    context_object_name = 'posts'  # Use 'posts' in the template
    ordering = ['-created_at']  #

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/blogpost_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as the author
        self.object = form.save()  # Save the post
        return redirect('home')  #

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'  # Use 'post' in the template
    
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog/registration.html'
    success_url = reverse_lazy('login') 

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(BlogPost, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete() 
        return redirect('post-detail', pk=pk)


class CommentCreateView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'blog/blogpost_detail.html'

    def form_valid(self, form):
        post = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.name = self.request.user.username
        form.save()
        return redirect('post-detail', pk=post.pk)
