from django.contrib import admin

from .models import CheckInStreak, DailyCheckIn, Goal, UserProfile


# 下面这些类用于配置 Django 后台中每张表的显示方式。
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 列表页显示哪些字段。
    list_display = ("user", "openid", "nickname", "created_at", "updated_at")
    # 后台搜索框可以搜索哪些字段。
    search_fields = ("user__username", "openid", "nickname")
    # 只读字段：后台可以看到，但不能手动修改。
    readonly_fields = ("created_at", "updated_at")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_active", "created_at", "updated_at")
    # 右侧筛选器，可以按启用状态、创建时间过滤。
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ("user", "goal", "check_date", "created_at")
    list_filter = ("check_date", "created_at")
    search_fields = ("user__username", "goal__title", "note")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CheckInStreak)
class CheckInStreakAdmin(admin.ModelAdmin):
    list_display = ("user", "current_streak", "longest_streak", "last_check_date", "updated_at")
    search_fields = ("user__username",)
    readonly_fields = ("updated_at",)
