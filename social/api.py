from libs.http import render_json
from social import logics


def get_rcmd_users(request):
    ''' 获取推荐用户 '''
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(data = result)

def like(request):
    sid = request.POST.get('sid') # 获取喜欢的用户id
    # 添加滑动记录,判断是否对方也喜欢过自己
    is_matched = logics.like_someone(request.user,sid)
    return render_json({'matched':is_matched})

