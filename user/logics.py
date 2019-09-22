
# 发送短信验证码
import random

import requests
from django.core.cache import cache

from common import keys
from swiper_social import cfg


def send_vcode(phonenum):
    # 产生随即验证码
    chars = random.sample([str(i) for i in range(9)],6)
    vcode = ''.join(chars)
    # print('=============')
    # print(vcode)
    # 将生成的验证码保存到缓存中，并设置过期时间,(以电话号码为缓存的key)
    cache.set(keys.VCODE_KEY % phonenum,vcode,180)
    print('验证码是：',vcode) # 682503

    sms_args = cfg.YZC_ARGS.copy()
    sms_args['mobile'] = phonenum
    sms_args['param'] = vcode
    response = requests.post(cfg.YZX_API,json=sms_args)


    # 检查最终返回值
    if response.status_code == 200:
        result = response.json()
        # print(result)
        if result['code'] == '000000':
            return True
    return False

''' 微博第三方登录 '''
def get_access_token(code):
    args = cfg.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    response = requests.post(cfg.WB_ACCESS_TOKEN_API,data=args)
    if response.status_code == 200:
        result = response.json()
        access_token = result['access_token']
        wb_uid = result['uid']
        return access_token,wb_uid
    return None,None

def get_user_info(access_token,wb_uid):
    args = cfg.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = wb_uid
    response = requests.get(cfg.WB_USER_SHOW_API,params=args)
    # 检查返回值
    if response.status_code == 200:
        result = response.json()
        user_info = {
            'phonenum':'WB_%s'% wb_uid,
            'nickname':result['screen_name'],
            'sex':'femal' if result['gender'] == 'f' else 'male',
            'avatar': result['avatar_hd'],
            'location': result['location'].split(' ')[0],
        }
        return user_info
    return None

''' 将头像文件保存到本地tmp文件夹 '''
def save_upload_avatar(user,upload_avatar):
    filename = 'Avatar-%s'%user.id
    filepath = '/tmp/%s'%filename

    with open(filepath,'wb',) as fp:
        for chunk in upload_avatar.chunks():
            fp.write(chunk)
    return filename,filepath


