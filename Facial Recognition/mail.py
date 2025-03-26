import smtplib
#授权码：qlgwiffiojtpiabd
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '1790169753@qq.com'  # 发件人邮箱账号
my_pass = 'qlgwiffiojtpiabd'  # 发件人邮箱密码
my_user = '1790169753@qq.com'  # 收件人邮箱账号，我这边发送给自己


def mail():
    msg = MIMEText('监测到有人开门', 'plain', 'utf-8')
    msg['From'] = formataddr(["FromRaspberry", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["Tinky", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "[Warning] Door Opened!"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
    print('邮件发送成功')


if __name__ == "__main__":
    mail()

