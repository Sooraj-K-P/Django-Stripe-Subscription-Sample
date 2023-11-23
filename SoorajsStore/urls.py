from django.contrib import admin
from django.urls import path, include
from membership import views

urlpatterns = [
    path('membership/', include('membership.urls')),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup', views.SignUp.as_view(), name='signup'),
    path('auth/settings', views.settings, name='settings'),
    path('join', views.join, name='join'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('updateaccounts', views.updateaccounts, name='updateaccounts'),
    path('deletesub',views.delete,name='delete'),
    path('modify',views.modify,name='modify'), 
    path('upgrade',views.upgrade,name='upgrade'), 
    path('pause',views.pausepayments,name='pausepayments'),
    path('unpause',views.unpause,name='unpause'),
    path('send_invoice',views.send_invoice,name='send_invoice'),
    path('downgrade',views.downgrade,name='downgrade'),
]