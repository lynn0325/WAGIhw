from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)           # 이메일 중복 방지
    nickname = models.CharField(max_length=30, unique=True)  # 닉네임 필드 추가

    def __str__(self):
        return self.username
