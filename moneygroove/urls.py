from django.urls import (
    include,
    path,
)
from iommi.admin import (
    Admin,
    Auth,
)
from moneygroove import views

urlpatterns = [
    path('admin/', include(Admin().urls())),
    path('', views.IndexPage().as_view()),
    path('login/', Auth.login),
    path('api/v1/groove/', views.api__groove),
]
