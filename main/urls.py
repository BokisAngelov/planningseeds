from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='main/password_reset_form.html', form_class=CustomPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('profiles/', views.userProfiles, name="userprofiles"),
    path('edit-profile/', views.editUser, name="edit-user"),
    path('filter-producers/', views.filter_producers, name='filter_producers'),

    path('', views.homepage, name='homepage'),
    path('products-list/', views.product_list, name='products-list'),
    path('product/<str:pk>/', views.product, name="product"),
    path('create-product/', views.createProduct, name="create-product"),
    path('update-product/<str:pk>', views.updateProduct, name="update-product"),
    # path('edit-product/<str:pk>', views.editProduct, name="edit-product"),
    path('delete-product/<str:pk>', views.deleteProduct, name="delete-product"),
    path('filter-products/', views.filter_products, name='filter_products'),

    path('request-offer/<str:pk>', views.request_offer, name="request-offer"),
    path('send-offer/<str:pk>', views.sendOffer, name="send-offer"),
    path('send-invoice/<uuid:offer_id>', views.sendInvoice, name="send-invoice"),
    path('accept-offer/<uuid:offer_id>/', views.acceptOffer, name='accept-offer'),
    path('edit-offer/<uuid:pk>/', views.editOffer, name="edit-offer"),
    path('filter-requests/<str:pk>/', views.userProfile, name='filter-requests'),
    path('filter-invoices/', views.filterInvoices, name='filter-invoices'),
    path('filter-offers/', views.filterOffers, name='filter-offers'),
    path('filter-customer-requests/', views.filter_customer_requests, name='filter-customer-requests'),

    path('how-it-works/', views.howWorks, name='how-it-works'),
    path('privacy-policy/', views.privacyPolicy, name='privacy-policy'),
    
]
