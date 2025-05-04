from django.urls import path  # URL 패턴을 정의하기 위한 함수
from . import views  # 현재 디렉토리의 views.py 가져오기

# accounts 앱 전용 URL 패턴 목록
urlpatterns = [
    path('signup/', views.signup, name='signup'),  # '/accounts/signup/' 경로 요청 시 signup 뷰 호출
]
