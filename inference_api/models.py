from django.db import models
import os
import datetime


def rename_image(path):
    def wrapper(instance, filename):
        filename = f'{datetime.datetime.now().today()}_{filename}'
        return os.path.join(path, filename)
    return wrapper


class Prediction(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to=rename_image('upload/images/'))
    landmark = models.CharField(blank=True, null=True, max_length=255)
    probability = models.FloatField(blank=True, null=True)
