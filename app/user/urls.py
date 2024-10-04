from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import *


app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get/<str:email>', RetrieveUserView.as_view(), name='get'),
    path('list/', ListUserView.as_view(), name='list'),
    path('update/<str:email>', UpdateUserView.as_view(), name='update'),
    path('delete/<str:email>', DeleteUserView.as_view(), name='delete'),

]
