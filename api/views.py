from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse
import json
import requests
@api_view(["POST"])
@permission_classes([AllowAny])
def wx_login(request):
    print("原始请求体：", request.body)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "code": 400,
                "message": "请求参数不是合法 JSON"
            },
            status=400
        )

    code = data.get("code")

    if not code:
        return JsonResponse(
            {
                "code": 400,
                "message": "没有收到微信 code"
            },
            status=400
        )

    # 3. 请求微信 jscode2session 接口
    try:
        response = requests.get("https://api.weixin.qq.com/sns/jscode2session", params={
            "appid":settings.WECHAT_APPID,
            "secret":settings.WECHAT_SECRET,
            "js_code":code,
            "grant_type":"authorization_code",
        },
        timeout=5
        )
        wx_data = response.json()
        print(wx_data,"======================")
    except requests.RequestException as exc:
        print("请求微信接口失败",str(exc))
        return JsonResponse(
            {
                "code": 502,
                "message": "微信登录服务暂时不可用"
            },
            status=502
        )

        print("微信接口返回：", wx_data)
    print("微信接口返回：", wx_data)
    # 4. 微信接口返回错误
    if wx_data.get("errcode"):
        return JsonResponse(
            {
                "code": "WX_LOGIN_FAILED",
                "message": wx_data.get("errmsg", "微信登录失败")
            },
            status=401
        )
        # 5. 获取用户 openid
    openid = wx_data.get("openid")
    unionid = wx_data.get("unionid")

    if not openid:
        return JsonResponse(
            {
                "code": "NO_OPENID",
                "message": "微信未返回 openid"
            },
            status=400
        )

    print("openid：", openid)
    print("unionid：", unionid)
    # 6. 暂时先返回 openid，确认流程通畅
    # 正式环境不要把 openid 直接暴露给前端
    return JsonResponse({
        "code": 0,
        "message": "微信登录成功",
        "data": {
            "openid": openid,
            "unionid": unionid,
        }
    })