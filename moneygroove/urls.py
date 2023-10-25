from django.urls import (
    include,
    path,
)
from iommi.admin import Admin
from moneygroove import views

urlpatterns = [
    path('admin/', include(Admin().urls())),
    path('', views.IndexPage().as_view()),
]
