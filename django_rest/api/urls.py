from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.getStudents),
    path('add/', views.addStudent),
    path('update/<str:pk>', views.updateStudent),
    path('delete/<str:pk>', views.deleteStudent),
    path('patch/<str:pk>', views.patchStudent),
]