from django.urls import path
from .views import SkinDiseasePredictionView

urlpatterns = [
    path('', SkinDiseasePredictionView.as_view(), name='predict_skin_disease'),
]

