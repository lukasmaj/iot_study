import os, time, time
import gpio

SENSOR_PIN = 21

class IoTProject:
    def __init__(self, email_list):
        self.email_list = email_list

    def runObserver(self):
        if not gpio.is_enable_pin(SENSOR_PIN):
            gpio.use_pin([SENSOR_PIN])

        while True:
            if gpio.check_state([SENSOR_PIN]) == 1:
                self.__send_message()
                time.sleep(1000)  

    def __send_message(self):
        for email in self.email_list:
            title = "Monitor aktywnosci w pomieszczeniu"
            body = "Twoja akcja jest wymagana!\n W twoim pomieszczeniu ktos jest! "
            cmd = "echo \"{0}\" | mail -s \"{1}\" {2}".format(body, title, email)
            os.system(cmd)

if __name__ == "__main__":
    email_list=["p4tmarc@gmail.com", "majkowski.lukasz.gm@gmail.com"]
    iot_proj = IoTProject(email_list=email_list)
    iot_proj.runObserver()