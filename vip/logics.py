
''' 检查vip用户是否具有某种功能权限装饰器 '''
from common import stat


def need_permission(view_func):
    def check(request,*args,**kwargs):
        perm_name = view_func.__name__
        # 检查当前用户是否具有对所操作的函数对应的权限
        if request.user.vip.has_perm(perm_name):
            return check(request,*args,**kwargs)
        else:
            raise stat.PermissionLimit
    return check