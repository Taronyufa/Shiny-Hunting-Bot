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

    def summary(self):

        self.press_start()

        time.sleep(.2)
        self.press_a()

        time.sleep(.9)
        self.press_a()

        time.sleep(.3)
        self.press_a()

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
