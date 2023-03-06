from django.urls import path
from OrderManagement import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/', views.myProfile),
    path('dashboard/', views.dashBoard),
    path('notyetfinished/', views.notYetFinished),

    path('product/main/', views.productMain),
    path('product/add/', views.productAdd),
    path('product/delete/<int:rid>/', views.productDel),
    path('product/edit/<int:rid>/', views.productEdit),

    path('customer/main/', views.customerMain),
    path('customer/add/', views.customerAdd),
    path('customer/delete/<int:cid>/', views.customerDel),
    path('customer/edit/<int:cid>/', views.customerEdit),
    
    path('order/my/', views.orderMy),
    path('order/create/', views.orderCreate),
    path('order/create/<int:cid>/', views.orderCustomer),
    path('order/delete/<int:oid>/', views.orderDel),
    path('order/addproduct/<str:oid>/', views.addProduct),
    path('order/review/<int:oid>/', views.orderReview),
    
    path('include/edit/<int:id>/', views.includeEdit),
    path('include/delete/<int:id>/', views.includeDel),
]
