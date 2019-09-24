from libs.http import render_json
from social import logics
from social.models import Swiped, Friend
from user.models import User


def get_rcmd_users(request):
    ''' 获取推荐用户 '''
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(data = result)

def like(request):
    ''' 右滑喜欢 '''
    sid = int(request.POST.get('sid')) # 获取喜欢的用户id
    # 添加滑动记录,判断是否对方也喜欢过自己
    is_matched = logics.like_someone(request.user,sid)
    return render_json({'matched':is_matched})

def superlike(request):
    ''' 上滑 超级喜欢 '''
    sid = int(request.POST.get('sid'))  # 获取超级喜欢的用户id
    is_matched = logics.superlike_someone(request.user, sid)
    return render_json({'matched': is_matched})

def dislike(request):
    ''' 左滑不喜欢 '''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.user, sid)
    return render_json()

def show_liked_me(request):
    ''' 查看谁喜欢过我 '''
    user_id_list = Swiped.who_liked_me(request.user.id)
    users = User.objects.filter(id__in=user_id_list)
    result = [user.to_dict() for user in users]
    return render_json(result)

def friend_list(request):
    ''' 好友列表 '''
    friend_id_list = Friend.friend_ids(request.user.id)
    users = User.objects.filter(id__in=friend_id_list)
    result = [user.to_dict() for user in users]
    return render_json(result)

