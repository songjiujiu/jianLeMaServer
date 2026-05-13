from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CheckInStreak, DailyCheckIn, Goal, UserProfile


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok", "service": "jianlema-server"})


@api_view(["POST"])
@permission_classes([AllowAny])
def wechat_login(request):
    code = request.data.get("code")
    nickname = request.data.get("nickname", "")
    avatar_url = request.data.get("avatar_url", "")

    if not code:
        return Response({"detail": "code is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not settings.WECHAT_APPID or not settings.WECHAT_SECRET:
        return Response(
            {"detail": "WECHAT_APPID or WECHAT_SECRET is not configured"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    response = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session",
        params={
            "appid": settings.WECHAT_APPID,
            "secret": settings.WECHAT_SECRET,
            "js_code": code,
            "grant_type": "authorization_code",
        },
        timeout=5,
    )
    session_data = response.json()

    if "errcode" in session_data and session_data.get("errcode") != 0:
        return Response(
            {
                "detail": "wechat login failed",
                "wechat_error": session_data,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    openid = session_data.get("openid")
    if not openid:
        return Response(
            {"detail": "wechat response missing openid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    User = get_user_model()
    with transaction.atomic():
        profile = UserProfile.objects.select_related("user").filter(openid=openid).first()
        if profile:
            user = profile.user
        else:
            user = User.objects.create_user(username=f"wx_{openid}")
            profile = UserProfile.objects.create(user=user, openid=openid)

        profile.unionid = session_data.get("unionid", profile.unionid)
        if nickname:
            profile.nickname = nickname
        if avatar_url:
            profile.avatar_url = avatar_url
        profile.save()

        CheckInStreak.objects.get_or_create(user=user)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": profile.nickname,
                "avatar_url": profile.avatar_url,
                "openid": profile.openid,
            },
        }
    )


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def today_check_in(request):
    today = timezone.localdate()

    if request.method == "GET":
        check_ins = DailyCheckIn.objects.filter(user=request.user, check_date=today)
        return Response(
            {
                "date": today,
                "checked": check_ins.exists(),
                "items": [
                    {
                        "id": item.id,
                        "goal_id": item.goal_id,
                        "goal_title": item.goal.title if item.goal else "",
                        "note": item.note,
                        "created_at": item.created_at,
                    }
                    for item in check_ins.select_related("goal")
                ],
            }
        )

    goal_id = request.data.get("goal_id")
    note = request.data.get("note", "")
    goal = None

    if goal_id:
        goal = Goal.objects.filter(id=goal_id, user=request.user, is_active=True).first()
        if not goal:
            return Response({"detail": "goal not found"}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        check_in, created = DailyCheckIn.objects.get_or_create(
            user=request.user,
            goal=goal,
            check_date=today,
            defaults={"note": note},
        )
        if not created and note:
            check_in.note = note
            check_in.save(update_fields=["note", "updated_at"])

        streak, _ = CheckInStreak.objects.select_for_update().get_or_create(user=request.user)
        if created:
            yesterday = today - timedelta(days=1)
            if streak.last_check_date == yesterday:
                streak.current_streak += 1
            elif streak.last_check_date != today:
                streak.current_streak = 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_check_date = today
            streak.save()

    return Response(
        {
            "id": check_in.id,
            "created": created,
            "date": check_in.check_date,
            "goal_id": check_in.goal_id,
            "note": check_in.note,
            "streak": {
                "current": streak.current_streak,
                "longest": streak.longest_streak,
                "last_check_date": streak.last_check_date,
            },
        },
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )
