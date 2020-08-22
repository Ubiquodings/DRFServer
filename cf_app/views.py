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
    # print('start api') # ok
    # client = Elasticsearch()
    # print(client) # ok
    #
    # # s = Search(using=client)
    # s = Search().using(client).query("match", title="python")
    # print(s) # ok
    # response = s.execute()
    # print(response) # xx 연결을 거부했다 ?
    # for hit in s:
    #     print(hit.title)
    # print(s.to_dict())

    # ver2
    client = Elasticsearch(settings.ES_SECRET_KEY)

    response = client.search(
        index="ubic_click_action",
        body={
            "query": {
                "match_all": {}
                # "filtered": {
                #     "query": {
                #         "match_all": {}
                #     },
                #     # "filter": {"term": {"category": "search"}}
                # }
            },
            # "aggs": {
            #     "per_tag": {
            #         "terms": {"field": "tags"},
            #         "aggs": {
            #             "max_lines": {"max": {"field": "lines"}}
            #         }
            #     }
            # }
        }
    )
    print(response)

    return Response({"message": response}, status=status.HTTP_200_OK)


# def search_test():
