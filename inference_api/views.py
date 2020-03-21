from keras.applications.resnet50 import preprocess_input
from keras_preprocessing.image import ImageDataGenerator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from inference_api.serializers import PredictionSerializer
from landmark_recognition.settings import MODEL


class PredictionView(APIView):

    def post(self, request):
        prediction_serializer = PredictionSerializer(data=request.data)

        if prediction_serializer.is_valid():
            prediction_serializer.save()

            test_img_gen = ImageDataGenerator(preprocessing_function=preprocess_input)
            test_data_gen = test_img_gen.flow_from_directory(directory='media',
                                                             target_size=(192, 192),
                                                             color_mode='rgb')

            acc = MODEL.predict_generator(generator=test_data_gen,
                                          steps=1)

            return Response(data=prediction_serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(data=prediction_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
