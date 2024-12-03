

from machine import Pin, UART
import time
 
# Initialize UART for SIM800L communication
sim800l = UART(1, baudrate=9600, tx=8, rx=9)

# Initialize the button pin and internal LED pin
button = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(25, Pin.OUT)

# Function to send AT command and wait for a response
def send_at_command(command, wait=2000):
    sim800l.write(command + '\r\n')
    time.sleep_ms(wait)
    if sim800l.any():
        response = sim800l.read().decode('utf-8', 'ignore')
        print(f"Response: {response}")
        return response
    return ''

# Initialize SIM800L
def initialize_sim800l():
    print("Initializing SIM800L...")
    send_at_command("AT") 
    send_at_command("AT+CMGF=1")  

# Send SMS function
def send_sms(phone_number, message):
    print("Sending SMS...")
    send_at_command(f'AT+CMGS="{phone_number}"')
    sim800l.write(message + '\x1A')  
    time.sleep(3)
    print("Message sent.")

# Main code
initialize_sim800l()

# Phone number to send the SMS
phone_number = "+917010333087"

while True:
    if button.value() == 0:  
        pass
    else:
        print("Button pressed!")
        led.value(1)  # Turn on LED
        send_sms(phone_number, "Your fuel is in halfway to become 0%")
        time.sleep(5)  # Debounce delay
        led.value(0)  # Turn off LED