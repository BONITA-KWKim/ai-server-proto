# imports the Google Cloud client library
from google.cloud import vision
# from google.cloud.vision import types


def get_google_vision_response(photo):
    print("[DEB] get google vision response")
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    content = photo['eye_photo'].read()

    response = client.annotate_image({
        "image": {
            "content": content
        },
        "features": [
            {
                "type": vision.enums.Feature.Type.SAFE_SEARCH_DETECTION
            },
            {
                "type": vision.enums.Feature.Type.LABEL_DETECTION
            },
            {
                "type": vision.enums.Feature.Type.WEB_DETECTION
            }
        ],
    })

    return response
