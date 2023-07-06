要使用 Discord 进行紧急任务推送，需要申请 BOT token，有几个步骤要进行

1. 登录 Discord 创建一个服务器
   
2. 在服务器里创建一个文本频道
   
3. 将[此频道](https://discord.com/channels/1048264948935053422/1048265963478462485)的消息转发到自己刚创建的文本频道（点击下方的关注）
   
4. 访问 [Discord 开发者页面](https://discord.com/developers/applications)，点击右上角的 `New Application` 创建一个应用程序

![image](https://github.com/cpms/pso2/assets/4178287/9480a0dc-5bb1-4640-aeed-8bd26e0460be)

5. 获取 token，注意保存下来，以后只能重置无法再次查看

![image](https://github.com/cpms/pso2/assets/4178287/f2c474dc-de4b-479c-9e3a-de5381ba0e19)

6. 往下拉，进行权限设置

![image](https://github.com/cpms/pso2/assets/4178287/ec06b4b2-4d89-4c3d-a796-f94eb231152a)

7. 生成 BOT 邀请链接
   
![image](https://github.com/cpms/pso2/assets/4178287/a7d012ca-622f-4068-849f-68b0b2a04f25)

8. 往下拉，复制生成的链接，然后浏览器访问

![image](https://github.com/cpms/pso2/assets/4178287/afc0cbf8-422d-4123-b90e-e4bba91af77b)

9. 将刚创建的机器人加入自己的服务器

![image](https://github.com/cpms/pso2/assets/4178287/1a33588b-734b-4686-8992-463df14fa61b)

10. 编辑插件的配置文件 `data.json`，找到 `discord_token` 字段，将刚才获取的 token 写入（记得一定要配置代理服务器 `proxy` 字段，否则 Discord 服务器无法连接）
 
11. 启动 `Hoshino`，观察日志是否有 Discord 用户成功登录字样。如果登录成功，可以在频道看到机器人已经在线
 
12. 在文本频道发送 `ping`，如果一切正常，机器人会响应 `pong`

13. 在要启用推送的QQ群，发送命令 `pso2cmd ngs_emg_push enable` 启动该群的推送功能（需要管理员权限）

至此配置已经完成，需要了解任务订阅at功能以及其他功能，在QQ群发送 `pso2cmd help` 查看帮助
