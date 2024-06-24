
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'chat', ChatViewSet, 'chat')
router.register(r'chatinstance', ChatInstanceViewSet, 'chatinstance')
router.register(r'user', UserViewSet, 'user')


urlpatterns = [
   path('api/', include(router.urls)),
   path('admin/login', login_user),
   path('login/', login_user),
   path('logout/', logout_user),
   path('accounts/google/login/callback/', oauth_callback),
   path('chat/', process_reply),
   ]