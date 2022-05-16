from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import login
from profiles.models import User, Friendships
from django.views.generic import ListView


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('post-list')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'main/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post-list')
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': _('Become a member')})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('article-list')
        form = self.form_class(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.username = user_form.username.lower()
            same_email_user = User.objects.filter(email=user_form.email, is_active=True).exists()
            user = None
            if not same_email_user:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # send email
                mail_subject = force_text(_("Activate your account.")).strip()
                html_message = render_to_string('main/acc_active_email.html', {
                    'full_name': user.get_full_name(),
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                plain_message = strip_tags(html_message).strip()
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, plain_message, "Fakebook <verify@fakebook.com>", [to_email],
                          html_message=html_message)
                return render(request, "main/info_view.html",
                              {"data": _("Please confirm your email address to complete the registration")})
            else:
                form.add_error("email", _("User with this email already exists!"))
            if user is not None:
                login(request, user)
                return redirect('article-list')
            else:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form, 'title': _('Become a member')})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        User.objects.filter(email=user.email, is_active=False).delete()
        login(request, user)
        return render(request, "main/info_view.html",
                      {"data": _("Thank you for your email confirmation. Now you can start using your account."),
                       "redirect_page": redirect("post-list").url})
    else:
        return render(request, "main/info_view.html", {"data": _("Activation link is invalid!")})

