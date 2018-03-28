
from users import views
from django.conf.urls import url,include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', views.UserList, base_name="users")

urlpatterns = [
    url(r'^', include(router.urls)),
]
