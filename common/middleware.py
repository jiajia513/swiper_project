from django.utils.deprecation import MiddlewareMixin

from common import stat
from libs.http import render_json
from user.models import User

''' 登录验证中间件 '''
class AuthorizeMiddleware(MiddlewareMixin):
    # 设置白名单
    WHITE_LIST = [
        '/user/get_vcode',
        '/user/check_vcode',
        '/weibo/wb_auth',
        '/weibo/callback',
    ]

    def process_request(self,request):
        if request.path in self.WHITE_LIST:
            return
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=stat.LOGIN_REQUIRED)

        # 获取当前用户 将用户信息绑定在request对象上
        request.user = User.objects.get(id=uid)
