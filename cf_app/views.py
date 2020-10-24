import collections

import urllib3
import json
import pickle
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
    print('size', size)

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
        # print(action['actionType'])
        if action['actionType'] == 'hover':
            category_score[action['categoryId']] += 1
        elif action['actionType'] == 'click':
            category_score[action['categoryId']] += 3
        elif action['actionType'] == 'cart-create':
            category_score[action['categoryId']] += 5
        elif action['actionType'] == 'order-create':
            category_score[action['categoryId']] += 7

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


@api_view(['GET'])
def get_all_es_data(request):
    """
    elastic search 모든 데이터 가져와서 userCF 연산 적용한다
    """
    index_name = 'ubic_click_action'

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match_all": {
        }}}  # _all
    )["count"]
    print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match_all": {  # _all
                }
            }
        },
        size=10000,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )

    try:
        response = get_pretty_response(response)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    return Response(response
                    , status=status.HTTP_200_OK)


def get_pretty_response(response):
    """
    elastic search data 파싱 작업 함수
    """
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
def test_get_productIdList_api1(request):
    response = [11794, 6079, 9694, 20522, 5607, 8328, 10121, 45417, 11809, 46176, 17745, 18456, 18616, 45552, 2171,
                5424, 2095, 2123, 2000, 6000, 1071, 987, 5968, 1045, 1784, 1016, 2045, 2140]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api2(request):
    response = [2193, 2207, 2223, 2237, 2258, 2286, 2316, 2337, 2362, 2387, 2408, 2443, 2469, 2489, 2515, 2541, 2568,
                2588, 2602, 2620, 2635, 2651, 2680, 2697, 2712, 2733, 2753, 2769, 2789, 2813, 2836, 2852, 2865, 2886,
                2901, 2914, 2935, 2957, 2975, 3005, 3022, 3040, 3058, 3075, 3097, 3115, 3137, 3148, 3166, 3191, 3214,
                3239, 3263, 3285, 3301, 3320, 3339, 3367, 3399, 3421, 3444, 3460, 3480, 3502, ]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api3(request):
    response = [6561, 6578, 6589, 6617, 6636, 6656, 6676, 6708, 6728, 6742, 6762, 6777, 6802, 6819, 6840, 6864, 6882,
                6899, 6916, 6938, 6965, 6985, 7009, 7028, 7044, 7068, 7088, 7110, 7131, 7149, 7170, 7187, 7203, 7219,
                7243, 7268, 7289, 7304, 7325, 7353, 7384, 7410, 7421, 7440, 7459, 7474, 7492, 7508, 7525, 7545, 7575,
                7603, 7619, 7638, 7663, 7685, 7706, 7723, 7735, 7751, 7773, 7795, 7811, ]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api4(request):
    response = [9717, 9743, 9759, 9780, 9803, 9818, 9842, 9859, 9879, 9894, 9914, 9922, 9939, 9950, 9963, 9975, 9991,
                10005, 10018, 10031, 10046, 10059, 10067, 10078, 10090, 10104, 10121, 10136, 10161, 10183, 10199, 10219,
                10242, 10263, 10276, 10300, 10320, 10339, 10352, 10378, 10396, 10412, 10430, 10446, 10458, 10472, 10488,
                10513, 10531, 10552, 10575, 10598, 10620, 10645, 10666, 10683, 10707, ]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api5(request):
    response = [11272, 11287, 11296, 11314, 11338, 11369, 11386, 11406, 11426, 11447, 11467, 11481, 11494, 11510, 11532,
                11559, 11579, 11599, 11617, 11631, 11656, 11677, 11694, 11712, 11729, 11750, 11771, 11794, 11809, 11824,
                11841, 11858, 11876, 11895, 11916, 11938, 11957, 11980, 12006, 12023, 12042, 12068, 12092, 12107, 12121,
                12144, 12162, 12177, 12196, 12215, 12232, 12251, 12268, 12284, ]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api6(request):
    response = [13455, 13473, 13497, 13536, 13561, 13579, 13599, 13618, 13638, 13654, 13674, 13698, 13715, 13732, 13755,
                13770, 13785, 13806, 13827, 13846, 13861, 13883, 13905, 13927, 13953, 13973, 13987, 14005, 14018, 14040,
                14063, 14081, 14102, 14120, 14137, 14150, 14169, 14187, 14203, 14223, 14247, 14266, 14284, 14304, 14322,
                14340, 14361, 14379, 14397, 14412, 14426, 14447, 14465, 14487, ]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_write_pkl_api(request):
    productIdList = [11794, 6079, 9694, 20522, 5607, 8328, 10121, 45417, 11809, 46176, 17745, 18456, 18616, 45552, 2171,
                     5424, 2095, 2123, 2000, 6000, 1071, 987, 5968, 1045, 1784, 1016, 2045, 2140]
    with open('list.pkl', 'wb') as f:
        pickle.dump(productIdList, f)

    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_read_pkl_api(request):
    with open('list.pkl', 'rb') as f:
        data = pickle.load(f)
    print(data)
    return Response({"message": data}, status=status.HTTP_200_OK)
