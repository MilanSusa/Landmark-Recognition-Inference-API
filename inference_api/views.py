from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from inference_api.serializers import PredictionSerializer


class PredictionView(APIView):

    def post(self, request):
        prediction_serializer = PredictionSerializer(data=request.data)

        if prediction_serializer.is_valid():
            prediction_serializer.save()
            return Response(data=prediction_serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(data=prediction_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
