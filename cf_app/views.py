import urllib3
import json
import pandas as pd

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from config import settings


@api_view(['GET'])
def test_api(request):
    return Response({"message": "ok."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_es_list_api(request):
    index_name = request.query_params.get('index_name')
    actionType = request.query_params.get('action_type')

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match": {
            "actionType": actionType
        }}}  # _all
    )["count"]
    print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match": {  # _all
                    "actionType": actionType
                }
            }
        },
        size=size,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )
    # print(response)
    response = response['hits']['hits']  # list : filter_path
    # df = pd.DataFrame(response)

    # response 루프돌면서 _source 의 값들의 배열로 만들거야
    result = []
    for row in response:
        row = row['_source']
        result.append(row)

    ''' 결과 배열의 원소 모양 : 자바에서 바로 클래스 배열로 받으면 된다
        {
            "now": "2020-09-10T16:53:51.114428",
            "userId": "47161",
            "productId": 20522,
            "categoryId": 18,
            "actionType": "order"
        },
    '''
    return Response(result, status=status.HTTP_200_OK)


# def search_test():
@api_view(['GET'])
def test_es_get_all_api(request):
    http = urllib3.PoolManager()

    index_name = request.query_params.get('index_name')
    ES_INDEX_SIZE_URL = settings.ES_SECRET_KEY + f'/_cat/count/{index_name}'  # 실패
    print(ES_INDEX_SIZE_URL)
    response = http.request(
        "GET",
        ES_INDEX_SIZE_URL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body={}
    )
    print("[responseCode] " + str(response.status))
    # Decode UTF-8 bytes to Unicode, and convert single quotes
    response = response.data.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list
    response = json.loads(response)
    print("[response] " + str(response))

    # ES_INDEX_URL = settings.ES_SECRET_KEY + f'/{index_name}/_search/?size={size}'
    #
    # response = http.request(
    #     "GET",
    #     ES_INDEX_URL,
    #     headers={"Content-Type": "application/json; charset=UTF-8"},
    #     body={}  # json.dumps(requestJson)
    # )
    # print("[responseCode] " + str(response.status))
    # # Decode UTF-8 bytes to Unicode, and convert single quotes
    # response = response.data.decode('utf8').replace("'", '"')
    # # Load the JSON to a Python list
    # response = json.loads(response)

    return Response({"message": response}, status=status.HTTP_200_OK)
