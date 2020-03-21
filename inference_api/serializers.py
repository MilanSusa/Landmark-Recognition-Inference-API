from rest_framework import serializers
from inference_api.models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"
