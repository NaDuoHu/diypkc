## 更新记录

- 2022.8.15
  - 自改pkc监控：
  - 监控解析需要自行修改user.py转发频道
  - 去除多余无用插件
  - 监控变量当日去重，需根据青龙版本自行修改user.py路径

```bash
首次更新方式：
1、以发送机器人命令方式：
# 下载自定义监控配置文件 jk.json
/cmd cd /ql/config && wget https://raw.githubusercontent.com/curtinlv/gd/main/conf/jk.json
# 更新user.py
/cmd cd /ql/jbot/user && rm -f user.py  && wget https://raw.githubusercontent.com/curtinlv/gd/main/user/user.py
# 更新 utils.py
/cmd cd /ql/jbot/diy && rm -f utils.py  && wget https://raw.githubusercontent.com/curtinlv/gd/main/diy/utils.py
# 重启机器人生效
/restart

2.ssh进入容器方式：
# 下载自定义监控配置文件 jk.json
cd /ql/repo/gd && git pull  && cp -a /ql/repo/gd/conf/jk.json /ql/config
# 更新user.py
rm -f /ql/jbot/user/user.py && cp -a /ql/repo/gd/user/user.py /ql/jbot/user/user.py
# 更新 utils.py
rm -f /ql/jbot/diy/utils.py && cp -a /ql/repo/gd/diy/utils.py /ql/jbot/diy/utils.py
# 重启机器人生效
pm2 restart jbot


PS：后续只需修改 jk.json 配置文件，自己定义变量监控和应对执行脚本即可。修改完，需重启机器人生效。