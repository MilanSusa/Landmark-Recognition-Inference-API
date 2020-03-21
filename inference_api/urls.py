from django.urls import path
from inference_api.views import PredictionView

urlpatterns = [
    path('', PredictionView.as_view()),
]
