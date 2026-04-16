import gpiozero
import sys
from subprocess import check_call
import getopt
from time import sleep

def parse_args(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except getopt.GetoptError:
        print ('on-off-controller.py -i <input gpio pin> -o <output gpio pin>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('on-off-controller.py -i <input gpio pin> -o <output gpio pin>')
            sys.exit()
        elif opt  == "-i":
            in_pin = arg
        elif opt == "-o":
            out_pin = arg

    return in_pin, out_pin

def run(in_pin, out_pin):

    output = gpiozero.OutputDevice(out_pin)

    off_button = gpiozero.Button(in_pin)

    output.on()

    while off_button.is_pressed:
        print("Button is pressed! Waiting for it not to be.")
        sleep(1)

    off_button.wait_for_press()

    output.off()
    check_call(['sudo', 'poweroff'])

if __name__ == "__main__":
   in_pin, out_pin = parse_args(sys.argv[1:])
   run(in_pin, out_pin)