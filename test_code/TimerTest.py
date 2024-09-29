import threading
import logging
from threading import Thread

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s LEVEL:%(levelname)s FROM: %(filename)s '
                           'FROM_LINE: [%(lineno)d]  THREAD: %(threadName)s CONTENT:  %(message)s',
                    datefmt='[%d/%b/%Y %H:%M:%S]')

class Listener(Thread):
    def __init__(self, name:str):
        super().__init__()
        Thread.name = name
        self.timer = threading.Timer(5, self.handleTime)

    def handleTime(self):
        log.info(111)

    def start(self):
        self.timer.start()
        threading.Thread.start(self)

    def cancel(self):
        if self.timer:
            log.info("Cancelled timer %s" % self.timer.name)
            self.timer.cancel()

    def reset(self):
        if self.timer:
            log.info("try cancel %s" % self.timer.name)
            self.timer.cancel()
            log.info("reset timer")
            self.timer = threading.Timer(5, self.handleTime)


class Scanner(Thread):
    def __init__(self, background: Listener, name:str):
        super().__init__()
        Thread.name = name
        self.listener = background

    def run(self):
        log.info("Scanner is running, input quit to stop")
        flag = input()
        while flag == 'quit':
            log.info("Scanner is running, input quit to stop")
            flag = input()
            log.info("something input, restart listener!")
            self.listener.reset()


if __name__ == '__main__':
    listener = Listener('listener')
    thread = Scanner(listener, 'scanner')
    listener.start()
    thread.start()
    while True:
        pass
