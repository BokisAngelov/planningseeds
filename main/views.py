from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from .models import Product, UserProfile, Request, Offer, Invoice, Categories
from .forms import CustomUserCreationForm, ProductForm, RequestOfferForm, UserEditForm, SendOfferForm, OfferEditForm
from django.conf import settings
from django.template.loader import render_to_string
import openpyxl
import os
import pycountry
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import token_generator
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

def custom_404_view(request, exception):
    return render(request, "main/404.html", status=404)

def analytics(request):

    if request.user.is_authenticated:
        # if request.user.userprofile.user_type == 'admin':
            # get all users
            producers = UserProfile.objects.filter(user_type='producer')
            customers = UserProfile.objects.filter(user_type='customer')

            # get all products
            products = Product.objects.all()
            # get all requests
            requests = Request.objects.all()
            # get all offers
            offers = Offer.objects.all()

            context = {
                'producers': producers,
                'customers': customers,
                'products': products,
            }
            return render(request, 'main/analytics.html')
        # else:
        #     return redirect('homepage')
    else:
        return redirect('login')


def send_email_invoice(request, offer):
    try:
        subject = f"Planning Seeds - Invoice for {offer.request.product.name}"
        message = render_to_string('main/email_invoice_template.html', {
            'offer': offer,
            'request': request
        })

        send_mail(subject, message, settings.EMAIL_HOST_USER, [offer.request.user.email])

        return True
    
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        messages.error(request, f"Error sending email. Please try again later.")

        return False
    

def send_email_accepted_offer(request, offer):
    try:
        subject = f"Planning Seeds - Offer {offer.status} for {offer.request.product.name}"
        message = render_to_string('main/email_offer_accepted_template.html', {
            'offer': offer,
            'request': request
        })

        send_mail(subject, message, settings.EMAIL_HOST_USER, [offer.producer.user.email])

        return True
    
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        messages.error(request, f"Error sending email. Please try again later.")

        return False
    

def send_email_for_offer(request, offer):
    try:
        subject = f"Planning Seeds - New offer for {offer.request.product.name}"
        message = render_to_string('main/email_offer_template.html', {
            'offer': offer,
            'request': request
        })

        send_mail(subject, message, settings.EMAIL_HOST_USER, [offer.request.user.email])

        return True
    
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        messages.error(request, f"Error sending email. Please try again later.")

        return False

def send_email_for_request(request, request_offer):
    try:
            
        subject = f"Planning Seeds - New request for {request_offer.product.name}"
        message = render_to_string('main/email_request_template.html', {
            'request': request,
            'request_offer': request_offer
        })

        send_mail(subject, message, settings.EMAIL_HOST_USER, [request_offer.product.producer.user.email])

        return True

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        messages.error(request, f"Error sending email. Please try again later.")

        return False

def send_verification_email(user, request):
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(f"/verify-email/{uid}/{token}/")
    subject = "Planning Seeds - Verify your email"
    message = render_to_string('main/email_verification_template.html', {
        'user': user,
        'verification_link': verification_link
    })

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Welcome, your email has been verified!")
        login(request, user)
        return redirect('homepage')
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect('register')

def howWorks(request):
    context = {
        'hello': _('HELLO')
    }
    return render(request, 'main/how_works.html', context)

def privacyPolicy(request):
    return render(request, 'main/privacy_policy.html')

def homepage(request):
    producers = UserProfile.objects.filter(user_type='producer').exclude(user__is_superuser=True)[:8]
    products = Product.objects.order_by('-created')[:5]

    context = {
        'producers': producers,
        'products': products,
    }
    return render(request, 'main/home.html', context)



def product_list(request):
    products = Product.objects.order_by('-created')
    categories = Categories.objects.all()
    country_codes = (
        UserProfile.objects.filter(user_type='producer')
        .exclude(country=None)
        .values_list('country', flat=True)
        .distinct()
    )

    countries = [
        {"code": code, "name": pycountry.countries.get(alpha_2=code).name}
        for code in set(country_codes)
    ]

    context = {
        'products': products,
        'categories': categories,
        'countries': countries
    }
    return render(request, 'main/product_list.html', context)

def filter_products(request):
    categories = request.GET.getlist('categories')
    countries = request.GET.getlist('countries')

    products = Product.objects.all()

    if categories:
        products = Product.objects.filter(category__in=categories)
    if countries:
        products = Product.objects.filter(producer__country__in=countries)

    
    products = products.distinct()
    products = products.order_by('-created')
    
    html = render_to_string('main/product_filter_grid.html', {'products': products})
    return JsonResponse({'html': html})

def filter_producers(request):
    countries = request.GET.getlist('countries')
    producers = UserProfile.objects.filter(user_type='producer', user__is_superuser=False)

    if countries:
        producers = UserProfile.objects.filter(user_type='producer', country__in=countries)

    producers = producers.distinct()
    producers = producers.order_by('-created')

    html = render_to_string('main/profiles_filter_grid.html', {'profiles': producers})
    return JsonResponse({'html': html})

def filterInvoices(request):
    invoice_status = request.GET.get('status')

    if invoice_status:
        invoices = Invoice.objects.filter(status=invoice_status, offer__producer=request.user.userprofile)
    else:
        invoices = Invoice.objects.filter(offer__producer=request.user.userprofile)
        
    invoices = invoices.distinct()
    invoices = invoices.order_by('-created')

    html = render_to_string('main/invoices_filter_table.html', {'invoices': invoices})
    return JsonResponse({'html': html})

def filterOffers(request):
    offer_status = request.GET.get('status')

    if offer_status:
        offers = Offer.objects.filter(status=offer_status, producer=request.user.userprofile)
    else:
        offers = Offer.objects.filter(producer=request.user.userprofile)
        
    offers = offers.distinct()
    offers = offers.order_by('-created')

    html = render_to_string('main/offers_filter_table.html', {'offers': offers})
    return JsonResponse({'html': html})

def filter_customer_requests(request):
    status = request.GET.get('status')

    if status:
        requests = Request.objects.filter(status=status, user=request.user.userprofile)
    else:
        requests = Request.objects.filter(user=request.user.userprofile)
        
    requests = requests.distinct()
    requests = requests.order_by('-created')

    html = render_to_string('main/requests_customer_filter_table.html', {'requests': requests})
    return JsonResponse({'html': html})

def product(request, pk):
    productObj = Product.objects.get(id=pk)
    requestsTo = Request.objects.filter(product=productObj)

    # Initialize empty QuerySets for unauthenticated users
    requestsFrom = Request.objects.none()
    offers = Offer.objects.none()

    if request.user.is_authenticated:
        requestsFrom = Request.objects.filter(product=productObj, user=request.user.userprofile)
        offers = Offer.objects.filter(producer=request.user.userprofile, request__product=productObj)

    context = {
        'productObj': productObj,
        'requestsTo': requestsTo,
        'requestsFrom': requestsFrom,
        'offers': offers,
    }
    return render(request, 'main/product.html', context)

def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except: 
            messages.error(request, 'Username does not exists!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username or pass is incorrect')

    return render(request, 'main/login_register.html')

def logoutUser(request):
    logout(request)

    return redirect('/')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()

            # Collect error messages
            error_messages = []

            # Check email validity
            email = form.cleaned_data.get('email')
            if not email:
                error_messages.append("Email is required.")
            elif UserProfile.objects.filter(email=email).exists():
                error_messages.append("This email is already in use.")

            # Check required fields
            required_fields = ['user_type', 'country']
            for field in required_fields:
                if not form.cleaned_data.get(field):
                    error_messages.append(f"{field.replace('_', ' ').capitalize()} is required.")

            if error_messages:
                # Add all error messages to messages.error
                messages.error(request, " ".join(error_messages))
            else:
                user.is_active = False
                user.save()
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'last_name': user.last_name,
                        'email': email,
                        'user_type': form.cleaned_data.get('user_type'),
                        'country': form.cleaned_data.get('country'),
                    }
                )
                
                send_verification_email(user, request)
                messages.success(request, 'A verification link has been sent to your email! Please verify your email before logging in.')
                
                return redirect('/')
        else:
            # Handle form.errors
            for field, errors in form.errors.items():
                messages.error(request, f"{field.capitalize()}: {' '.join(errors)}")

    context = {'page': page, 'form': form}
    return render(request, 'main/login_register.html', context)

@login_required(login_url="login")
def editUser(request):
    profile = request.user.userprofile #get logged in user
    form = UserEditForm(instance=profile)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have updated your profile!')
            return redirect('user-profile', profile.id) 

    context = {'form': form}
    return render(request, 'main/edit_profile.html', context)

@login_required(login_url="login")
def createProduct(request):

    profile = request.user.userprofile

    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            product.producer = profile
            form.save()
            messages.success(request, 'Good Job! You have added a new product.')
            return redirect('user-profile', profile.id)

    context = {'form': form}
    return render(request, 'main/product_form.html', context)

@login_required(login_url="login")
def updateProduct(request, pk):

    profile = request.user.userprofile

    if profile.user_type != 'producer':
        return redirect('/')
    
    product = profile.product_set.get(id=pk) # get only users products
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your product has been updated!')
            return redirect('product', product.id)

    context = {'form': form, 'product': product}
    return render(request, 'main/edit_product.html', context)


@login_required(login_url="login")
def deleteProduct(request, pk):

    profile = request.user.userprofile
    product = profile.product_set.get(id=pk) # get only users products

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Your product has been deleted!')
        return redirect('user-profile', profile.id)

    context = {'object': product}
    return render(request, 'main/delete_template.html', context)

@login_required(login_url="login")
def request_offer(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = RequestOfferForm(request.POST)
        if form.is_valid():
            request_offer = form.save(commit=False)
            request_offer.product = product
            # request_offer.user = request.user.userprofile.user
            user_profile = get_object_or_404(UserProfile, user=request.user)
            request_offer.user = user_profile  

            if send_email_for_request(request, request_offer):

                request_offer.save()
                # previous_url = request.META.get('HTTP_REFERER', '/')
                # send_email_for_request(request, request_offer)
                messages.success(request, 'Your request has been sent to the producer!')
                return redirect('product', product.id)
            
            else:
                messages.error(request, 'Failed to send the email. Please try again later.')
    else:
        form = RequestOfferForm()

    context = {'form': form, 'product': product}
    return render(request, 'main/request_offer.html', context)

@login_required(login_url='login')
def sendOffer(request, pk):
    for_request = get_object_or_404(Request, id=pk)

    if request.method == 'POST':
        form = SendOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.request = for_request
            offer.producer = for_request.product.producer
            offer.quantity = for_request.quantity

            if send_email_for_offer(request, offer):
                # If email is sent successfully, save the offer and update request status
                offer.save()
                for_request.status = 'In-progress'
                for_request.save()
                messages.success(request, 'Your offer has been sent to the customer!')
                return redirect('user-profile', pk=request.user.userprofile.id)
            else:
                # If email fails, show an error message and do not save the offer
                messages.error(request, 'Failed to send the email. Please try again later.')

    else:
        form = SendOfferForm()

    context = {'form': form, 'for_request': for_request}
    return render(request, 'main/send-offer.html', context)

@login_required(login_url='login')
def viewOffer(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    offer = Offer.objects.filter(producer=user)

    context = {'user': user, 'offers':offer}
    return render(request, 'main/view-offer', context)

@login_required(login_url="login")
def editOffer(request, pk):

    offer = Offer.objects.get(id=pk)
    form = OfferEditForm(instance=offer)

    if request.method == 'POST':
        form = OfferEditForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have updated your offer!')
            return redirect('send-invoice', offer.id) 

    context = {'form': form}
    return render(request, 'main/edit_offer.html', context)

def userProfile(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    # current_user = request.user.userprofile.user
    products = Product.objects.filter(producer=user)
    requestsFrom = None
    requestsTo = None
    offers = None
    received_offers= None
    send_invoices = None
    received_invoices = None
    inv_total = None

    if request.user.is_authenticated:

        is_owner = request.user == user.user
    # Fetch requests based on the user type
        if user.user_type == 'producer' and is_owner:
            requestsFrom = Request.objects.filter(product__producer=user)
            offers = Offer.objects.filter(producer=user)
            send_invoices = Invoice.objects.filter(offer__producer=user)
            # Calculate the grand total
            inv_total = sum(inv.offer.total_price for inv in send_invoices)
        elif request.user.userprofile.user_type == 'customer':
                requestsTo = Request.objects.filter(user=request.user.userprofile)
                received_offers = Offer.objects.filter(request__in=requestsTo)
                received_invoices = Invoice.objects.filter(offer__request__user=user)
        
    # Handle AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        status = request.GET.get('status', '')
        if status:
            requestsTo = Request.objects.filter(product__producer=user, status=status)
        else:
            requestsTo = Request.objects.filter(product__producer=user)
            
        return render(request, 'main/requests_table.html', {'requests': requestsTo})
    
    context = {
        'user': user, 
        'requestsFrom': requestsFrom, 
        'requestsTo': requestsTo, 
        'products': products, 
        'offers': offers, 
        'received_offers': received_offers, 
        'is_owner': request.user == user.user,
        'send_invoices': send_invoices,
        'received_invoices': received_invoices,
        'inv_total': inv_total
        }
    return render(request, 'main/user_profile.html', context)

def userProfiles(request):
    profiles = UserProfile.objects.filter(user_type='producer')
    country_codes = (
        UserProfile.objects.filter(user_type='producer')
        .exclude(country=None)
        .values_list('country', flat=True)
        .distinct()
    )

    countries = [
        {"code": code, "name": pycountry.countries.get(alpha_2=code).name}
        for code in set(country_codes)
    ]
   
    context = {'profiles': profiles, 'countries': countries}
    return render(request, 'main/profiles.html', context)

@login_required(login_url='login')
def acceptOffer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, id=offer_id)
        for_request = offer.request
        answer_status = request.POST.get('answer-status')

        if request.user.userprofile == offer.request.user and answer_status == 'Accepted':
            offer.status = 'Accepted'

            if send_email_accepted_offer(request, offer):              
                offer.save()
                for_request.status = 'Accepted'
                for_request.save()
                return JsonResponse({'success': True})
        elif request.user.userprofile == offer.request.user and answer_status == 'Rejected':
            offer.status = 'Rejected'

            if send_email_accepted_offer(request, offer):
                offer.save()
                for_request.status = 'Rejected'
                for_request.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'You are not authorized to accept this offer.'}, status=403)
        
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)   

@login_required(login_url='login')
def sendInvoice(request, offer_id):
    
    offer = get_object_or_404(Offer, id=offer_id)
    
    if request.user.userprofile != offer.producer:
        return HttpResponse('Unauthorized', status=403)
    
    invoice_dir = os.path.join(settings.MEDIA_ROOT, 'docs')
    invoice_filename = f'Invoice_{offer.id}.xlsx'
    invoice_file_path = os.path.join(invoice_dir, invoice_filename)
    
    if request.method == 'POST':
        # Load the Excel template
        template_path = os.path.join(settings.MEDIA_ROOT, 'docs', 'InvoiceTemplate.xlsx')
        wb = openpyxl.load_workbook(template_path)
        sheet = wb.active

        # need to generate invoice number randomly 

        # Populate the template with offer data
        sheet['A16'] = offer.request.product.name  # Set product name
        sheet['F16'] = offer.quantity  # Set quantity
        sheet['G16'] = offer.unit_price  # Set unit price
        sheet['H16'] = offer.total_price  # Set total price
        # sheet['B6'] = offer.delivery_timeline  # Set delivery timeline

        # Add producer details to the invoice
        producer = offer.producer
        customer = offer.request.user
        sheet['A1'] = producer.first_name + producer.last_name  # Producer's full name
        sheet['A3'] = producer.user.email  # Producer's email
        sheet['A4'] = producer.phone_number  # Producer's phone number (assuming this field exists)
        sheet['A2'] = producer.address  # Producer's address (assuming this field exists)
        sheet['A8'] = customer.first_name + customer.last_name
        sheet['A9'] = customer.company_name
        sheet['A10'] = customer.address
        sheet['A12'] = customer.phone_number

        # Save the filled template as a new file for preview
        wb.save(invoice_file_path)
        #  need to send email here with the document maybe attached

        # Save the invoice to the database
        create_invoice_record = Invoice.objects.create(offer=offer, invoice_file=invoice_file_path)
        send_email_invoice(request, offer)
        messages.success(request, 'You have sent the invoice successfully!')
        # Redirect to a success page or back to the profile
        return redirect('user-profile', pk=request.user.userprofile.id)

    return render(request, 'main/send-invoice.html', {'offer': offer})