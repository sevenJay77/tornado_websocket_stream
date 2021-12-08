import os
import signal
import multiprocessing
from utils import logger
from pull_frame import PullFrameProcess
from redis_websocket_srv import WebsocketProcess

log = logger.get_logger(__file__)

# 任务列表
service_list = []

def service_start():
    for service in service_list:
        service.start()

def service_join():
    for service in service_list:
        service.join()


def exit_handler(signum, frame):
    os._exit(0)


def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    queue = multiprocessing.Queue()

    pull_srv = PullFrameProcess(queue)
    pull_srv.daemon = True
    service_list.append(pull_srv)

    web_srv = WebsocketProcess(queue)
    web_srv.daemon = True
    service_list.append(web_srv)


    # 任务开启
    service_start()
    service_join()


if __name__ == "__main__":
    main()
