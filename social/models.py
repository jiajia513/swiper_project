from django.db import models

# Create your models here.


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

class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls,uid,sid):
        '''创建好友关系'''
        # 以防每次创建好友关系都去判断sid,uid
        uid1, udi2 = (sid, uid) if uid > sid else (uid, sid)
        cls.objects.create(uid1=uid1, udi2=udi2)
