import subprocess
import shlex
import os

class Gpio:
    def __init__(self):
        pass
    
    def __exe(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def set_pin(self, pin):
        path = "/sys/class/gpio/gpio{0}/value".format(pin)
        cmd = ["echo 1 > {0}".format(path)]
        self.__exe(cmd)

    def clear_pin(self, pin):
        path = "/sys/class/gpio/gpio{0}/value".format(pin)
        cmd = ["echo 0 > {0}".format(path)]
        self.__exe(cmd)

    def set_as_output(self,pin):
        path = "/sys/class/gpio/gpio{0}/direction".format(pin)
        cmd = ["echo out > {0}".format(path)]
        self.__exe(cmd)

    def is_enable_pin(self, pin):
        path = "/sys/class/gpio/gpio{0}".format(pin)
        if os.path.exists(path):
            return True
        else:
            return False

    def use_pin(self, pin_list):
        for pin in pin_list:
            cmd  = ["echo {0} > /sys/class/gpio/export".format(pin)]
            self.__exe(cmd)

    def unuse_pin(self, pin_list):
        for pin in pin_list:
            cmd  = ["echo {0} > /sys/class/gpio/unexport".format(pin)]
            self.__exe(cmd)

    def check_state(self, pin_list):
        ret = 0
        i = 0
        for pin in pin_list:
            gpio = "gpio{0}".format(pin)
            cmd = ["cat /sys/class/gpio/{0}/value ".format(gpio)]
            out = self.__exe(cmd)
            ret = ret | (0x01&(int(out)<< i))
        return ret

__gpio = Gpio()
use_pin = __gpio.use_pin
unuse_pin = __gpio.unuse_pin
check_state = __gpio.check_state
is_enable_pin = __gpio.is_enable_pin
set_pin = __gpio.set_pin
clear_pin = __gpio.clear_pin
set_as_output = __gpio.set_as_output