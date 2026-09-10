# Python libraries
import random

import vgamepad as vg
import threading
import time
import csv
import os

# Python Classes
from utilities.Constant import SCREENSHOT_PATH
from utilities.Controller import Controller
from utilities import Screenshot as Sc
from utilities import ImageProcessing as Ip
from utilities import Telegram as Tg

gamepad = vg.VX360Gamepad()


def main():

    routine = get_routine()
    stop = False


    with open(os.path.join("csv", "stats.csv"), "r") as f:
        reader = csv.reader(f)
        row = next(reader)

        i = int(row[0])

    gp = Controller(gamepad)

    stop_event = threading.Event()
    listener_thread = threading.Thread(target=listen_for_stop, args=(stop_event,), daemon=True)
    listener_thread.start()

    print("Virtual controller connected. Starting in 3 seconds...")

    time.sleep(3)

    if routine[0] == "hold_b":
        routine.remove("hold_b")
        gp.hold_b()

    while not stop_event.is_set():

        for elem in routine:
            match elem:
                case "a":
                    gp.press_a()
                case "b":
                    gp.press_b()
                case "reset":
                    gp.soft_reset()
                case "left":
                    gp.press_left()
                case "right":
                    gp.press_right()
                case "up":
                    gp.press_up()
                case "down":
                    gp.press_down()
                case "fight_check":
                    Sc.screenshot_windows()
                    if Ip.is_battle():

                        if os.path.exists(SCREENSHOT_PATH):
                            os.remove(SCREENSHOT_PATH)

                        time.sleep(2.8)
                        Sc.screenshot_windows()

                        i += 1
                        result = Ip.is_shiny_fight()
                        print(f'{result} on try {i}\n\n')

                        if result:
                            Tg.send_message(i)
                            stop = Tg.fight_commands(gamepad)

                        else:
                            time.sleep(1)
                            gp.press_a()
                            time.sleep(3)
                            gp.run()
                            time.sleep(1)
                            gp.press_a()
                            time.sleep(1.5)

                case _ if "summary" in elem:
                    gp.summary(int(elem[8:]))

                    time.sleep(1.5)
                    Sc.screenshot_windows()
                    result = Ip.is_shiny_summary()

                    i += 1
                    print(f'{result} on try {i}\n\n')
                    if result:
                        Tg.send_message(i)
                        stop = True
                case _ if "random" in elem:
                    time.sleep(float(elem[7:]) + random.uniform(0, 1))
                case _ if "sleep" in elem:
                    time.sleep(float(elem[6:]))
                case _:
                    pass

        if stop:
            break


    with open(os.path.join("csv", "stats.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow([i])


def listen_for_stop(stop_event):
    input("Press ENTER to stop the loop\n")
    stop_event.set()


def get_routine():
    dictionary = {}

    with open(os.path.join("csv", "routines.csv"), "r") as f:
        routines = csv.reader(f)
        next(routines)
        for row in routines:
            dictionary[row[0]] = row[1]

    routine = -1
    while isinstance(routine, int):
        print("\nChoose which routine to use:")

        i = 1
        for keys in dictionary.keys():
            print(f'\t{i}. {keys}')
            i += 1

        routine = int(input()) - 1
        if 0 <= routine < len(dictionary):
            routine = list(dictionary.values())[routine]
        else:
            print("The number does not correspond to any routine")

    routine = routine.split()
    return routine

def addRoutine():
    routine_name = input("Insert the name of the routine: ").strip()

    print("Write 'end' to stop")
    commands = []

    while True:
        temp = input("Insert the command without spaces: ").strip()
        if temp == "end":
            break
        if temp:
            commands.append(temp)

    commands_str = " ".join(commands)

    os.makedirs("csv", exist_ok=True)

    with open(os.path.join("csv", "routines.csv"), "a") as f:
        writer = csv.writer(f)
        writer.writerow([routine_name, commands_str])

if __name__ == "__main__":

    while True:

        print("\nChoose an option:\n\t1. Take the screenshot\n\t2. Crop the pokemon ( summary )\n\t3. Compute the "
              "distance\n\t4. Crop the text box ( fight )\n\t5. Check if a battle is ongoing\n\t6. Compute the number of white pixels"
              "\n\t7. Add a new routine\n\t8. Exit the program\n\t9. Start a new loop")
        x = input("Insert the number: ")

        match x:
            case "1":
                Sc.screenshot_windows()
            case "2":
                Ip.crop_pokemon()
            case "3":
                print(Ip.is_shiny_summary(0))
            case "4":
                Ip.mask_textbox_white()
            case "5":
                print(Ip.is_battle())
            case "6":
                print(Ip.is_shiny_fight())
            case "7":
                addRoutine()
            case "8":
                # noinspection PyProtectedMember
                os._exit(0)
            case "9":
                main()
                # noinspection PyProtectedMember
                os._exit(0)
