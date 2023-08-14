'''
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
战国大逃杀_V1.1
updata 修改登录方式，修复账号封禁无法登录
bug反馈 https://t.me/qianmo98
task 签到，后续陆续增加
无需下载,浏览器打开，
https://www.zgdts.zhonghebang.cn/#/pages/login/register?invite=buEGHV
0撸，注册获得5米，每天签到得1米，不建议投资
流程：先扫码注册，实名后加入官方群753554661，发送手机号+已实名+领取金币，等待50金币到账，金币到账后参与一次大逃杀即可成为有效玩家，即可开始每天的签到
然后出售50币收益约6块，每日签到一次10币约1块
抓任意包取出Authorization
export zgtoken=Authorization 多账户换行隔开
corn：10 10 * * *
'''
import requests
import re

response = requests.get('https://netcut.cn/p/e9a1ac26ab3e543b')
note_content_list = re.findall(r'"note_content":"(.*?)"', response.text)
formatted_note_content_list = [note.replace('\\n', '\n').replace('\\/', '/') for note in note_content_list]

for note in formatted_note_content_list:
    print(note)



import os
import requests,datetime
accounts = os.getenv("zgtoken")

# 检查zgtoken是否存在
if accounts is None:
    print('你不填入zgtoken，咋运行？')
else:
    # 获取环境变量的值，并按竖线分割成多个账号的参数组合
    accounts_list = os.environ.get('zgtoken').split('\n')
    num_of_accounts = len(accounts_list)
    print(f"获取到 {num_of_accounts} 个账号")

    # 遍历所有账号
    for i, account in enumerate(accounts_list, start=1):
        # 按分号参分割当前账号的不同数
        values = account.split('@')
        Authorization = values[0] # 获取各个值
        print(f"\n=======开始执行账号{i}=======")


        print("==============查询账号==============")
        url = f"https://api.zgdts.zhonghebang.cn/api/v1/user_profile"
        headers = {
            "authorization": Authorization,
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; vivo Y85 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 Html5Plus/1.0",
        }

        res = requests.post('https://api.zgdts.zhonghebang.cn/api/v1/user_profile', headers=headers).json()
        if 'code' in res and res['code'] == 1:
            nickname = res['data']['nickname']
            coin = res['data']['coin']
            level = res['data']['level']
            invite_code = res['data']['invite_code']
            print(f'【昵称】:{nickname}---{level}\n【邀请码】:{invite_code}\n【当前金币】:{coin}')
        else:
            print(f'错误未知{res["data"]}')

        print("==============执行签到任务==============")
        url = f"https://api.zgdts.zhonghebang.cn/api/v1/user/sign_in"
        today = datetime.date.today()
        day = today.day


        data = {
            'time': day
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        print(response["msg"])
