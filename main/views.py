from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from .models import Product, UserProfile, Request, Offer, Invoice
from .forms import CustomUserCreationForm, ProductForm, RequestOfferForm, UserEditForm, SendOfferForm, OfferEditForm
from django.conf import settings
import openpyxl
import os


def homepage(request):
    producers = UserProfile.objects.filter(user_type='producer')
    products = Product.objects.all()

    context = {
        'producers': producers,
        'products': products,
    }
    return render(request, 'main/home.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

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
    messages.error(request, 'User was logged out!')
    return redirect('/')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.user_type = form.cleaned_data.get('user_type')
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Error occurred during registration!')

    context = {'page': page, 'form':form}
    return render(request, 'main/login_register.html', context)

@login_required(login_url="login")
def editUser(request):
    profile = request.user.userprofile #get logged in user
    form = UserEditForm(instance=profile)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
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
            return redirect('product', product.id)

    context = {'form': form, 'product': product}
    return render(request, 'main/edit_product.html', context)

# @login_required(login_url="login")
# def editProduct(request, pk):

#     return render(request, 'main/edit_product.html')

@login_required(login_url="login")
def deleteProduct(request, pk):

    profile = request.user.userprofile
    product = profile.product_set.get(id=pk) # get only users products

    if request.method == 'POST':
        product.delete()
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
            request_offer.save()
            # previous_url = request.META.get('HTTP_REFERER', '/')
            messages.success(request, 'Your request has been sent to the producer!')
            return redirect('product', product.id)
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
            offer.save()

            for_request.status = 'In-progress'
            for_request.save()

            messages.success(request, 'Your offer has been sent to the customer!')
            return redirect('user-profile', pk=request.user.userprofile.id)
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


        # Add logging to see what requests are being fetched
        # print(f"AJAX request status: {status}")
        # print(f"Filtered requests count: {requestsTo.count()}")

            
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
   
    context = {'profiles': profiles}
    return render(request, 'main/profiles.html', context)

@login_required(login_url='login')
def acceptOffer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, id=offer_id)
        for_request = offer.request
        answer_status = request.POST.get('answer-status')

        if request.user.userprofile == offer.request.user and answer_status == 'Accepted':
            offer.status = 'Accepted'
            offer.save()
            for_request.status = 'Accepted'
            for_request.save()
            return JsonResponse({'success': True})
        elif request.user.userprofile == offer.request.user and answer_status == 'Rejected':
            offer.status = 'Rejected'
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
    print(request.POST)
    if request.user.userprofile != offer.producer:
        return HttpResponse('Unauthorized', status=403)
    
    invoice_dir = os.path.join(settings.MEDIA_ROOT, 'docs')
    invoice_filename = f'Invoice_{offer.id}.xlsx'
    invoice_file_path = os.path.join(invoice_dir, invoice_filename)
    
    if request.method == 'POST':
        if 'preview' in request.POST:
            # Load the Excel template
            template_path = os.path.join(settings.MEDIA_ROOT, 'docs', 'InvoiceTemplate.xlsx')
            wb = openpyxl.load_workbook(template_path)
            sheet = wb.active

            # Populate the template with offer data
            sheet['A16'] = offer.request.product.name  # Set product name
            sheet['F16'] = offer.quantity  # Set quantity
            sheet['G16'] = offer.unit_price  # Set unit price
            sheet['H16'] = offer.total_price  # Set total price
            # sheet['B6'] = offer.delivery_timeline  # Set delivery timeline

            # Add producer details to the invoice
            producer = offer.producer
            customer = offer.request.user
            sheet['A1'] = producer.user.get_full_name()  # Producer's full name
            sheet['A3'] = producer.user.email  # Producer's email
            sheet['A4'] = producer.phone_number  # Producer's phone number (assuming this field exists)
            sheet['A2'] = producer.address  # Producer's address (assuming this field exists)
            sheet['B8'] = customer.user.get_full_name()
            sheet['B9'] = customer.company_name
            sheet['B10'] = customer.address
            sheet['B12'] = customer.phone_number

            # Save the filled template as a new file for preview
            wb.save(invoice_file_path)

            # Render the preview page
            return render(request, 'main/preview-invoice.html', {'offer': offer, 'invoice_file': invoice_filename})

        elif 'submit' in request.POST:
            # Save the invoice to the database
            invoice = Invoice.objects.create(offer=offer, invoice_file=invoice_file_path)

            # Redirect to a success page or back to the profile
            return redirect('user-profile', pk=request.user.userprofile.id)
        
        # elif 'cancel' in request.POST:
        #     # Delete the invoice from the database
        #     invoice = Invoice.objects.get(offer=offer)
        #     invoice.delete()

            # Redirect to a success page or back to the profile
            return redirect('user-profile', pk=request.user.userprofile.id)


    return render(request, 'main/send-invoice.html', {'offer': offer})