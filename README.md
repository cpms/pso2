# 概述
基于 [rss 订阅插件](https://github.com/zyujs/rss)魔改而来的 PSO2NGS（梦幻之星 ONLINE2 新纪元）HoshinoBot V2 插件，主要功能：
* 推送 NGS 和 PSO2 的紧急预告信息
* 推送 NGS 异常天气通知
* 通知信息经过格式化，翻译成中文并且时间自动转换成北京时间
* 记录 NGS 紧急任务的发生时间
* 获取每日土豆
* PSO2 日文验证码识别（使用 [pso2s.com](http://pso2s.com) 提供的服务）

本插件使用 RSSHub 来订阅推特的紧急预告信息，默认使用网上公开的 RSSHub 服务器，建议有条件的可以自行搭建

如自行搭建 RSSHub，需要申请推特开发者权限并配置好 RSSHub 来订阅推特的信息，详见 [RSSHub 官方文档](https://docs.rsshub.app/install/#pei-zhi-bu-fen-rss-mo-kuai-pei-zhi)

由于旧 PSO2 已经停止更新，本插件主要维护 NGS 相关的功能

**下载推特的土豆图需要配置科学上网，自行搭建的 RSSHub 也需要科学上网才可以访问推特的 API，详见 [RSSHub 官方文档](https://docs.rsshub.app/install/#pei-zhi-dai-li-pei-zhi)**

# 安装
1. 在 HoshinoBot 的 `modules` 目录下克隆`git clone https://github.com/cpms/pso2.git`
2. 进入 `pso2` 目录，安装依赖 `pip install -r requirements.txt`
3. 修改 HoshinoBot 的配置文件 `config/__bot__.py`，在加载的模块列表中按照格式添加 `pso2`
4. **启动然后关闭** HoshinoBot，在插件文件夹会生成数据文件 `data.json`，打开这个文件，将 `proxy` 的值修改为自己的代理服务器地址
5. 再次启动 HoshinoBot

# 初始化
在需要提供服务的Q群使用命令订阅以下链接（注意订阅链接有更新）

分别是 **NGS 紧急通知**、**NGS 土豆图**、**PSO2 紧急通知**、**NGS 异常天气通知**

**NGS 异常天气通知推特那边更新也不是特别及时，有时候延迟几分钟，感觉实用性不是很强，请酌情选择订阅**
```
pso2cmd add https://rss.shab.fun/twitter/user/PSO2NGS_JP
pso2cmd add https://rss.shab.fun/twitter/user/YukiPikochi?filter=%23アルファリアクター
pso2cmd add https://rss.shab.fun/twitter/user/pso2_emg_hour
pso2cmd add https://rss.shab.fun/twitter/user/Pso2ngsB?filter=%E7%95%B0%E5%B8%B8%E6%B0%97%E8%B1%A1%E9%80%9A%E7%9F%A5
```
**因为本插件针对以上信息源进行定制解析，所以不建议使用本插件订阅其他 RSS 源**

# 命令
* `pso2cmd list` : 查看订阅列表
* `pso2cmd add rss地址 `: 添加rss订阅
* `pso2cmd remove 序号` : 删除订阅列表指定项
* `今日土豆`：发送最新土豆图
* `今日土豆细节`：发送最新土豆细节图
* `最近紧急`：发送最近一次 NGS 紧急任务的发生时间
* `紧急记录`：发送今日 NGS 紧急任务的时间记录
* `验证码识别`：在此关键词后面接上 SEGA 的验证码图片，尝试进行识别

# 鸣谢
rss 订阅插件原作者[@zyujs](https://github.com/zyujs)

本插件默认使用的 RSSHub 服务器 [rss.shab.fun](http://rss.shab.fun/)

PSO2NGS紧急预告机器人[@PSO2NGS 15分前緊急予告BOT](https://twitter.com/PSO2NGS_JP)

PSO2紧急预告机器人[@PSO2 １時間前緊急予告BOT](https://twitter.com/pso2_emg_hour)

NGS 异常天气通知[@PSO2 NGS Bot](https://twitter.com/Pso2ngsB)

提供每日土豆的推主[@ピコチ](https://twitter.com/YukiPikochi)

PSO2 日文验证码识别服务 [pso2s.com](http://pso2s.com)

# 许可
本插件以 GPL-v3 协议开源
