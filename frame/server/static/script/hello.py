import time

from service.controller.sub_controller.client import *


def main(gc: GameClient):
    while True:
        gc.info(f'hello client')
        gc.check_stop()
        time.sleep(1)
