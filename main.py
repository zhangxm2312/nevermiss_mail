from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText

links_dic={}

# 将网站首页通知写入待发送列表
# parent_link: str, 主网页
# list_link: str, 主网页中通知列表所在网页
# news_class: str, 通知列表所在网页中通知所属的class名
def news_spider(parent_link, list_link, news_class):
    news_req=requests.get(parent_link+list_link)
    news_req.encoding="UTF-8"
    news_soup=BeautifulSoup(news_req.text,'html.parser')
    # 网址中通知都在一个class="news_title"的span里
    news_list = news_soup.find_all(attrs={"class": news_class})
    for link in news_list:  # 写入待发送列表
        links_dic[parent_link+str(link.a.get('href'))]=str(link.a.get_text())

news_spider("https://jwc.ahu.edu.cn", "/10314/list.htm", "news_title")  # 教务处
# news_spider("https://wendian.ahu.edu.cn", "/14566/list.htm", "Article_Title")  # 文典学院
# news_spider("https://www.ahu.edu.cn", "/tzgg/list.htm","cols_title") #安徽大学

# 收件人
accepter={'章小明':'2797477677@qq.com'}

# 已发送邮件
mail_sent = {
    'https://jwc.ahu.edu.cn/2022/0522/c10314a286802/page.htm': '关于调整2022年上半年全国大学英语四、六级考试安排及相关事项的通知',
    'https://jwc.ahu.edu.cn/2022/0522/c10314a286801/page.htm': '2022年上半年大学英语四、六级考试安徽大学考点防疫须知',
    'https://jwc.ahu.edu.cn/2022/0520/c10314a286742/page.htm': '关于开展2022-2023学年《军事理论》课程（蜀山校区）助教选聘工作的通知',
    'https://jwc.ahu.edu.cn/2022/0519/c10314a286595/page.htm': '关于2022-2023学年第一学期本科学生选课安排的通知',
    'https://jwc.ahu.edu.cn/2022/0518/c10314a286205/page.htm': '关于开展就业育人“共创行动”企业和专家遴选推荐的通知',
    'https://jwc.ahu.edu.cn/2022/0517/c10314a286110/page.htm': '关于开展“国创计划”十五周年荣誉表彰及纪念丛书征文推荐工作的通知',
    'https://jwc.ahu.edu.cn/2022/0516/c10314a286054/page.htm': '关于举办2022年中国机器人及人工智能大赛安徽大学校内选拔赛的通知',
    'https://jwc.ahu.edu.cn/2022/0516/c10314a286005/page.htm': '关于做好2021-2022学年第二学期期末考试工作的通知',
    'https://jwc.ahu.edu.cn/2022/0512/c10314a285822/page.htm': '关于调整本学期后续本科教学安排的通知',
    'https://jwc.ahu.edu.cn/2022/0512/c10314a285772/page.htm': '关于开展2021-2022学年第二学期劳动教育实践活动的通知'}

# 邮件插件
vpn = 1 # vpn=1则用qq发邮件，否则用gmail发
smtp_server = 'smtp.qq.com' if vpn else 'smtp.gmail.com'
port = 465 if vpn else 587
# user_email = QQ邮箱 if vpn else Gmail邮箱
# password = QQ邮箱SMTP授权码

# 登陆邮箱
server = smtplib.SMTP_SSL(smtp_server, timeout=60)
server.connect(smtp_server, port)
server.login(user_email, password)

# 发送邮件
for news in links_dic:
    # 若在已发送列表，则跳过
    if news in mail_sent:
        continue
    # 邮件正文、发件人、标题
    msg = MIMEText(news, 'plain', 'utf-8')
    msg['From'] = '安徽大学爬虫邮件系统'
    msg['Subject'] = links_dic[news]
    # 逐个发送给收件人列表
    for one in accepter:
        msg['To'] = one
        server.sendmail(user_email, accepter[one], msg.as_string())
    # 加入已发送列表
    mail_sent[news]=links_dic[news]
links_dic={}
