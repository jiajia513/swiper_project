''' 用来保存程序逻辑中的状态码 '''

OK = 0 # 成功
VCODE_ERR = 1000 # 验证码发送失败
INVILD_VCODE = 1001  # 验证码无效
ACCESS_TOKEN_ERR = 1002  # 授权码接口错误
USER_INFO_ERR = 1003  # 用户信息接口错误
LOGIN_REQUIRED = 1004  # 用户未登录
USER_DATA_ERRR = 1005  # 用户数据错误
PROFILE_DATA_ERRR = 1006  # 用户交友资料数据错误

class LogicErr(Exception):
    code = None
    data = None
    def __init__(self,data=None):
        self.data = data or self.__class__.__name__


def gen_logic_err(name,code):
    ''' 生成一个逻辑异常类 '''
    return type(name,(LogicErr,),{'code':code})

VcodeErr = gen_logic_err('VcodeErr', 1000)              # 验证码发送失败
InvildVcode = gen_logic_err('InvildVcode', 1001)        # 验证码无效
AccessTokenErr = gen_logic_err('AccessTokenErr', 1002)  # 授权码接口错误
UserInfoErr = gen_logic_err('UserInfoErr', 1003)        # 用户信息接口错误
LoginRequired = gen_logic_err('LoginRequired', 1004)    # 用户未登录
UserDataErrr = gen_logic_err('UserDataErrr', 1005)      # 用户数据错误
ProfileDataErrr = gen_logic_err('ProfileDataErrr', 1006)  # 用户交友资料数据错误
SwipeTypeErr = gen_logic_err('SwipeTypeErr', 1007)      # 滑动类型错误
SwipeRepeatErr = gen_logic_err('SwipeRepeatErr',1008) # 重复滑动错误
RewindLimit = gen_logic_err('RewindLimit', 1009)        # 反悔达到上限
RewindTimeout = gen_logic_err('RewindTimeout', 1010)    # 反悔超时
PermissionLimit = gen_logic_err('PermissionLimit', 1011)  # 用户没有相应的权限