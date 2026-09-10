import vgamepad as vg
import time


class Controller:

    def __init__(self, gamepad):
        self.gamepad = gamepad

    def soft_reset(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        self.gamepad.update()

    def summary(self, option):

        self.press_start()

        time.sleep(.2)
        self.press_a()

        time.sleep(.9)
        self.press_a()

        time.sleep(.3)
        self.press_a()

        for i in range(1, option):
            time.sleep(.1)
            self.press_down()

    def run(self):
        self.press_down()

        time.sleep(.2)
        self.press_right()

        time.sleep(.2)
        self.press_a()

    def hold_b(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

    def release_b(self):
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

    def press_a(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()

    def press_b(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

    def press_start(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()

    def press_back(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()

    def press_up(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.gamepad.update()

    def press_down(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        self.gamepad.update()

    def press_left(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        self.gamepad.update()

    def press_right(self):
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        self.gamepad.update()
        time.sleep(.1)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        self.gamepad.update()
