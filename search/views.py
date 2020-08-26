import urllib3
import json

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def test_api(request):
    # print(settings.ETRI_API_KEY)  # ok
    # print('request.query_params:', request.query_params.get('key')) ok
    # self.request.query_params.get('longitude')

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"

    accessKey = settings.ETRI_API_KEY  # "YOUR_ACCESS_KEY"
    analysisCode = "morp"
    # analysisCode = "ner"
    text = request.query_params.get('text')  # "YOUR_SENTENCE" # /?text=sisi
    if text == '':
        print('\nError\nproductInfo :\n', text)
        return Response({"result": {}}, status=status.HTTP_400_BAD_REQUEST)

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    print("[responseCode] " + str(response.status))
    # Decode UTF-8 bytes to Unicode, and convert single quotes
    response = response.data.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list
    response = json.loads(response)

    # response = response["message"]
    try:
        response = response["return_object"]["sentence"][0]["morp"]  # list
    except:
        print('\nError\nproductInfo :\n', text, '\nresponse :\n', response)
        return Response({"result": {}}, status=status.HTTP_404_NOT_FOUND)

    print('\nproductInfo :\n', text, '\nresponse :\n', response)
    print('response-type: ', type(response))

    for i,item in enumerate(response):
        if item['type'] in ['ETM','SS','SP']:
            print('index: ',i)
            # 제거
            del response[i]
            # response.remove(i)

    return Response({"result": response}, status=status.HTTP_200_OK)
