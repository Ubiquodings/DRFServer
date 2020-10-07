from django.urls import path
from . import views

urlpatterns = [
    # /cf/
    path('test/', views.test_api),

    # index_name & action_type 받아서 파싱 후 결과 반환하는 api
    path('es-list/', views.test_es_list_api),

    # index_name & user_id 받아서 {카테고리:점수} 반환하는 api
    path('category-score/', views.get_last50_for_category_score_from_ES),

    path('es-index-list/', views.test_es_get_all_api),

    # 쇼핑몰에 productIdList 하드코딩 반환하는 api
    path('get-product-ids/', views.test_get_productIdList_api),
]
