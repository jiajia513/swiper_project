''' 程序逻辑配置和第三方平台配置 '''

# 反悔相关配置
DAILY_REWIND = 3  # 每日反悔次数
REWIND_TIMEOUT = 5 * 60  # 可反悔的滑动记录的秒数

# redis相关配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 3,
    'password':123456,
}

# 七牛云配置
QN_ACCESS_KEY = 'kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw'
QN_SECRET_KEY = 'QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy'
QN_BASE_URL = 'http://py4hx1gc8.bkt.clouddn.com'
QN_BUCKET = 'swiper999'

# 云之迅配置
from urllib.parse import urlencode

YZC_ARGS = {
        "sid": "99bb5905a675885ede2f92928203d668",
        "token": "1742dfc1ade1e9c1269b63545da675fa",
        "appid": "f652a7e4ca104d6d94440baf367ff2a2",
        "templateid": "502574",
        "param": None,
        "mobile": None,
    }
YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'

# 微博配置
WB_APP_KEY = '2980503752'
WB_APP_SECRET = 'a82f22e5a181bffa4a825fe9e491fdca'
WB_CALLBACK = 'http://127.0.0.1:8000/weibo/callback' # 授权回调地址，用来供微博访问的

# 第一步 Authorize 请求授权接口
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id':WB_APP_KEY,
    'redirect_uri':WB_CALLBACK,
    'display':'default'
}
WB_AUTH_URL = '%s?%s'%(WB_AUTH_API,urlencode(WB_AUTH_ARGS))
# 第二步 获取授权令牌
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None,
}
# 第三步 获取用户信息
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token': None,
    'uid': None
}