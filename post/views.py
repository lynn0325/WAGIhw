from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Comment  # Comment 모델 임포트
# views.py 상단에 추가

# Create your views here.
from .models import Post, PostImage



@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)  # ✅ request.FILES 제거
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # ✅ 여러 이미지 저장
            files = request.FILES.getlist('images')
            print("DEBUG: 이미지 수 =", len(files))
            for file in files:
                PostImage.objects.create(post=post, image=file)

            return redirect('list')
    else:
        form = PostForm()
    return render(request, 'write.html', {'form': form})

def list(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)  
    return render(request, 'detail.html', {'post': post})  #form.py 장고 게시물 form으로 받는거 어쩌구 +게시글 이미지 추가

@login_required
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # ✅ 본인이 쓴 글이 아닐 경우 접근 차단
    if post.author != request.user:
        return redirect('list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # ✅ 새로 추가된 이미지 저장
            for img in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=img)

            # ✅ 삭제 체크된 이미지 삭제
            delete_ids = request.POST.getlist('delete_images')
            PostImage.objects.filter(id__in=delete_ids, post=post).delete()

            return redirect('detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'update.html', {'form': form, 'post': post,})

@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # ✅ 작성자만 삭제 가능
    if post.author != request.user:
        return redirect('list')

    if request.method == 'POST':
        post.delete()
        return redirect('list')

    # 삭제 확인 페이지로 렌더링
    return render(request, 'delete_confirm.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # URL로 전달된 post_id를 사용해 해당 게시글을 가져옵니다.
    # 없으면 404 에러 반환

    if request.method == 'POST':
        content = request.POST.get('content')
        # 댓글 입력값(content)을 POST 요청에서 가져옵니다.

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
        # 댓글을 DB에 저장합니다. 작성자는 현재 로그인한 사용자입니다.

    return redirect('detail', post_id=post.id)
    # 댓글을 작성한 후 다시 해당 게시글 상세 페이지로 리다이렉트합니다.


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)  # 이미 좋아요한 경우 취소
    else:
        post.likes.add(user)     # 좋아요 추가

    return redirect('detail', post_id=post.id)  # 다시 상세 페이지로 이동
