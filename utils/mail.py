import smtplib
from email.mime.text import MIMEText
import atexit

def send_mail(sub=None, cont=None):
    '''
    sub: 邮件主题
    cont: 邮件正文
    '''
    try:
        # 发件人邮箱地址
        sendAddress = '497465762@qq.com'
        # 发件人授权码
        password = 'chllcjcngjbdcahg'
        # 连接服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 登录邮箱
        loginResult = server.login(sendAddress, password)
        print(loginResult)

        # 正文
        content = cont
        # 定义一个可以添加正文的邮件消息对象
        msg = MIMEText(content, 'plain', 'utf-8')
        # 发件人昵称和地址
        msg['From'] = 'webdev<497465762@qq.com>'
        # 收件人昵称和地址
        msg['To'] = 'hb_dys<hb_dys@163.com>'
        # 邮件主题
        msg['Subject'] = sub
        server.sendmail(sendAddress,['hb_dys@163.com'], msg.as_string())
        print('发送成功')
    except:
        print('发送失败')

# 在程序退出时使用，可以用于提醒报错或者执行结束
# 示例1
@atexit.register
def go():
    # with open('./law/国家法律法规数据库/down_load_urls/unique_url.json', 'w', encoding='utf8') as f:
    #     json.dump(unique_url, f, ensure_ascii=False)  # 可写中文
    #     print('已获取url保存成功')
    # with open('./law/国家法律法规数据库/down_load_urls/law_title_url.json', 'w', encoding='utf8') as f:
    #     json.dump(law_title_url, f, ensure_ascii=False)  # 可写中文
    #     print('已获取law_title_url保存成功')
    print('停止')
    send_mail('报错', '错误内容')

# 实例2
atexit.register(go)