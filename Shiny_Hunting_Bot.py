# Python libraries
import vgamepad as vg
import threading
import time
import csv
import os

# Python Classes
from utilities.Controller import Controller
from utilities import Screenshot as Sc
from utilities import ImageProcessing as Ip
from utilities import Telegram as Tg

gamepad = vg.VX360Gamepad()


def main():

    routine = get_routine()


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

    while not stop_event.is_set():

        for elem in routine:
            match elem:
                case "a":
                    gp.press_a()
                case "b":
                    gp.press_b()
                case "reset":
                    gp.soft_reset()
                case "summary":
                    gp.summary()
                case _:
                    time.sleep(float(elem))

        time.sleep(1.5)

        Sc.screenshot_windows()

        result = Ip.is_shiny()

        i += 1

        print(f'{result} on try {i}\n\n')

        if result:
            Tg.send_message()
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

if __name__ == "__main__":

    while True:

        print("\nChoose an option:\n\t1. Take the screenshot\n\t2. Crop the screenshot\n\t3. Compute the "
              "distance\n\t4. Close the program\n\t5. Start the loop\n")
        x = input("Insert the number: ")

        match x:
            case "1":
                Sc.screenshot_windows()
            case "2":
                Ip.crop_pokemon()
            case "3":
                print(Ip.is_shiny())
            case "4":
                # noinspection PyProtectedMember
                os._exit(0)
            case "5":
                main()
                # noinspection PyProtectedMember
                os._exit(0)
