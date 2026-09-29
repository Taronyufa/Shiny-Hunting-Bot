# Python libraries
import vgamepad as vg
import threading
import argparse
import random
import time
import csv
import os


# Python Classes
from shiny_hunting_bot.utilities.Constant import SCREENSHOT_PATH
from shiny_hunting_bot.utilities.Controller import Controller
from shiny_hunting_bot.utilities import ImageProcessing as Ip
from shiny_hunting_bot.utilities import Screenshot as Sc
from shiny_hunting_bot.utilities import Telegram as Tg

gamepad = vg.VX360Gamepad()


def main():
    args = parse_arg()

    if args.debug:
        while True:

            print("\nChoose an option:\n\t1. Take the screenshot\n\t2. Crop the pokemon ( summary )\n\t3. Compute the "
                  "distance\n\t4. Crop the text box ( fight )\n\t5. Check if a battle is ongoing\n\t6. Compute the number of white pixels"
                  "\n\t7. Add a new routine\n\t8. Exit the program\n")
            x = input("Insert the number: ")

            match x:
                case "1":
                    Sc.screenshot_windows()
                case "2":
                    Ip.crop_pokemon_summary()
                case "3":
                    print(Ip.is_shiny_summary(0))
                case "4":
                    Ip.mask_textbox_white()
                case "5":
                    print(Ip.is_battle())
                case "6":
                    print(Ip.is_shiny_fight())
                case "7":
                    add_routine()
                case "8":
                    # noinspection PyProtectedMember
                    os._exit(0)

    elif args.showroutines:
        toString_routines()

    elif args.routine is not None:
        loop(args.routine - 1)


def loop(routine):

    stop = False
    routine = get_routine(routine)


    with open(os.path.join("shiny_hunting_bot/config", "stats.csv"), "r") as f:
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
                    Sc.screenshot_linux()
                    if Ip.is_battle():

                        if os.path.exists(SCREENSHOT_PATH):
                            os.remove(SCREENSHOT_PATH)

                        time.sleep(2.8)
                        Sc.screenshot_linux()

                        i += 1
                        result = Ip.is_shiny_fight()
                        print(f'{result} on try {i}\n\n')

                        if result:
                            Tg.send_message(i)
                            stop = Tg.fight_commands(gamepad)

                        else:
                            time.sleep(1)
                            gp.press_a()
                            time.sleep(4)
                            gp.run()
                            time.sleep(1)
                            gp.press_a()
                            time.sleep(1.5)

                case _ if "summary" in elem:
                    gp.summary(int(elem[8:]))

                    time.sleep(1.5)
                    Sc.screenshot_linux()
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


    with open(os.path.join("shiny_hunting_bot/config", "stats.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow([i])


def listen_for_stop(stop_event):
    input("Press ENTER to stop the loop\n")
    stop_event.set()


def toString_routines():
    dictionary = {}

    with open(os.path.join("shiny_hunting_bot/config", "routines.csv"), "r") as f:
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

def get_routine(n):
    dictionary = {}

    with open(os.path.join("shiny_hunting_bot/config", "routines.csv"), "r") as f:
        routines = csv.reader(f)
        next(routines)
        for row in routines:
            dictionary[row[0]] = row[1]

    if 0 <= n < len(dictionary):
        routine = list(dictionary.values())[n]
    else:
        print("The number does not correspond to any routine")
        os._exit(0)

    routine = routine.split()
    return routine

def add_routine():
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

    with open(os.path.join("shiny_hunting_bot/config", "routines.csv"), "a") as f:
        writer = csv.writer(f)
        writer.writerow([routine_name, commands_str])

def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug")
    # parser.add_argument("-g", "--game", required=True) for later support to more games
    parser.add_argument("-r", "--routine", type=int)

    parser.add_argument("--showroutines")

    args = parser.parse_args()

    if not (args.debug or args.routine is not None or args.showroutines):
        parser.error("at least one of -d/--debug, -r/--routine, --showroutines is required")

    return args

if __name__ == "__main__":
    main()