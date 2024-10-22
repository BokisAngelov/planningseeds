from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('profiles/', views.userProfiles, name="userprofiles"),
    path('edit-profile/', views.editUser, name="edit-user"),

    path('', views.homepage, name='homepage'),
    path('products-list/', views.product_list, name='products-list'),
    path('product/<str:pk>/', views.product, name="product"),
    path('create-product/', views.createProduct, name="create-product"),
    path('update-product/<str:pk>', views.updateProduct, name="update-product"),
    # path('edit-product/<str:pk>', views.editProduct, name="edit-product"),
    path('delete-product/<str:pk>', views.deleteProduct, name="delete-product"),

    path('request-offer/<str:pk>', views.request_offer, name="request-offer"),
    path('send-offer/<str:pk>', views.sendOffer, name="send-offer"),
    path('send-invoice/<uuid:offer_id>', views.sendInvoice, name="send-invoice"),
    path('accept-offer/<uuid:offer_id>/', views.acceptOffer, name='accept-offer'),
    path('filter-requests/<str:pk>/', views.userProfile, name='filter-requests'),
    path('edit-offer/<uuid:pk>/', views.editOffer, name="edit-offer"),
    
]
