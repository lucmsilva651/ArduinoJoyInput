import serial
import pynput 
import time

mouse = pynput.mouse.Controller()

# SETTINGS HERE
PORT = '/dev/ttyUSB0' # COM3 if on Windows, /dev/ttyUSB0 or /dev/ttyACM0 if on Linux
BAUD = 230400
TIMEOUT = 0.01
SENSI = 480.0
DEFAULT = (506, 497) # change this if your joystick center is different

# CHANGE IF YOU NEED RIGHT BTN INSTEAD OF LEFT
CLICK_BTN = pynput.mouse.Button.left
mouse_is_pressed = False # check if real mouse is being pressed

# SERIAL INIT
try:
    ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
except serial.SerialException as e:
    print(f"ERROR: Cannot open serial {PORT}: {e}")
    exit()

print(f"Reading at {BAUD}...")
print("-" * 50)

while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        
        if line:
            try:
                parts = line.split(',')
                if len(parts) == 3:
                    # button is Z value
                    joy_x, joy_y, button = map(int, parts)

                    # calc movt
                    delta_x = joy_x - DEFAULT[0]
                    delta_y = joy_y - DEFAULT[1]
                    mov_x = round(delta_x / SENSI)
                    mov_y = round(delta_y / SENSI)
                    
                    if mov_x != 0 or mov_y != 0:
                        mouse.move(mov_x, mov_y)
                    
                    if button == 1 and not mouse_is_pressed:
                        mouse.press(CLICK_BTN)
                        mouse_is_pressed = True
                        print("Button pressed (HOLD)")

                    elif button == 0 and mouse_is_pressed:
                        mouse.release(CLICK_BTN)
                        mouse_is_pressed = False
                        print("Button released (RELEASE)")

            except ValueError:
                pass
            except Exception as e:
                pass

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        break
    
    except serial.SerialTimeoutException:
        pass
    
    except Exception as e:
        print(f"ERROR while comm: {e}")
        time.sleep(0.1)

if 'ser' in locals() and ser.is_open:
    ser.close()
    print("Serial port closed.")
