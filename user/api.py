

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from common import stat, keys
from libs.http import render_json
from libs.qn_cloud import upload_to_qn
from swiper_social import cfg
from user import logics
from user.forms import UserForm, ProfileForm
from user.models import User

''' 获取短信验证码 '''
def get_vcode(request):
    # 获取要验证的手机号
    phonenum = request.GET.get('phonenum')

    # 发送验证码，并检查是否发送成功
    if logics.send_vcode(phonenum):
        return render_json(code=stat.OK)
    else:
        return render_json(code=stat.VCODE_ERR)

    # return JsonResponse(data={'code':0})


''' 验证短信验证码，进行登录或注册 '''
def check_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    vcode_cache = cache.get(keys.VCODE_KEY % phonenum)
    if vcode and vcode_cache and vcode == vcode_cache:
        # 取出用户
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果用户不存在，则将用户添加到表里，自动注册后登录
            # print('============================')
            user = User.objects.create(
                phonenum=phonenum,
                nickname = phonenum
            ) # 这种方法会自动save

            # 登陆后保存一个唯一标识，保存在session
            request.session['uid'] = user.id
            # 返回状态码，并把个人资料返回给前端
            return render_json(code=stat.OK,data=user.to_dict())
    else:
        return render_json(code=stat.VCODE_ERR)


''' 第三方微博登录 '''
# 跳转到用户授权页
def wb_auth(request):
    return redirect(cfg.WB_AUTH_URL)

''' 微博回调接口，通过获取到的授权令牌 获取用户信息，并执行登录或注册 '''
def wb_callback(request):
    code = request.GET.get('code')
    # 获取授权令牌
    access_token,wb_uid = logics.get_access_token(code)
    if not access_token:
        return render_json(code=stat.ACCESS_TOKEN_ERR)

    # 获取用户信息
    user_info = logics.get_user_info(access_token,wb_uid)
    if not user_info:
        return render_json(code=stat.USER_INFO_ERR)

    # 执行登录或注册
    try:
        user = User.objects.get(phonenum = user_info['phonenum'])
    except User.DoesNotExist:
        # 如果用户不存在直接创建出来
        user = User.objects.create(**user_info)

    request.session['uid'] = user.id

    return render_json(code=stat.OK)

''' 获取个人资料、修改个人资料、上传头像 '''
# 获取个人资料
def get_profile(request):
    profile_data = request.user.profile.to_dict()
    return render_json(profile_data)

# 修改个人资料
def set_profile(request):
    # 获取表单提交的数据
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    # 检查User数据
    if not user_form.is_valid():
        return render_json(user_form.errors,code=stat.PROFILE_DATA_ERRR)
    # 检查 Profile 的数据
    if not profile_form.is_valid():
        return render_json(profile_form.errors, code=stat.PROFILE_DATA_ERRR)

    # 保存用户和交友资料的数据
    user = request.user
    user.__dict__.update(user_form.cleaned_data)
    user.save()
    
    user.profile.__dict__.update(profile_form.cleaned_data)
    user.profile.save()


    return render_json()

# 上传个人形象
def upload_avatar(request):
    # 从前端获取上传的头像文件
    avatar = request.FILES.get('avatar')

    # 异步处理，将下面上传文件操作放到logics中，通过装饰器引用celery异步处理
    # # 将文件保存到本地临时存储
    # filename,filepath = logics.save_upload_avatar(request.user,avatar)
    # # 将文件上传到七牛云
    # avatar_url = (filename,filepath)
    # # 将七牛获取的图片路径avatar_url保存到数据库
    # request.user.avatar = avatar_url
    # request.user.save()
    # # 删除本地存储的文件
    # os.remove(filepath)

    logics.handle_avatar.delay(request.user,avatar)

    return render_json()

