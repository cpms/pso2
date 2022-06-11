import re
import aiohttp
import asyncio
import feedparser
from PIL import Image
from io import BytesIO
import math
import base64
import hoshino
import traceback
import os
import json
import time
import random
import string

import sys
import html

rss_news = {}

data = {
    'rsshub': 'http://rss.shab.fun',
    'proxy': 'http://127.0.0.1:10809',
    'proxy_urls': ['https://pbs.twimg.com'],
    'last_time': {},
    'group_rss': {},
    'group_mode': {},
    'ngs_emg_time': [],
}

HELP_MSG = '''命令前缀pso2cmd
pso2cmd list : 查看订阅列表
pso2cmd add rss地址 : 添加rss订阅
pso2cmd remove 序号 : 删除订阅列表指定项
今日土豆：发送最新土豆图
今日土豆细节：发送最新土豆细节图
最近紧急：发送最近一次NGS紧急任务的发生时间
紧急记录：发送今日NGS紧急任务的时间记录
验证码识别：在此关键词后面接上SEGA的验证码图片，尝试进行识别
'''

sv = hoshino.Service('pso2', bundle='pso2ngs紧急预告、每日土豆图、PSO2日文验证码识别', help_= HELP_MSG)
alpha_img_base64 = ""
sukeiru_img_base64 = ""
alpha_detail_base64 = ""
sukeiru_detail_base64 = ""
first_start_flag = True

def save_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        traceback.print_exc()

def load_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(path):
        save_data()
        return
    try:
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            if 'rsshub' in d:
                if d['rsshub'][-1] == '/':
                    d['rsshub'] = d['rsshub'][:-1]
                data['rsshub'] = d['rsshub']
            if 'last_time' in d:
                data['last_time'] = d['last_time']
            if 'group_rss' in d:
                data['group_rss'] = d['group_rss']
            if 'group_mode' in d:
                data['group_mode'] = d['group_mode']
            if 'proxy' in d:
                data['proxy'] = d['proxy']
            if 'proxy_urls' in d:
                data['proxy_urls'] = d['proxy_urls']
            if 'ngs_emg_time' in d :
                data['ngs_emg_time'] = d['ngs_emg_time']
    except:
        traceback.print_exc()
    global default_rss

load_data()

default_rss = []
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())#解决aiohttp使用代理后参数出错
async def query_data(url, proxy=''):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy) as resp:
                return await resp.read()
    except:
        return None

async def post_captcha_img(data):
    csrftoken = '8pcWwO4gbPGqFSdHN6befQvWX95KsZ8Q2eSReVxqIP8cXyx3XSxiU3a1fMfHOuxv'#抓访问首页的cookies
    csrfmiddlewaretoken = 'LD0wQha7iE7y7iArpuIaIxJV4rdJsemiFsGryoDhPEzkpYUNzg4enKo0m4nGOJLX'#抓接口地址提交的隐藏表单
    
    multipartWriter = aiohttp.MultipartWriter('mixed')
    multipartWriter.append(csrfmiddlewaretoken).set_content_disposition('form-data', name = 'csrfmiddlewaretoken')
    multipartWriter.append(data, {'Content-Type': 'image/jpg'}) \
    .set_content_disposition(
        'form-data',
        name = 'file',
        filename = '123.jpg'
    )
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62', 'Content-Type': 'multipart/form-data; boundary=' + multipartWriter.boundary}
    cookies = {'csrftoken': csrftoken}
    url_upload = 'http://pso2s.com/upload/'
    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.post(url_upload, data = multipartWriter ,headers = headers) as resp:
                if resp.status == 200:
                    return await resp.text(encoding="utf-8")
                else:
                    return "出现未知错误，请重试"
    except:
        return None

def get_image_url(desc):
    imgs = re.findall(r'<img.*?src="(.+?)".+?>', desc)
    return imgs

def ngs_translate(content):
    content = content.replace("緊急通知","紧急任务通知")
    content = content.replace("緊急クエストが発生します","有紧急任务")
    content = content.replace("ステージライブが開催します","有演唱会")
    return content

def ngs_time(content):#转换成北京時間ngs
    content = content.replace("01:00","00点")
    content = content.replace("02:00","01点")
    content = content.replace("03:00","02点")
    content = content.replace("04:00","03点")
    content = content.replace("05:00","04点")
    content = content.replace("06:00","05点")
    content = content.replace("07:00","06点")
    content = content.replace("08:00","07点")
    content = content.replace("09:00","08点")
    content = content.replace("10:00","09点")
    content = content.replace("11:00","10点")
    content = content.replace("12:00","11点")
    content = content.replace("13:00","12点")
    content = content.replace("14:00","13点")
    content = content.replace("15:00","14点")
    content = content.replace("16:00","15点")
    content = content.replace("17:00","16点")
    content = content.replace("18:00","17点")
    content = content.replace("19:00","18点")
    content = content.replace("20:00","19点")
    content = content.replace("21:00","20点")
    content = content.replace("22:00","21点")
    content = content.replace("23:00","22点")
    content = content.replace("00:00","23点")
    
    content = content.replace("01:30","00点30分")
    content = content.replace("02:30","01点30分")
    content = content.replace("03:30","02点30分")
    content = content.replace("04:30","03点30分")
    content = content.replace("05:30","04点30分")
    content = content.replace("06:30","05点30分")
    content = content.replace("07:30","06点30分")
    content = content.replace("08:30","07点30分")
    content = content.replace("09:30","08点30分")
    content = content.replace("10:30","09点30分")
    content = content.replace("11:30","10点30分")
    content = content.replace("12:30","11点30分")
    content = content.replace("13:30","12点30分")
    content = content.replace("14:30","13点30分")
    content = content.replace("15:30","14点30分")
    content = content.replace("16:30","15点30分")
    content = content.replace("17:30","16点30分")
    content = content.replace("18:30","17点30分")
    content = content.replace("19:30","18点30分")
    content = content.replace("20:30","19点30分")
    content = content.replace("21:30","20点30分")
    content = content.replace("22:30","21点30分")
    content = content.replace("23:30","22点30分")
    content = content.replace("00:30","23点30分")
    return content

def pso2_time(content):#转换成北京時間pso2
    count01 = 0
    if content.count("01") == 1:
        count01 = 1
    elif content.count("01") == 2:
        count01 = 2
    content = content.replace("01","北京時間00")
    content = content.replace("02","北京時間01")
    content = content.replace("03","北京時間02")
    content = content.replace("04","北京時間03")
    content = content.replace("05","北京時間04")
    content = content.replace("06","北京時間05")
    content = content.replace("07","北京時間06")
    content = content.replace("08","北京時間07")
    content = content.replace("09","北京時間08")
    content = content.replace("10","北京時間09")
    content = content.replace("11","北京時間10")
    content = content.replace("12","北京時間11")
    content = content.replace("13","北京時間12")
    content = content.replace("14","北京時間13")
    content = content.replace("15","北京時間14")
    content = content.replace("16","北京時間15")
    content = content.replace("17","北京時間16")
    content = content.replace("18","北京時間17")
    content = content.replace("19","北京時間18")
    content = content.replace("20","北京時間19")
    content = content.replace("21","北京時間20")
    content = content.replace("22","北京時間21")
    content = content.replace("23","北京時間22")
    if count01 == 0:
        content = content.replace("00","北京時間23")
    elif count01 == 1:
        content = re.sub(r"】\d{2}","】北京時間23",content)
    content = re.sub(r"】\d{2}","】北京時間23",content)
    return content

def remove_html(content):
    #移除html标签
    content = content.replace('<br>','\n')#转换换行符1
    content = content.replace('<br /><br />','\n')#转换换行符2
    if content.find("#PSO2NGS緊急通知") >= 0:
        content = ngs_time(content)
        if content.find("#PSO2NGS緊急通知") >= 0 and content.find("ステージライブ") >= 0: #处理半点紧急
            if time.localtime().tm_hour == 23:
                data['ngs_emg_time'].append('00:30')
            else:
                ngs_emg_time_tmp = time.localtime().tm_hour + 1
                data['ngs_emg_time'].append(str(ngs_emg_time_tmp) + ':30')
        elif content.find("#PSO2NGS緊急通知") >= 0 and content.find("30分") == -1: #处理整点紧急
            if time.localtime().tm_hour == 23:
                data['ngs_emg_time'].append('00:00')
            else:
                ngs_emg_time_tmp = time.localtime().tm_hour + 1
                data['ngs_emg_time'].append(str(ngs_emg_time_tmp) + ':00')
        temp_list = []#紧急记录去重
        for i in data['ngs_emg_time']:
            if i not in temp_list:
                temp_list.append(i)
        data['ngs_emg_time'] = temp_list
        content = re.sub(r"\nVer.*緊急通知","",content)#去掉最后一行
        content = ngs_translate(content)#翻译内容
    elif content.find("#PSO2") >= 0:
        content = re.sub(r"\(.*\)","",content,1)#去掉上一场紧急的信息
        content = re.sub(r"＞\n #","＞\n予告無し #",content)#处理无预告1
        content = re.sub(r"＞\n【","＞\n予告無し\n【",content)#处理无预告2
        content = content.replace("<br><br>","<br>")#去除2次换行
        content = pso2_time(content)#转换时间
    p = re.compile('<[^>]+>')
    content = p.sub("", content)
    return content

def remove_lf(content):
    text = ''
    for line in content.splitlines():
        line =  line.strip()
        if line:
            text += line + '\n'
    text = text.rstrip()
    return text

async def generate_pso2_image(url_list,mode):#mode0=土豆，mode1=土豆细节
    try:
        url = html.unescape(url_list[mode])
    except:
        return None
    proxy = ''
    for purl in data['proxy_urls']:
        if purl in url:
            proxy = data['proxy']
    image = await query_data(url, proxy)
    if image:
        try:
            im = Image.open(BytesIO(image))
            im = im.convert("RGBA")
            raw_images = im
        except:
            pass

    io = BytesIO()
    raw_images.save(io, 'png')
    return io.getvalue()

async def generate_image(url_list):
    raw_images = []
    num = 0
    for url in url_list:
        url = html.unescape(url)
        proxy = ''
        for purl in data['proxy_urls']:
            if purl in url:
                proxy = data['proxy']
        image = await query_data(url, proxy)
        if image:
            try:
                im = Image.open(BytesIO(image))
                im = im.convert("RGBA")
                raw_images.append(im)
                num += 1
            except:
                pass
        if num >= 9:
            break

    if num == 0:
        return None
    elif num == 1:
        io = BytesIO()
        raw_images[0].save(io, 'png')
        return io.getvalue()

    dest_img = None
    box_size = 300
    row = 3
    border = 5
    height = 0
    width = 0
    if num == 3 or num >= 5:    #3列
        width = 900 + border * 2
        height = math.ceil(num / 3) * (300 + border) - border
    else: #2列
        box_size = 400
        row = 2
        width = 800 + border
        height = math.ceil(num / 2) * (400 + border) - border
    dest_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))

    for i in range(num):
        im = raw_images[i]
        if im:
            w, h = im.size
            if w > h:
                x0 = (w // 2) - (h // 2)
                x1 = x0 + h
                im = im.crop((x0, 0, x1, h))
            elif h > w:
                y0 = (h // 2) - (w // 2)
                y1 = y0 + w 
                im = im.crop((0, y0, w, y1))
            im = im.resize((box_size, box_size),Image.ANTIALIAS)
            x = (i % row) * (box_size + border)
            y = (i // row) * (box_size + border)
            dest_img.paste(im, (x, y))
    io = BytesIO()
    dest_img.save(io, 'png')
    return io.getvalue()

def get_published_time(item):
    time_t = 0
    if 'published_parsed' in item:
        time_t = time.mktime(item['published_parsed'])
    if 'updated_parsed' in item:
        time_t = time.mktime(item['updated_parsed'])
    return time_t

def get_latest_time(item_list):
    last_time = 0
    for item in item_list:
        time = get_published_time(item)
        if time > last_time:
            last_time = time
    return last_time

def check_title_in_content(title, content):
    title = title[:len(title)//2]
    title = title.replace('\n', '').replace('\r', '').replace(' ', '')
    content = content.replace('\n', '').replace('\r', '').replace(' ', '')
    if title in content:
        return True
    return False
    

async def get_rss_news(rss_url):
    global alpha_img_base64
    global sukeiru_img_base64
    global alpha_detail_base64
    global sukeiru_detail_base64
    global first_start_flag
    
    news_list = []
    proxy = ''
    for purl in data['proxy_urls']:
        if purl in rss_url:
            proxy = data['proxy']
    res = await query_data(rss_url, proxy)
    if not res:
        return news_list
    feed = feedparser.parse(res)
    if feed['bozo'] != 0:
        sv.logger.info(f'rss解析失败 {rss_url}')
        return news_list
    if len(feed['entries']) == 0:
        return news_list
    if rss_url not in data['last_time']:
        sv.logger.info(f'rss初始化 {rss_url}')
        data['last_time'][rss_url] = get_latest_time(feed['entries'])
        return news_list

    last_time = data['last_time'][rss_url]

    for item in feed["entries"]:
        if get_published_time(item) > last_time or (first_start_flag and item['description'].find("#アルファリアクター") != -1): #插件启动后的第一次获取土豆
            if first_start_flag:
                first_start_flag = False
            summary = item['summary']
            #移除转发信息
            i = summary.find('//转发自')
            if i > 0:
                summary = summary[:i]
            if item['description'].find("#アルファリアクター") != -1: #处理土豆
                image_urls = get_image_url(summary)
                alpha_img_bin = await generate_pso2_image(image_urls,0)
                alpha_detail_bin = await generate_pso2_image(image_urls,1)
                try:
                    alpha_img_base64 = f"base64://{base64.b64encode(add_salt(alpha_img_bin)).decode()}"
                except:
                    pass
                try:
                    alpha_detail_base64 = f"base64://{base64.b64encode(add_salt(alpha_detail_bin)).decode()}"
                except:
                    pass
                news = {
                    'feed_title': feed['feed']['title'],
                    'title': item['title'],
                    'content': remove_html(summary),
                    'id': item['id'],
                    'description': remove_html(item['description']),
                    'image': "",
                    }
            else:
                news = {
                    'feed_title': feed['feed']['title'],
                    'title': item['title'],
                    'content': remove_html(summary),
                    'id': item['id'],
                    'description': remove_html(item['description']),
                    'image': await generate_image(get_image_url(summary)),
                    }
            news_list.append(news)
    data['last_time'][rss_url] = get_latest_time(feed['entries'])
    return news_list

async def refresh_all_rss():
    for item in default_rss:
        if item not in rss_news:
            rss_news[item] = []
    for group_rss in data['group_rss'].values():
        for rss_url in group_rss:
            if rss_url not in rss_news:
                rss_news[rss_url] = []
    #删除没有引用的项目的推送进度
    for rss_url in list(data['last_time'].keys()):
        if rss_url not in rss_news:
            data['last_time'].pop(rss_url)
    for rss_url in rss_news.keys():
        rss_news[rss_url] = await get_rss_news(rss_url)
    save_data()

def add_salt(data):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    return data + bytes(salt, encoding="utf8")

def format_msg(news):
    #msg = f"{news['feed_title']}更新:"
    #if not check_title_in_content(news['title'], news['content']):
        #msg += f"\n{news['title']}"async
    #msg += f"\n----------\n{remove_lf(news['description'])}"
    msg = remove_lf(news['description'])
    if news['image']:
        base64_str = f"base64://{base64.b64encode(add_salt(news['image'])).decode()}"
        msg += f'[CQ:image,file={base64_str}]'
    return msg

def format_brief_msg(news):
    msg = f"{news['feed_title']}更新:\n{news['id']}"
    msg += f"\n----------\n{news['title']}"
    return msg

async def group_process():
    bot = hoshino.get_bot()
    groups = await sv.get_enable_groups()
    await refresh_all_rss()
    
    for gid in groups.keys():
        rss_list = default_rss
        if str(gid) in data['group_rss']:
            rss_list = data['group_rss'][str(gid)]
        else:
            data['group_rss'][str(gid)] = default_rss
        for rss_url in rss_list:
            if rss_url in rss_news:
                news_list = rss_news[rss_url]
                for news in reversed(news_list):
                    msg = None
                    if str(gid) in data['group_mode'] and data['group_mode'][str(gid)] == 1:
                        msg = format_brief_msg(news)
                    else:
                        msg = format_msg(news)
                    try:
                        if msg.find("#アルファリアクター") > 0 or msg.find("緊急クエスト予告＞ #PSO2") > 0: #不发送土豆图、无紧急PSO2预告
                            pass
                        else:
                            await bot.send_group_msg(group_id=gid, message=msg)
                    except:
                        sv.logger.info(f'群 {gid} 推送失败')
                await asyncio.sleep(1)

async def rss_add(group_id, rss_url):
    group_id = str(group_id)
    proxy = ''
    for purl in data['proxy_urls']:
        if purl in rss_url:
            proxy = data['proxy']
    res = await query_data(rss_url, proxy)
    feed = feedparser.parse(res)
    if feed['bozo'] != 0:
        return f'无法解析rss源:{rss_url}'
        
    if group_id not in data['group_rss']:
        data['group_rss'][group_id] = default_rss
    if rss_url not in set(data['group_rss'][group_id]):
        data['group_rss'][group_id].append(rss_url)
    else:
        return '订阅列表中已存在该项目'
    save_data()
    return '添加成功'

def rss_remove(group_id, i):
    group_id = str(group_id)
    if group_id not in data['group_rss']:
        data['group_rss'][group_id] = default_rss
    if i >= len(data['group_rss'][group_id]):
        return '序号超出范围'
    data['group_rss'][group_id].pop(i)
    save_data()
    return '删除成功\n当前' + rss_get_list(group_id)

def rss_get_list(group_id):
    group_id = str(group_id)
    if group_id not in data['group_rss']:
        data['group_rss'][group_id] = default_rss
    msg = '订阅列表:'
    num = len(data['group_rss'][group_id])
    for i in range(num): 
        url = data['group_rss'][group_id][i]
        url = re.sub(r'http[s]*?://.*?/', '/', url)
        msg += f"\n{i}. {url}"
    if num == 0:
        msg += "\n空"
    return msg

def rss_set_mode(group_id, mode):
    group_id = str(group_id)
    mode = int(mode)
    if mode > 0:
        data['group_mode'][group_id] = 1
        msg = '已设置为简略模式'
    else:
        data['group_mode'][group_id] = 0
        msg = '已设置为标准模式'
    save_data()
    return msg

@sv.on_prefix('验证码识别')
async def get_captcha(bot, ev):
    captcha_img = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    if captcha_img:
        await bot.send(ev,f'正在识别验证码，请稍候')
        captcha_img_url = captcha_img.group(2)
        captcha_img_bin = await query_data(captcha_img_url, "")
        result = await post_captcha_img(captcha_img_bin)
        await bot.send(ev,f'验证码识别结果：\n{result}\n\nPowered By pso2s.com')
    else:
        await bot.send(ev,'没有识别到图片，请在关键词后面直接加上图片发送')

@sv.on_rex(r'^(每日|今日|今天|最新)土豆$')
async def send_alpha_img(bot, ev):
    if alpha_img_base64 != "":
        await bot.send(ev, f'[CQ:image,file={alpha_img_base64}]')
    else:
        await bot.send(ev, "今日土豆图尚未获取，请等待刷新\n刷新时间为每小时5、15、45分")

@sv.on_rex(r'^(每日|今日|今天|最新)土豆(详细|细节)$')
async def send_alpha_detail(bot, ev):
    if alpha_detail_base64 != "":
        await bot.send(ev, f'[CQ:image,file={alpha_detail_base64}]')
    else:
        await bot.send(ev, "今日土豆细节图尚未获取，请等待刷新\n刷新时间为每小时5、15、45分")
        
@sv.on_rex(r'^有紧急嘛|有紧急吗|最近紧急|有无紧急|近期紧急$')
async def send_last_ngs_emg(bot, ev):
    if data['ngs_emg_time']:
        msg = f"最近一次NGS紧急任务的时间为 {data['ngs_emg_time'][len(data['ngs_emg_time'])-1]}"
    else:
        msg = "暂无数据"
    await bot.send(ev, msg)

@sv.on_fullmatch('紧急记录')
async def send_ngs_emg_log(bot, ev):
    if data['ngs_emg_time']:
        emg_time = ""
        for i in range(len(data['ngs_emg_time'])-1,-1,-1):
            emg_time += f"\n{data['ngs_emg_time'][i]}"
        msg = f"今日NGS紧急任务的发生时间记录：\n{emg_time}"
    else:
        msg = "暂无数据"
    await bot.send(ev, msg)

@sv.on_prefix('pso2cmd')
async def rss_cmd(bot, ev):
    msg = ''
    group_id = ev.group_id
    args = ev.message.extract_plain_text().split()
    is_admin = hoshino.priv.check_priv(ev, hoshino.priv.ADMIN)

    if len(args) == 0:
        msg = HELP_MSG
    elif args[0] == 'help':
        msg = HELP_MSG
    elif args[0] == 'add':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2:
            msg = await rss_add(group_id, args[1])
        else:
            msg = '需要附带rss地址'
    elif args[0] == 'addb' or  args[0] == 'add-bilibili':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            rss_url = data['rsshub'] + '/bilibili/user/dynamic/' + str(args[1])
            msg = await rss_add(group_id, rss_url)
        else:
            msg = '需要附带up主id'
    elif args[0] == 'addr' or  args[0] == 'add-route':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2:
            rss_url = data['rsshub'] + args[1]
            msg = await rss_add(group_id, rss_url)
        else:
            msg = '需要提供route参数'
        pass
    elif args[0] == 'remove' or args[0] == 'rm':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            msg = rss_remove(group_id, int(args[1]))
        else:
            msg = '需要提供要删除rss订阅的序号'
    elif args[0] == 'list' or args[0] == 'ls':
        msg = rss_get_list(group_id)
    elif args[0] == 'mode':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            msg = rss_set_mode(group_id, args[1])
        else:
            msg = '需要附带模式(0/1)'
    else:
        msg = '参数错误'
    await bot.send(ev, msg)
    

#@sv.scheduled_job('cron', minute = '5,45-55,15-20', second='25')
@sv.scheduled_job('cron', second='30')
async def job():
    await group_process()

@sv.scheduled_job('cron', hour = '5' ,minute = '0', second='0')
async def clear_ngs_emg_time():
    data['ngs_emg_time'].clear()
    save_data()
