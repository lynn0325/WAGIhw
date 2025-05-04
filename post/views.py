from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
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
            return redirect('detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'write.html', {'form': form})

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
