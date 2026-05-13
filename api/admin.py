from django.contrib import admin

from .models import CheckInStreak, DailyCheckIn, Goal, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "openid", "nickname", "created_at", "updated_at")
    search_fields = ("user__username", "openid", "nickname")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_active", "created_at", "updated_at")
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
