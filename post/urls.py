from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from post.views import write, list, detail  # views에서 필요한 뷰 임포트 추가


urlpatterns = [
    path('write/', write, name='write'),  # 글 작성 페이지
    path('', list, name='list'),          # 글 목록 페이지
    path('post/<int:post_id>/', detail, name='detail'),  # 글 상세 페이지
    path('accounts/', include('accounts.urls')),  # ✅ 꼭 있어야 함
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete, name='delete'),

]

# ✅ 개발 환경에서 media 경로 열기 (이미지 보기 가능하게)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
