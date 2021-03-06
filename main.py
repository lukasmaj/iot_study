import os, time, time
import gpio
import subprocess
import threading

HOTMAIL_CONFIG_FILE = "/home/pi/config/msmtprc_hotmail"
GMAIL_CONFIG_FILE = "/home/pi/config/msmtprc_gmail"
SENSOR_PIN = 26
ON_OFF_PIN = 20



class Pins(threading.Thread):
    def __init__(self, pin, delay):
        threading.Thread.__init__(self)
        self.pin = pin
        self.on = False
        self.delay = delay
    def run(self):
        while True:
            prev_state = self.on 
            if gpio.check_state([self.pin]) == 1:
                self.on = True
                if prev_state:
                    time.sleep(self.delay)

    def state(self):
        ret = self.on
        self.on = False
        return ret

class StateMachine:
    def __init__(self):
        self.state = False
        print "Minitor OFF"

    def change_state(self):
        if self.state:
            self.state = False
            print "Turn OFF"
        else:
            self.state = True
            print "Turn ON"
        time.sleep(2)
    def onMonitoring(self):
        return self.state

class IoTProject:
    def __init__(self, email_list):
        self.email_list = email_list
        #self.primary_connection = "gmail"
        self.primary_connection = "hotmail"
        self.state_machine = StateMachine() 

    def runObserver(self):
        if not gpio.is_enable_pin(SENSOR_PIN):
            gpio.use_pin([SENSOR_PIN])
        if not gpio.is_enable_pin(ON_OFF_PIN):
            gpio.use_pin([ON_OFF_PIN])
        on_pin = Pins(ON_OFF_PIN, 2)
        on_pin.start()
        sensor_pin = Pins(SENSOR_PIN, 10)
        sensor_pin.start()
        while True:
            #if gpio.check_state([ON_OFF_PIN]) == 1:
            if on_pin.state():
                self.state_machine.change_state()
            
            if self.state_machine.onMonitoring():
                if sensor_pin.state():
                    self.__send_message()
                    time.sleep(5)
                self.__getReadySmtp()  
    
    def __getReadySmtp(self):
        cnt_fail = 0
        if self.primary_connection is "gmail":
            self.__chengeFile(GMAIL_CONFIG_FILE)
            if not self.__checkConnection("smtp.gmail.com"):
                self.primary_connection = "hotmail"
                cnt_fail = cnt_fail+1
                self.__chengeFile(HOTMAIL_CONFIG_FILE)
                time.sleep(1)

        if self.primary_connection is "hotmail":
            self.__chengeFile(HOTMAIL_CONFIG_FILE)
            if not self.__checkConnection("smtp.office365.com"):
                self.primary_connection = "gmail" 
                cnt_fail = cnt_fail+1
                self.__chengeFile(GMAIL_CONFIG_FILE)
                time.sleep(1)

        if cnt_fail > 1:
            assert False, "Cannot connect to any server"

    def __checkConnection(self, server):

        cmd = ["ping {0} -c 3".format(server)]
        ret = self.__exe(cmd)
        if "Host Unreachable" in ret:
            return False
        else:
            return True

    def __send_message(self):
        for email in self.email_list:
            title = "Zaobserwowano ruch"
            body = "Twoja akcja jest wymagana!\n W twoim pomieszczeniu ktos jest! "
            message = "\nFrom:Monitor\nSubject:{0}\nTo:{1}\n\n{2}".format(title,email,body)
            if self.primary_connection == "gmail":
                message = "From:Monitor\nSubject:{0}\nTo:{1}\n\n{2}".format(title,email,body)
                cmd = "echo \"{0}\" | sendmail {1}".format(message, email)
            else:
                message = "\nFrom:Monitor\nSubject:{0}\nTo:{1}\n\n{2}".format(title,email,body)
                cmd = "echo -e \"{0}\" | sendmail {1}".format(message, email)
            #self.__exe(cmd)
            os.system(cmd)

    def __exe(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def __chengeFile(self, file):
        cmd = ["sudo cp {0} /etc/msmtprc".format(file)]
        self.__exe(cmd)

if __name__ == "__main__":
    email_list=["p4tmarc@gmail.com", "majkowski.lukasz.gm@gmail.com", "testowe.konto.lukasz@gazeta.pl"]
    iot_proj = IoTProject(email_list=email_list)
    iot_proj.runObserver()