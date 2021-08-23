from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
import json
from django.contrib import messages
from .forms import CommentForm
from .models import Post, Comments
from profiles.models import Friendships


# Create your views here.

class PostList(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    model = Post
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['count'] = Friendships.objects.filter(receiver=self.request.user).count()
        return context

    def paginate_queryset(self, queryset, page_size, ):
        paginator = self.get_paginator(queryset, page_size, orphans=self.get_paginate_orphans(),
                                       allow_empty_first_page=self.get_allow_empty())
        page = self.request.GET.get("page", 1)
        try:
            page_number = int(page)
            if page_number > paginator.num_pages or page_number < 1:
                page_number = 1
        except ValueError:
            page_number = 1
        page = paginator.page(page_number)
        return paginator, page, page.object_list, page.has_other_pages()


class PostCreate(CreateView):
    model = Post
    fields = ['avatar', 'content']
    success_url = reverse_lazy('post-list')
    template_name = 'posts/post-create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['avatar', 'content']
    template_name = 'posts/post-update.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdate, self).form_valid(form)


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if obj.author != self.request.user:
            raise Http404
        return obj


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post-detail.html'
    context_object_name = 'post'
    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.id
            }))

    def get_context_data(self, **kwargs):
        post_comments_count = Comments.objects.all().filter(post=self.object.id).count()
        post_comments = Comments.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'comments': post_comments,
            'comments_count': post_comments_count,
        })
        return context


class LikeView(View):
    http_method_names = ['post']

    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
        user = self.request.user
        body = json.loads(request.body)
        post_id = body.get('id')
        post = get_object_or_404(Post, id=post_id)
        is_liked = False
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            is_liked = True
        context = {'total_likes': post.total_likes, 'is_liked': is_liked}
        return HttpResponse(json.dumps(context), content_type='application/json')
