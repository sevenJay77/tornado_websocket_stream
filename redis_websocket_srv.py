from multiprocessing import Process
import threading
import time
import tornado
import asyncio
import os
from tornado import ioloop, web, websocket, httpclient, gen
from utils import logger
from config import CommonConfig

log = logger.get_logger(__file__)


# 配置tornado web应用
class Application(tornado.web.Application):
    def __init__(self, queue):

        handlers = [
            (r"/", IndexHandler),
            (r"/ws", ImageWebSocketHandler),
        ]

        settings = dict(
            xheaders=True,
            websocket_ping_interval=10,
            websocket_ping_timeout=30,
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # 读取帧信息
        t = ImageThread(queue)
        t.setDaemon(True)
        t.start()



class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')



class ImageWebSocketHandler(websocket.WebSocketHandler):

    connections = []

    def __init__(self, *args, **kwargs):
        super(ImageWebSocketHandler, self).__init__(*args, **kwargs)

    @tornado.gen.engine
    def callback(self, message):
        self.write_message(message, True)

    def open(self):
        self.connections.append(self)
        log.info("join new client, time={}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        pass

    def on_close(self):
        self.connections.remove(self)
        log.info("close new client, time={}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True

    def on_ping(self, data):
        log.info('into on_pong the data is |%s|' % data)




# websocket服务线程
class WebsocketProcess(Process):
    def __init__(self, queue):
        super(WebsocketProcess, self).__init__()
        self.exit_flag = 0
        self.queue = queue
        self.port = CommonConfig.websocket_port

    def __del__(self):
        pass

    def stop(self):
        self.exit_flag = 1

    def run(self):
        log.info('start run app')
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = Application(self.queue)
        app.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()



# 读取帧信息
class ImageThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.exit_flag = 0
        self.queue = queue
        self._prev_image_id = None

    def __del__(self):
        pass

    def start(self):
        threading.Thread.start(self)

    def stop(self):
        self.exit_flag = 1

    def run(self):
        tornado.ioloop.IOLoop.instance()

        log.info("start notify framework")
        while not self.exit_flag:
            try:
                qsize = self.queue.qsize()
                if qsize > 0:
                    image = self.queue.get()
                    for connection in ImageWebSocketHandler.connections:
                        connection.callback(image)
                else:
                    time.sleep(0.001)
            except Exception as e:
                log.error(e)
