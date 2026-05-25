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
    """健康检查接口。

    不需要登录，用来确认后端服务是否正常启动。
    """

    return Response({"status": "ok", "service": "jianlema-server"})
@api_view(["GET"])
@permission_classes([AllowAny])
def health_goals(requests):
    name = requests.query_params.get("name", "")
    age = requests.query_params.get("age", "")
    return  Response({"status": "ok", "service": {name:name,age:age}})
@api_view(["POST"])
@permission_classes([AllowAny])
def create_health_goal(request):
    name = request.data.get("name", "")
    age = request.data.get("age", "")
    print(
        "============================================="
    )
    return Response({
        "status": "ok",
        "message": "post received",
        "data": {
            "name": name,
            "age": age,
        }
    })
@api_view(["POST"])
@permission_classes([AllowAny])
def dev_login(request):
    if not settings.DEBUG:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    username = request.data.get("username", "dev_user")
    nickname = request.data.get("nickname", "开发测试用户")

    User = get_user_model()
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={"openid": f"dev_{username}"},
        )
        profile.nickname = nickname
        profile.save(update_fields=["nickname", "updated_at"])
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
                "openid": profile.openid,
            },
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def wechat_login(request):
    """微信小程序登录接口。

    前端把微信 wx.login() 得到的 code 发过来，后端拿 code 去微信服务器换 openid，
    然后创建或更新本地用户，并返回 JWT token 给前端。
    """

    # code 是微信临时登录凭证，必须由前端传入。
    code = request.data.get("code")
    nickname = request.data.get("nickname", "")
    avatar_url = request.data.get("avatar_url", "")

    if not code:
        return Response({"detail": "code is required"}, status=status.HTTP_400_BAD_REQUEST)

    # 没配置微信 AppID / Secret 时，不能真正调用微信登录。
    if not settings.WECHAT_APPID or not settings.WECHAT_SECRET:
        return Response(
            {"detail": "WECHAT_APPID or WECHAT_SECRET is not configured"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # 调用微信官方接口：用 code 换取 openid / unionid 等登录信息。
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

    # 微信接口返回 errcode 时，说明 code 无效、配置错误或微信侧拒绝了请求。
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
        # 没有 openid 就无法识别微信用户，所以直接返回错误。
        return Response(
            {"detail": "wechat response missing openid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    User = get_user_model()
    # transaction.atomic() 表示下面的数据库操作要么全部成功，要么全部回滚。
    with transaction.atomic():
        # 先用 openid 查是否已经登录过。
        profile = UserProfile.objects.select_related("user").filter(openid=openid).first()
        if profile:
            user = profile.user
        else:
            # 第一次登录：创建 Django 用户，再创建微信资料。
            user = User.objects.create_user(username=f"wx_{openid}")
            profile = UserProfile.objects.create(user=user, openid=openid)

        # 每次登录时顺便更新微信资料，前端没传的字段就保持旧值。
        profile.unionid = session_data.get("unionid", profile.unionid)
        if nickname:
            profile.nickname = nickname
        if avatar_url:
            profile.avatar_url = avatar_url
        profile.save()

        CheckInStreak.objects.get_or_create(user=user)

    # 生成 JWT：access 用来访问接口，refresh 用来刷新 access。
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
    """今日打卡接口。

    GET：查询今天是否打过卡。
    POST：给今天新增一次打卡，并更新连续打卡天数。
    """

    # timezone.localdate() 会使用 settings.py 中配置的 Asia/Shanghai 时区。
    today = timezone.localdate()

    if request.method == "GET":
        # 查当前登录用户今天的所有打卡记录。
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
        # 只能给自己的、启用中的目标打卡，避免操作别人的数据。
        goal = Goal.objects.filter(id=goal_id, user=request.user, is_active=True).first()
        if not goal:
            return Response({"detail": "goal not found"}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        # get_or_create：今天同一个目标没有打卡就创建；已经打过就返回旧记录。
        check_in, created = DailyCheckIn.objects.get_or_create(
            user=request.user,
            goal=goal,
            check_date=today,
            defaults={"note": note},
        )
        if not created and note:
            # 如果已经打过卡，但这次传了备注，就更新备注。
            check_in.note = note
            check_in.save(update_fields=["note", "updated_at"])

        # select_for_update() 会锁住这条统计记录，避免并发请求同时修改连续天数。
        streak, _ = CheckInStreak.objects.select_for_update().get_or_create(user=request.user)
        if created:
            yesterday = today - timedelta(days=1)
            if streak.last_check_date == yesterday:
                # 昨天也打过卡，说明连续天数 +1。
                streak.current_streak += 1
            elif streak.last_check_date != today:
                # 不是连续打卡，就从 1 天重新开始。
                streak.current_streak = 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_check_date = today
            streak.save()

    # created 为 True 返回 201，表示新建成功；否则返回 200，表示只是更新或重复打卡。
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
