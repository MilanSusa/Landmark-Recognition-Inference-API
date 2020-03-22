# Landmark Recognition Inference API

Landmark recognition inference API provides user the option of performing inference on a given image via specific API 
endpoint in order to recognize which famous or infamous landmark is found in the picture. 

## Running locally

After setting up virtual environment, run the following command to install required dependencies:

    pip install -r requirements.txt

Generate Django secret key via https://djecrety.ir/ and set environment variable:

    LANDMARK_RECOGNITION_DJANGO_SECRET_KEY

to contain the generated key.

Download dataset from [here][1] and place it in the `/datasets` directory.

Download model from [here][2] and place it in the `/pretrained_models` directory.

[1]: https://s3.amazonaws.com/google-landmark/metadata/train.csv
[2]: https://www.kaggle.com/mayukh18/resnet50-0092#resnet50.model

Run the following command to apply init migrations:

    python manage.py migrate

To start a web server for the application, run:

    python manage.py runserver 
    
By default, application server will start on port 8000 so you can try the API out by running:

    curl -X POST 'http://localhost:8000/inference/' \
    -H 'Content-Type: multipart/form-data' \
    -F 'image=@{path_to_your_image}'

while replacing `{path_to_your_image}` with the path of the image you want to perform inference on.

## Example

Lets test out the API by providing the following image of Golden Gate Bridge:

![](images/test-image.jpg)

By hitting the API endpoint we get the following JSON response:

    {
        "id": 1,
        "image": "/media/upload/images/2020-03-22_153928.659642_test-image.jpg",
        "landmark": "Golden Gate Bridge",
        "probability": 0.7794782519340515
    }

## License

Licensed under the [MIT License](LICENSE).
