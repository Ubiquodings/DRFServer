import collections

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
    """
    http://127.0.0.1:8000/cf/es-list/?index_name=ubic_click_action&action_type=order
    """
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

    result = get_pretty_response(response)

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


@api_view(['GET'])  # userId 가 필요하네 !
def get_last50_for_category_score_from_ES(request):
    """
        엘라스틱서치에서 최근 50개 행동 가져와서 category_score 로 변경하는 함수
        http://127.0.0.1:8000/cf/category-score/?index_name=ubic_click_action&user_id=47161
    """
    index_name = request.query_params.get('index_name')
    user_id = request.query_params.get('user_id')

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match": {
            "userId": user_id
        }}}  # _all
    )["count"]
    print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match": {  # _all
                    "userId": user_id
                }
            }
        },
        size=size,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )
    # print(response)

    # category_score 계산 로직
    try:
        response = get_pretty_response(response)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    category_score = collections.defaultdict(int)
    for action in response:  # 
        category_score[action['categoryId']] += 1

    # 근데 사실 필요한건 가장 점수가 높은 카테고리 값!
    def return_value_from_dict(x):
        return x[1]

    # print('정렬전 ', category_score)
    result = sorted(category_score.items(), key=return_value_from_dict, reverse=True)
    print('정렬후 ', result)
    # result[0][0] # category:score 니까 [0]

    # result = []
    return Response({
        'maxScoreCategory': result[0][0]
    }, status=status.HTTP_200_OK)


def get_pretty_response(response):
    response = response['hits']['hits']  # list : filter_path
    # df = pd.DataFrame(response)

    # response 루프돌면서 _source 의 값들의 배열로 만들거야
    result = []
    for row in response:
        row = row['_source']
        result.append(row)

    return result


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

    return Response({"message": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api(request):
    response = [11794, 6079, 9694, 20522, 5607, 8328, 10121, 45417, 11809, 46176, 17745, 18456, 18616, 45552, 2171,
                5424, 2095, 2123, 2000, 6000, 1071, 987, 5968, 1045, 1784, 1016, 2045, 2140]
    return Response({"productIdList":response}, status=status.HTTP_200_OK)
