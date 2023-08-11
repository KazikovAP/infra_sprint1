from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Achievement(models.Model):
    """Класс для добавления достижений кота."""
    name = models.CharField(max_length=64)
    verbose_name = 'Достижение'

    def __str__(self):
        return self.name


class Cat(models.Model):
    """Класс для описания кота."""
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
        )
    achievements = models.ManyToManyField(
	Achievement, through='AchievementCat')
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
        )
    verbose_name = 'Кот'

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    """Класс, связывающий конкретные достижения с конкретным котом"""
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    verbose_name = 'Достижение кота'

    def __str__(self):
        return f'{self.achievement} {self.cat}'
