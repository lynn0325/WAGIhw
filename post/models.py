from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    # 좋아요를 누른 사용자들을 저장하는 ManyToMany 필드입니다.
    # related_name='liked_posts'를 설정하면 user.liked_posts.all()로 내가 좋아요 누른 게시글을 조회할 수 있습니다.
    # blank=True는 좋아요가 없는 경우도 허용합니다.

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  
    # 이 댓글이 달린 게시글(Post)을 나타냅니다.
    # on_delete=models.CASCADE는 해당 게시글이 삭제되면 댓글도 함께 삭제됨을 의미합니다.
    # related_name='comments'로 post.comments.all()로 댓글을 조회할 수 있게 됩니다.

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 댓글 작성자 (로그인한 사용자). 유저가 탈퇴하면 댓글도 같이 삭제됩니다.

    content = models.TextField()
    # 댓글 본문 내용입니다.

    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글 작성 시간이 자동으로 저장됩니다.

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'
    # 댓글 객체를 문자열로 출력할 때 작성자와 내용 일부를 보여줍니다.