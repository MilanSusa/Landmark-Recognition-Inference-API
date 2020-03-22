import os
import shutil
import numpy as np
import re
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from keras.applications.resnet50 import preprocess_input
from keras_preprocessing.image import ImageDataGenerator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from inference_api.serializers import PredictionSerializer
from landmark_recognition.settings import MODEL, LANDMARK_ID_DF, TRAIN_DF, BASE_DIR


class PredictionView(APIView):

    @swagger_auto_schema(
        responses={
            201: openapi.Response('Prediction', PredictionSerializer)
        }
    )
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

            index_of_maximum = np.argmax(acc[len(acc) - 1])
            landmark_id = LANDMARK_ID_DF.iloc[index_of_maximum]['landmark']
            landmark_urls = TRAIN_DF.loc[TRAIN_DF['landmark_id'] == landmark_id]['url']

            annotated_landmark_names = {}
            for url in landmark_urls:
                landmark_name_with_jpg_extension = url.rpartition('/')[2]
                landmark_name_without_jpg_extension = landmark_name_with_jpg_extension.split('.')[0]
                landmark_name_with_numbers = ' '.join(landmark_name_without_jpg_extension.split('_')[0:-1])
                landmark_name_with_excess_spaces = re.sub('%[0-9a-zA-Z]+', ' ', landmark_name_with_numbers)
                landmark_name = re.sub(' +', ' ', landmark_name_with_excess_spaces)

                if landmark_name in annotated_landmark_names:
                    annotated_landmark_names[landmark_name] += 1
                else:
                    annotated_landmark_names[landmark_name] = 1

            most_probable_landmark = max(annotated_landmark_names, key=lambda k: annotated_landmark_names[k])
            probability = np.max(acc[len(acc) - 1])

            prediction_serializer.validated_data['landmark'] = most_probable_landmark
            prediction_serializer.validated_data['probability'] = probability
            prediction_serializer.save()

            folder_rel_dir = 'media' + os.path.sep + 'upload' + os.path.sep + 'images' + os.path.sep
            folder_abs_dir = os.path.join(BASE_DIR, folder_rel_dir)

            for filename in os.listdir(folder_abs_dir):
                file_path = os.path.join(folder_abs_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}: {e}')

            return Response(data=prediction_serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(data=prediction_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
