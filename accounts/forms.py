from django import forms  # Django의 폼 기능을 가져옵니다.
from django.contrib.auth.forms import UserCreationForm  # 기본 회원가입 폼 클래스
from .models import User  # 우리가 정의한 커스텀 유저 모델 불러오기

# 회원가입 폼 정의
class SignupForm(UserCreationForm):  # 기본 UserCreationForm을 상속하여 확장합니다.
    email = forms.EmailField(required=True)  # 이메일 필드를 필수로 받도록 지정
    nickname = forms.CharField(max_length=30)  # 닉네임 필드 추가

    class Meta:
        model = User  # 사용할 모델은 우리가 정의한 User 모델
        fields = ['username', 'password1', 'password2', 'email', 'nickname']  
        # 회원가입 시 입력 받을 필드 목록 (비밀번호 2개는 자동 검증됨)
