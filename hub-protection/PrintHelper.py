__author__ = 'omerturgeman'

import sys
from time import sleep

#speed = 0.02

class STATIC_DATA:
    LOW_DIM_VALUE = '030f00'
    HIGH_DIM_VALUE = 'ff0f00'

def print_clock_effect(first, last, speed):
    for x in range(0,3):
        sys.stdout.write('\r' + first + '|' + last)
        sys.stdout.flush()
        sleep(speed)
        sys.stdout.write('\r' + first + '/' + last)
        sys.stdout.flush()
        sleep(speed)
        sys.stdout.write('\r' + first + '-' + last)
        sys.stdout.flush()
        sleep(speed)
        sys.stdout.write('\r' + first + '\\' + last)
        sys.stdout.flush()
        sleep(speed)

def reaviling_string(heradline, secret_string, speed):
    for char_pos in range(0,len(secret_string)):
        print_input_first = heradline
        print_input_last = ""
        for i in range(0,char_pos):
            print_input_first += secret_string[i]
        for i in range(0, len(secret_string) - char_pos - 1):
            print_input_last += 'X'
        print_clock_effect(print_input_first, print_input_last, speed)
    sys.stdout.write('\r' + heradline + secret_string)
    print ""


def print_string_as_packet (headline, str_packet):
        import sys
        print headline + ":"
        new_line = True
        l = len(str_packet) + 2
        i = 0
        while i < l - 2:
            if not new_line:
                sys.stdout.write(" ")
            sys.stdout.write(str_packet[i:i+2])
            i += 2
            sys.stdout.write(" ")
            if i % 16 == 0:
                print ""
                new_line = True
            else:
                new_line = False
        print ""
