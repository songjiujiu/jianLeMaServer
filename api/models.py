from django.conf import settings
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )
    openid = models.CharField("微信 OpenID", max_length=128, unique=True)
    unionid = models.CharField("微信 UnionID", max_length=128, blank=True)
    nickname = models.CharField("昵称", max_length=64, blank=True)
    avatar_url = models.URLField("头像", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return self.nickname or self.openid


class Goal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals",
        verbose_name="用户",
    )
    title = models.CharField("目标名称", max_length=100)
    description = models.TextField("目标描述", blank=True)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "目标"
        verbose_name_plural = "目标"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DailyCheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_check_ins",
        verbose_name="用户",
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="check_ins",
        verbose_name="目标",
        null=True,
        blank=True,
    )
    check_date = models.DateField("打卡日期", default=timezone.localdate)
    note = models.TextField("打卡备注", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "每日打卡"
        verbose_name_plural = "每日打卡"
        ordering = ["-check_date", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "goal", "check_date"],
                name="unique_user_goal_check_date",
            ),
        ]

    def __str__(self):
        goal_name = self.goal.title if self.goal else "默认目标"
        return f"{self.user} - {goal_name} - {self.check_date}"


class CheckInStreak(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="check_in_streak",
        verbose_name="用户",
    )
    current_streak = models.PositiveIntegerField("当前连续打卡天数", default=0)
    longest_streak = models.PositiveIntegerField("最长连续打卡天数", default=0)
    last_check_date = models.DateField("最后打卡日期", null=True, blank=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "连续打卡"
        verbose_name_plural = "连续打卡"

    def __str__(self):
        return f"{self.user} - {self.current_streak} 天"
