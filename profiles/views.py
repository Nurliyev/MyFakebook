from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from .models import User, Friendships


# Create your views here.
class UserDetail(LoginRequiredMixin, DetailView):
    template_name = 'profiles/profile-detail.html'
    context_object_name = 'author'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.kwargs.get('pk'))
        try:
            context['friend_request'] = Friendships.objects.get(sender_id=self.request.user.id,
                                                                receiver_id=self.kwargs.get('pk'))
        except:
            pass
        return context


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    context_object_name = 'author'
    fields = ['avatar', 'first_name', 'last_name', 'bio']
    success_url = reverse_lazy('post-list')
    template_name = 'profiles/edit-profile.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()  # This should help to get current user

        # Next, try looking up by primary key of Usario model.
        queryset = queryset.filter(pk=self.request.user.id)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No user matching this query")
        return obj


def send_friend_request(request, userID):
    sender = request.user
    receiver = User.objects.get(id=userID)
    friendship, created = Friendships.objects.get_or_create(
        sender=sender, receiver=receiver
    )
    if created:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def accept_friend_request(request, requestID):
    friendships = Friendships.objects.get(id=requestID)
    if friendships.receiver == request.user:
        friendships.receiver.friends.add(friendships.sender)
        friendships.sender.friends.add(friendships.receiver)
        friendships.delete()
    return redirect('notifications')


def delete_friend_request(request, deleteID):
    user_profile = request.user
    friend_profile = get_object_or_404(User, id=deleteID)  # Profile instance has the same id as user
    user_profile.friends.remove(friend_profile)  # A removes B
    friend_profile.friends.remove(user_profile)  # B removes A
    return redirect('friend-list')


class FriendList(ListView):
    template_name = 'profiles/friends.html'
    context_object_name = 'friends'
    model = User

    def get_context_data(self, **kwargs):
        context = super(FriendList, self).get_context_data(**kwargs)
        context['count'] = Friendships.objects.filter(receiver=self.request.user).count()
        return context
