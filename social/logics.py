import datetime

from social.models import Swiped, Friend
from user.models import User


def rcmd(user):
    ''' 推荐可滑动的用户 '''
    profile = user.profile
    today = datetime.date.today() # 获取当前时间

    # 相对当前用户的交友资料设置的最大年龄的最早出生的日期
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚的出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 筛选出符合条件的用户
    users = User.objects.filter(
        sex = profile.dating_sex,
        location = profile.dating_location,
        birthday__gte = earliest_birthday,
        birthday__lte = latest_birthday,
    )[:20]
    return users

def like_someone(user,sid):
    ''' 喜欢某人，添加记录并判断是否配对 '''
    Swiped.objects.create(uid=user.id, sid=sid, stype='like')  # 添加滑动记录

    # 判断对方是否也喜欢过自己，如果喜欢就创建好友关系
    if Swiped.is_like(sid,user.id):  # 将uid和sid反过来
        # 喜欢过就创建好友关系并存入好友关系表
        Friend.make_friends(user.id,sid)
        return True
    return False

