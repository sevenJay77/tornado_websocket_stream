# tornado_websocket_stream

**A web RTSP play platform based on websocket and tornado,  websocket use blob binaryType read as ArrayBuffer**

#### 功能介绍

* Opencv解码 RTSP流，通过websocket 在Web端显示。
* websocket使用Blob binaryType， ArrayBuffer数据格式， 读取为base64在前端显示
* Websocket基于 Tornado
* 多进程解码RTSP流，通过queue通信。一个进程解码帧信息，一个进程读取队列帧信息


#### 运行环境

`
Python3.6+
`

#### pip安装

`
pip3 install -r requirements.txt
`


#### 使用

1. 修改 config.ini 配置信息：端口号、RTSP流地址
2. 启动脚本 python3 main.py
3. 打开浏览器 http://localhost:{port}

