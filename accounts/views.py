from django.shortcuts import render, redirect  # 템플릿 렌더링 및 페이지 이동을 위한 함수들
from .forms import SignupForm  # 위에서 만든 회원가입 폼 불러오기

# 회원가입 뷰 함수 정의
def signup(request):
    if request.method == 'POST':  # 폼 제출된 경우 (POST 요청)
        form = SignupForm(request.POST)  # 사용자가 작성한 데이터를 폼에 넣음
        if form.is_valid():  # 폼의 유효성 검사 (비밀번호 확인, 중복 검사 등 자동으로 처리됨)
            form.save()  # 유효하면 DB에 사용자 저장
            return redirect('login')  # 회원가입 완료 후 로그인 페이지로 이동
    else:  # 처음 접속했거나, GET 요청일 때
        form = SignupForm()  # 비어 있는 폼 생성
    return render(request, 'accounts/signup.html', {'form': form})  
    # 폼을 템플릿에 전달하여 화면에 출력
