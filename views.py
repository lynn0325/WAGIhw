from django.shortcuts import render, redirect, get_object_or_404
# 템플릿 렌더링, 페이지 이동, 객체 없을 경우 404 처리

from django.contrib.auth.decorators import login_required
# 로그인하지 않은 사용자가 접근 못 하도록 제한

from .forms import PostForm  # 게시글 작성/수정 폼
from .models import Post, PostImage, Comment  # 모델들 임포트

@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)  # 글 내용만 처리. 이미지는 아래에서 처리
        if form.is_valid():
            post = form.save(commit=False)  # author를 추가해야 하므로 일단 저장 보류
            post.author = request.user  # 작성자 정보 추가
            post.save()  # 실제 DB에 저장

            # 여러 이미지 저장
            files = request.FILES.getlist('images')  # input name="images"로부터 여러 파일을 가져옴
            print("DEBUG: 이미지 수 =", len(files))  # 디버깅용 출력
            for file in files:
                PostImage.objects.create(post=post, image=file)  # 이미지 하나씩 저장

            return redirect('list')  # 작성 완료 후 목록 페이지로 이동
    else:
        form = PostForm()  # GET 요청이면 빈 폼 보여줌

    return render(request, 'write.html', {'form': form})  # 템플릿에 폼 전달


def list(request):
    query = request.GET.get('q')  # 검색창에서 입력한 값(q)을 가져옴

    if query:
        posts = Post.objects.filter(title__icontains=query)
        # 제목에 query가 포함된 게시글들만 필터링 (대소문자 구분 X)
    else:
        posts = Post.objects.all()

    return render(request, 'list.html', {
        'posts': posts,
        'query': query  # 검색창에 입력값 유지용
    })

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)  # 특정 게시글 불러오기 (없으면 404)
    return render(request, 'detail.html', {'post': post})  # 템플릿에 게시글 전달

@login_required
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('list')  # 본인 글이 아니면 수정 불가

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # 기존 데이터와 연결된 폼
        if form.is_valid():
            form.save()  # 제목/내용 수정

            # 새 이미지 추가
            for img in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=img)

            # 삭제할 이미지 id 리스트 가져와 삭제
            delete_ids = request.POST.getlist('delete_images')
            PostImage.objects.filter(id__in=delete_ids, post=post).delete()

            return redirect('detail', post_id=post.id)
    else:
        form = PostForm(instance=post)  # 기존 내용이 담긴 폼 생성

    return render(request, 'update.html', {'form': form, 'post': post})  # 수정 폼 렌더링

@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('list')  # 본인이 아닌 경우 삭제 금지

    if request.method == 'POST':
        post.delete()  # 삭제 실행
        return redirect('list')  # 목록 페이지로 이동

    return render(request, 'delete_confirm.html', {'post': post})  # 삭제 확인 페이지

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')  # 댓글 내용 받기
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            # 댓글 저장

    return redirect('detail', post_id=post.id)  # 다시 해당 글로 이동

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)  # 좋아요 취소
    else:
        post.likes.add(user)  # 좋아요 추가

    return redirect('detail', post_id=post.id)  # 다시 상세페이지로 이동
