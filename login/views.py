from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import *
from .tokens import *
from .forms import CreateCustomerForm, EvaluationForm, EvaluationForm, CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


@login_required(login_url='login')
@admin_only
def evaluationRequests(request):
    evaluations = Evaluation.objects.all()
    context = {'evaluations': evaluations}
    return render(request, 'login/evaluationRequests.html', context)


@login_required(login_url='login')
def requestEvaluation(request):
    form = EvaluationForm()
    if(request.method == 'POST'):
        form = EvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            evaluation = form.save()
            evaluation.customer = request.user.customer
            evaluation.save()
            messages.success(
                request, 'Your request has been succesfully made.')
            return redirect('request-evaluation')
        else:
            print('No')
    context = {'form': form}
    return render(request, 'login/requestEvaluation.html', context)


def registerPage(request):
    form = CreateUserForm()
    if(request.method == 'POST'):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')

    context = {'form': form}
    return render(request, 'login/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    customerForm = CreateCustomerForm(request.POST or None)
    context = {'customerForm': customerForm}
    if user is not None and account_activation_token.check_token(user, token):
        if customerForm.is_valid():
            user.is_active = True
            user.save()
            contact_number = customerForm.cleaned_data.get(
                'contact_number')
            Customer.objects.create(user=user, username=user.username,
                                    email=user.email, contact_number=contact_number)
            messages.success(
                request, 'Your account has been succesfully activated.')
            return redirect('login')
    return render(request, 'login/activate.html', context)


def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                current_site = get_current_site(request)
                mail_subject = "Two Factor Authentication"
                message = render_to_string('login/two_factor_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user), })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()
                return HttpResponse('Two Factor Authentication email has been sent to your email address. Please check it.')
            else:
                messages.info(request, 'Username or password is not correct.')

    context = {'form': form}
    return render(request, 'login/login.html', context)


def authenticate_login(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        login(request, user)
        if user.is_superuser:
            return redirect('evaluation-requests')
        return redirect('request-evaluation')


def logoutPage(request):
    logout(request)
    return redirect(loginPage)


# Create your views here.
