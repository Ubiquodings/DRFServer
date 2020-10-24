from django.urls import path
from . import views

urlpatterns = [
    # /cf/
    path('test/', views.test_api),

    # index_name & action_type 받아서 파싱 후 결과 반환하는 api
    path('es-list/', views.test_es_list_api),

    # es 모든 데이터 가져오기 : user_click_action
    path('es-get-all-data/', views.get_all_es_data),

    # index_name & user_id 받아서 {카테고리:점수} 반환하는 api
    path('category-score/', views.get_last50_for_category_score_from_ES),

    path('es-index-list/', views.test_es_get_all_api),

    # 쇼핑몰에 productIdList 하드코딩 반환하는 api
    path('get-product-ids/', views.test_get_productIdList_api),

    # test : pkl 저장하는 api
    path('save-pkl/', views.test_write_pkl_api),
    # test : pkl 서빙하는 api
    path('get-pkl/', views.test_read_pkl_api),
]
