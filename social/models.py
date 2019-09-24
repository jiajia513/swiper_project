from django.db import models

# Create your models here.
from django.db.models import Q

from common import stat


class Swiped(models.Model):
    STYPE = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )

    uid = models.IntegerField(verbose_name='滑动者的ID')
    sid = models.IntegerField(verbose_name='被滑动者的ID')
    stype = models.CharField(max_length=16,choices=STYPE,verbose_name='滑动的类型')
    stime = models.DateTimeField(auto_now_add=True,verbose_name='滑动时间')

    @classmethod
    def is_like(cls,uid,sid):
        ''' 检查是否喜欢过某人 '''
        return cls.objects.filter(uid=uid, sid=sid,stype__in=['like', 'superlike']).exists()

    # 解决因网络等问题造成的重复滑动对数据库的记录重复的问题
    @classmethod
    def swipe(cls,uid,sid,stype):
        if stype not in ['like','superlike','dislike']:
            raise stat.SwipeTypeErr
        elif cls.objects.filter(uid=uid,sid=sid).exists():
            raise stat.SwipeRepeatErr

        return cls.objects.create(uid=uid,sid=sid,stype=stype)

    @classmethod
    def who_liked_me(cls, uid):
        ''' 取出喜欢自己或超级喜欢自己的人 '''
        return cls.objects.filter(sid=uid,stype__in=['like','superlke']).values_list('uid',flat=True)


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls,uid,sid):
        '''创建好友关系'''
        # 以防每次创建好友关系都去判断sid,uid
        uid1, uid2 = (sid, uid) if uid > sid else (uid, sid)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def friend_ids(cls, uid):
        ''' 查询自己的所有的好友的ID '''
        condition = Q(uid1=uid) | Q(uid2=uid)
        friend_relatons = cls.objects.filter(condition)
        uid_list = []
        for relation in friend_relatons:
            friend_id = relation.uid1 if relation.uid2 == uid else relation.uid2
            uid_list.append(friend_id)
        return uid_list

