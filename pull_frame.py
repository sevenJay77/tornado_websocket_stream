import cv2
import os
import time
from multiprocessing import Process
from imutils.video import FileVideoStream
import numpy as np
from utils import logger
from config import CommonConfig

log = logger.get_logger(__file__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "frame")


class PullFrameProcess(Process):

    def __init__(self, queue):
        super(PullFrameProcess, self).__init__()
        self.queue = queue
        self.url = CommonConfig.rtsp_url
        self.exit_flag = 0
        self.redis_client = None

    def __del__(self):
        pass

    def run(self):
        log.info("start pull rtsp")
        vc = FileVideoStream(self.url).start()
        time.sleep(1)
        while self.exit_flag == 0:
            try:
                frame = vc.read()
                _, image = cv2.imencode('.jpg', frame)
                self.queue.put(np.array(image).tobytes())
            except Exception as e:
                log.error("read frame error {}".format(e))
            cv2.waitKey(1)
        vc.release()

    def stop(self):
        self.exit_flag = 1



