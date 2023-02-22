from microbit import uart, sleep, button_a, button_b

uart.init(baudrate=115200)

while True:
    if button_a.is_pressed():
        uart.write('A')
    elif button_b.is_pressed():
        uart.write('B')
    else:
        uart.write('N')
    sleep(100)
