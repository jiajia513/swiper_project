import datetime
import time

from common import keys, stat
from libs.cache import rds
from social.models import Swiped, Friend
from swiper_social import cfg
from user.models import User


def rcmd(user):
    ''' 推荐可滑动的用户 '''
    profile = user.profile
    today = datetime.date.today() # 获取当前时间

    # 相对当前用户的交友资料设置的最大年龄的最早出生的日期
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚的出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 取出划过用户的ID
    sid_list = Swiped.objects.filter(uid=user.id).values_list('sid', flat=True)
    # 取出超级喜欢过自己，但是还没有被自己滑过的
    superliked_me_id_list = [int(uid) for uid in rds.zrange(keys.SUPERLIKED_KEY % user.id,0,19)]
    superliked_me_users = User.objects.filter(id__in = superliked_me_id_list)

    # 筛选出符合条件的用户
    other_count = 20-len(superliked_me_users)
    if other_count>0:
        other_users = User.objects.filter(
            sex = profile.dating_sex,
            location = profile.dating_location,
            birthday__gte = earliest_birthday,
            birthday__lte = latest_birthday,
        ).exclude(id__in=sid_list)[:other_count]
        users = superliked_me_users | other_users
    else:
        users = superliked_me_users

    return users

def like_someone(user,sid):
    ''' 喜欢某人，添加记录并判断是否配对 '''
    # Swiped.objects.create(uid=user.id, sid=sid, stype='like')  # 添加滑动记录
    Swiped.swipe(user.id, sid, 'like')

    # 判断对方是否也喜欢过自己，如果喜欢就创建好友关系
    if Swiped.is_like(sid,user.id):  # 将uid和sid反过来
        # 喜欢过就创建好友关系并存入好友关系表
        Friend.make_friends(user.id,sid)
        return True
    return False

def superlike_someone(user,sid):
    ''' 超级喜欢某人
    自己超级喜欢过对方，则一定会出现在对方的推荐列表中'''
    Swiped.swipe(user.id, sid, 'superlike')  # 添加滑动记录

    # 将自己的id写如对方的优先推荐队列中
    rds.zadd(keys.SUPERLIKED_KEY % sid,{user.id:time.time()})
    if Swiped.is_like(sid, user.id):
        # 如果对方喜欢过自己，匹配成好友
        Friend.make_friends(user.id, sid)
        # 如果对方超级喜欢过你，将对方从你的超级喜欢列表中删除
        rds.zrem(keys.SUPERLIKED_KEY % user.id, sid)
        return True
    else:
        return False

def dislike_someone(user,sid):
    ''' 不喜欢某人 '''
    Swiped.swipe(user.id,sid,'dislike') # 添加滑动记录
    # 如果对方超级喜欢你，将对方从你的超级喜欢列表中删除
    rds.zrem(keys.SUPERLIKED_KEY % user.id,sid)


def rewind_swiped(user):
    ''' 反悔一次滑动记录 '''
    # 获取今天的反悔次数
    rewind_times = rds.get(keys.REWIND_KEY % user.id,0)

    # 检查今天的反悔次数是否达到3次
    if rewind_times >= cfg.DAILY_REWIND:
        return stat.RewindLimit

    # 找到最近的一次的滑动记录
    latest_swiped = Swiped.objects.filter(uid = user.id).latest('stime')

    # 检查反悔记录是否是5分钟之内的
    now = datetime.datetime.now()
    if (now - latest_swiped.stime).total_seconds() >= cfg.REWIND_TIMEOUT:
        raise stat.RewindTimeout

    # 检查上一次滑动记录是否有可能匹配成为好友，删除好友记录
    if latest_swiped.stype in ['like','superlike']:
        Friend.break_off(user.id,latest_swiped.sid)

    # 如果滑动是超级喜欢，将自己的uid从对方的推荐列表中删除
    if latest_swiped.stype is 'superlike':
        rds.zrem(keys.SUPERLIKED_KEY % latest_swiped.sid,user.id)

    # 删除滑动记录
    latest_swiped.delete()

    # 更新当天的滑动次数，同时设置过期时间为下一个凌晨
    next_zero = datetime.datetime(now.year,now.month,now.day) + datetime.timedelta(1)
    remain_seconds = (next_zero - now).total_seconds()
    rds.set(keys.REWIND_KEY % user.id,rewind_times+1,int(remain_seconds))