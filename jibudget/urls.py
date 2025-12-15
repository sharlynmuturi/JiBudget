from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('budget.urls')),
#     path('login/', auth_views.LoginView.as_view(template_name='budget/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]
from budget import views as budget_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', budget_views.home, name='home'),
    path('about/', budget_views.about, name='about'),  # 👈 Public home page
    path('app/', include('budget.urls')),      # 👈 All app views behind /app/
    path('login/', auth_views.LoginView.as_view(template_name='budget/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include('api.urls')),
    
    path('', include('pwa.urls')),
    

]
