from rest_framework.response import Response
from rest_framework.decorators import api_view
from PIL import Image
import io
import base64
from api.rainwater import rainfall

from api.rooftop_detection import get_solar_data, get_rainwater_data
import cv2


def convert_mat_to_base64(image: cv2.Mat):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image_byte_array = io.BytesIO()
    pil_image.save(image_byte_array, format='JPEG')
    image_base64 = base64.b64encode(image_byte_array.getvalue()).decode('utf-8')

    return image_base64


@api_view(['POST'])
def getRainwaterData(request):
    image_data = request.FILES.get('image')
    lat, long = request.data.get('lat'), request.data.get('long')

    if not image_data:
        return Response({"error": "No image data sent!"}, status=400)

    img = Image.open(image_data)

    rainwater_data = get_rainwater_data(img)

    rain=rainfall(lat,long,rainwater_data["roof_area"])
    # Prepare data to be sent in the response
    data = {
        "area": rainwater_data["roof_area"],
        "image": convert_mat_to_base64(rainwater_data["threshold_img"]),
        'rain_water_harvested':rain[0],
        'litres_consumed':rain[1],
        'bill_amount':rain[2],
        'monthly_saving': rain[3],
    }

    return Response(data) 


@api_view(['POST'])
def getSolarData(request):
    image_data = request.FILES.get('image')

    if not image_data:
        return Response({"error": "No image data sent!"}, status=400)

    img = Image.open(image_data)

    solar_data = get_solar_data(img)

    # Prepare data to be sent in the response
    data = {
        "area": solar_data["area_of_panels"],
        "image": convert_mat_to_base64(solar_data["image_with_panels"])
    }

    return Response(data)

@api_view(['GET'])
def ping(request):
    return Response("pong", status=200)