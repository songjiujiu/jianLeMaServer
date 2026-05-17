from django.conf import settings
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    """微信用户资料表。

    Django 自带 User 表负责登录身份，这个表额外保存微信 openid、昵称、头像等信息。
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        # 用户被删除时，对应的资料也一起删除。
        on_delete=models.CASCADE,
        # 可以通过 user.profile 反向拿到这条用户资料。
        related_name="profile",
        verbose_name="用户",
    )
    # openid 是微信小程序用户的唯一标识，用它判断是不是同一个微信用户。
    openid = models.CharField("微信 OpenID", max_length=128, unique=True)
    # unionid 不是所有小程序都会返回，所以允许为空字符串。
    unionid = models.CharField("微信 UnionID", max_length=128, blank=True)
    nickname = models.CharField("昵称", max_length=64, blank=True)
    avatar_url = models.URLField("头像", blank=True)
    # auto_now_add：第一次创建时自动填入时间。
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    # auto_now：每次保存时自动更新时间。
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        # verbose_name 用于 Django 后台显示中文名称。
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        # 后台列表里显示昵称；没有昵称时显示 openid。
        return self.nickname or self.openid


class Goal(models.Model):
    """用户创建的目标，例如“每天背单词”或“每天运动”。"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # 一个用户可以有多个目标；删除用户时，目标也一起删除。
        on_delete=models.CASCADE,
        # 可以通过 user.goals.all() 查询这个用户的全部目标。
        related_name="goals",
        verbose_name="用户",
    )
    title = models.CharField("目标名称", max_length=100)
    description = models.TextField("目标描述", blank=True)
    # 软开关：目标不想继续用了，可以改成 False，而不是直接删除数据。
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "目标"
        verbose_name_plural = "目标"
        # 默认按创建时间倒序排列，最新目标排在前面。
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class DailyCheckIn(models.Model):
    """每日打卡记录表。

    每打一次卡，就会在这里保存一条记录。
    """

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
        # 允许没有目标的默认打卡。
        null=True,
        blank=True,
    )
    # 默认使用当前本地日期，这里会跟随 settings.py 里的 TIME_ZONE。
    check_date = models.DateField("打卡日期", default=timezone.localdate)
    note = models.TextField("打卡备注", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "每日打卡"
        verbose_name_plural = "每日打卡"
        ordering = ["-check_date", "-created_at"]
        constraints = [
            # 限制同一个用户、同一个目标、同一天只能打卡一次。
            models.UniqueConstraint(
                fields=["user", "goal", "check_date"],
                name="unique_user_goal_check_date",
            ),
        ]

    def __str__(self):
        # 没有关联目标时，用“默认目标”方便后台阅读。
        goal_name = self.goal.title if self.goal else "默认目标"
        return f"{self.user} - {goal_name} - {self.check_date}"


class CheckInStreak(models.Model):
    """连续打卡统计表。

    这张表只保存统计结果，真正的每次打卡记录在 DailyCheckIn 表里。
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="check_in_streak",
        verbose_name="用户",
    )
    # 当前连续打卡天数，例如连续 3 天打卡就是 3。
    current_streak = models.PositiveIntegerField("当前连续打卡天数", default=0)
    # 历史最长连续打卡天数。
    longest_streak = models.PositiveIntegerField("最长连续打卡天数", default=0)
    # 最后一次成功新增打卡记录的日期。
    last_check_date = models.DateField("最后打卡日期", null=True, blank=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "连续打卡"
        verbose_name_plural = "连续打卡"

    def __str__(self):
        return f"{self.user} - {self.current_streak} 天"
