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
from django.http import HttpResponse


# Only logged in users can access the page
@login_required(login_url='login')
# Only admin users can access the page
@admin_only
# Page for listing the evaluation requests
def evaluationRequests(request):
    evaluations = Evaluation.objects.all()
    context = {'evaluations': evaluations}
    return render(request, 'login/evaluationRequests.html', context)


# Only logged in users can access the page
@login_required(login_url='login')
# Page where users can request for evaluations
def requestEvaluation(request):
    # Bring a from to create an evaluation
    form = EvaluationForm()
    # When the form is submitted,
    if(request.method == 'POST'):
        # Bring the data and files that the user submitted
        form = EvaluationForm(request.POST, request.FILES)
        # When the form is all valid,
        if form.is_valid():
            # Make a model with the data from the form
            evaluation = form.save()
            evaluation.customer = request.user.customer
            evaluation.save()
            # Print a success message
            messages.success(
                request, 'Your request has been succesfully made.')
            # Redirect the page
            return redirect('request-evaluation')
    # Hand over the form so it can be rendered on the page
    context = {'form': form}
    # Render with the html file given
    return render(request, 'login/requestEvaluation.html', context)


# Page for registering as a user
def registerPage(request):
    # Bring a from to create a user
    form = CreateUserForm()
    # When the form is submitted,
    if(request.method == 'POST'):
        # Bring the data and files that the user submitted
        form = CreateUserForm(request.POST)
        # When the form is all valid,
        if form.is_valid():
            # Create a user with the data from the form
            user = form.save()
            # Set the user as inactive since they has not confirmed their email yet
            user.is_active = False
            user.save()
            # Get the current site's address
            current_site = get_current_site(request)
            # Set the title of the confimation email
            mail_subject = "Activate your account."
            # The contents of the confirmation email
            message = render_to_string('login/acc_active_email.html', {  # Bring the html file to write the content of the email
                # Set the user, domain, uid(encoded with base64), token
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            # Compose the email and send
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            # Tell the user that the email has been sent
            return HttpResponse('Please confirm your email address to complete the registration.')
    context = {'form': form}
    # Render with the html file given
    return render(request, 'login/register.html', context)


# The page that users see when clicking the link in the confimation email
def activate(request, uidb64, token):
    # Decode the uid and try to find the right user with it
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # Draw a form to create a customer
    customerForm = CreateCustomerForm(request.POST or None)
    context = {'customerForm': customerForm}
    # If the user is found and the token is valid,
    if user is not None and account_activation_token.check_token(user, token):
        # Check if the form (to put a contact number) is filled,
        if customerForm.is_valid():
            # Set the user as active
            user.is_active = True
            user.save()
            # Create a customer with the contact number given
            contact_number = customerForm.cleaned_data.get(
                'contact_number')
            Customer.objects.create(user=user, username=user.username,
                                    email=user.email, contact_number=contact_number)
            # Display a success message
            messages.success(
                request, 'Your account has been succesfully activated.')
            # Redirect to the login page
            return redirect('login')
    # Render with the html file given
    return render(request, 'login/activate.html', context)


# The page where users can sign in.
def loginPage(request):
    # Draw a form to sign in.
    form = LoginForm()
    # If the form is submitted,
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Authenticate the user with the given username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            # If the user is authenticated,
            if user is not None:
                # Create a two factor authentication email
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


# The function that is called when the user is authenticated by the two factor email
def authenticate_login(request, uidb64, token):
    # Decode the uid and try to find the right user with it
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # If the user is found and the token is valid,
    if user is not None and account_activation_token.check_token(user, token):
        # Sign in the user
        login(request, user)
        # If the user is admin(superuser), redirect to the page to see the list of requests
        if user.is_superuser:
            return redirect('evaluation-requests')
        # Otherwise, redirect to the page to request evaluations
        return redirect('request-evaluation')


# The function to sign out
def logoutPage(request):
    logout(request)
    return redirect(loginPage)


# Create your views here.
