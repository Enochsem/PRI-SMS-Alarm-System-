from machine import Pin, PWM, UART
from sim808 import Message
import time, sys, neopixel



r=Pin(17)
t=Pin(16)
sp = UART(2,115200)                         # init with given baudrate
#sp.init(115200, bits=8, parity=None, stop=1,tx=r, rx=t)

np = neopixel.NeoPixel(Pin(21), 1)
led = Pin(19, Pin.OUT)
pir = Pin(22, Pin.IN, Pin.PULL_UP)
buzpin = Pin(18,Pin.OUT)
buzzer = PWM(buzpin)
buzzer.deinit()


def offrgb():
    np[0]=(0,0,0)
    np.write()
    print('off')
    
def onrgb():
    np[0]=(255,0,0)
    np.write()
    print('on')

def sendmsg():
    rcpt=str(0559275604)#Enter recipient number
    msgcnt=str('Intrudeer detected')#Enter message
    msg=Message(rcpt,msgcnt)
    msg.setTextMode()
    msg.sendMessage()

def short():
    for i in range(0,3):
        buzzer.duty(50)
        buzzer.freq(1760)
        led(1)
        onrgb()
        time.sleep_ms(500)
        led(0)
        offrgb()
        buzzer.duty(0)
        time.sleep_ms(200)

def long():
    for i in range(0,3):
        buzzer.duty(50)
        buzzer.freq(1760)
        led(1)
        onrgb()
        time.sleep(1)
        led(0)
        offrgb()
        buzzer.duty(0)
        time.sleep_ms(200)

def pirsensor(pir):    
    pirState = pir.value()
    print(pirState)
    time.sleep_ms(100)
    if pirState == 1:
        sendmsg()
        sos()
        print('buzzer and led sos call')
        buzzer.duty(0)
        print('Heat signature detected')
    else:
        led.off()
        offrgb()

def sos1():
    buzzer.init()
    short()
    long()
    short()       
    buzzer.duty(0)
    buzzer.deinit()
    
def buzz (buzz_freq, on_time, off_time):
    buzzer.init()
    buzzer.freq(buzz_freq)
    led(1)
    onrgb()
    time.sleep_ms(on_time)
    buzzer.duty(0)
    led(0)
    offrgb()
    time.sleep_ms(off_time)

def sos():
    for note in range(0,10):
        buzzer.duty(50)
        if note == 3 or note == 4 or note == 5:
            buzz (1760, 850, 200)
        else:
            buzz (1760, 500, 200)
    buzzer.duty(0)
    buzzer.deinit()



if __name__ == "__main__":
    try:
        pir.irq(trigger=3, handler=pirsensor)
    except KeyboardInterrupt:
        print('End')
        sys.exit(0)