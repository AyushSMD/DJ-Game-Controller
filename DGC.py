import rtmidi
import vgamepad as vg
import time

# Fine tuning variables
smoothing_factor = 0.2
ddj_port_index = 0

# left joystick's x axis
right_jog_control_touch = 54
right_jog_status_touch = 145
right_jog_control_rotatoion = 34
right_jog_status_rotatoion = 177
steering_sensitivity = 0.5 

# right trigger
right_fader_status = 177
right_fader_control = 19

# right trigger
left_fader_status = 176
left_fader_control = 19

# Initialize MIDI input
midiin = rtmidi.MidiIn()
ports = midiin.get_ports()
print("Available MIDI Ports:", ports)

# Select DDJ-RB port (adjust index if needed)
midiin.open_port(ddj_port_index)

# Initialize virtual gamepad
gamepad = vg.VX360Gamepad()

# Steering state
steering_value = 0.0  # -1.0 (left) to +1.0 (right)
touch_active = False

# Fader smoothing
last_accel = 0.0
last_brake = 0.0

def handle_midi_message(message, delta_time):
    global touch_active, steering_value, last_accel, last_brake

    msg, _ = message
    status, control, value = msg[0], msg[1], msg[2]

    # print (msg) # <-------------------------uncomment this line for the messages 

    # --- Steering ---
    # Jog touch on/off
    if control == right_jog_control_touch and status == right_jog_status_touch: 
        touch_active = (value > 0)
        if not touch_active:
            steering_value = 0.0
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
            print("Touch released -> Centered")

    # Jog rotation
    elif control == right_jog_control_rotatoion and touch_active and status == right_jog_status_rotatoion:  
        delta = (value - 64) / 64.0  
        steering_value += delta * steering_sensitivity 
        steering_value = max(-1.0, min(1.0, steering_value))
        gamepad.left_joystick_float(x_value_float=steering_value, y_value_float=0.0)
        gamepad.update()
        print(f"Steering: {steering_value:.2f}")

    # --- Acceleration ---
    # Right fader
    if control == right_fader_control and status == right_fader_status:  
        # Invert fader if top = max acceleration physically
        # value = 127 - value  # comment out if fader already goes 0->bottom,127->top

        accel = value / 127.0

        if abs(accel - last_accel) < 0.01:
            accel = last_accel  # ignore tiny fluctuations
        accel = last_accel * (1 - smoothing_factor) + accel * smoothing_factor
        last_accel = accel

        gamepad.right_trigger_float(value_float=accel)
        gamepad.update()

        print(f"Accel: {accel:.2f}")
        

    # --- Brake ---
    # left fader
    if control == left_fader_control and status == left_fader_status:  
        brake = value / 127.0

        if abs(brake - last_brake) < 0.01:
            brake = last_brake  # ignore tiny fluctuations
        brake = last_brake * (1 - smoothing_factor) + brake * smoothing_factor
        last_brake = brake

        gamepad.left_trigger_float(value_float=1-brake)
        gamepad.update()

        print(f"brake: {1-brake:.2f}")

    # --- Gears ---
    if control == 12 and status == 145:
        if value > 0:  # press
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            gamepad.update()
            print("Gear up pressed")
        else:  # release
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            gamepad.update()
            print("Gear up released")

    if control == 11 and status == 145:
        if value > 0:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            gamepad.update()
            print("Gear down pressed")
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            gamepad.update()
            print("Gear down released")




# Main loop
print("Listening for DDJ-RB input... (Ctrl+C to quit)")
try:
    while True:
        msg = midiin.get_message()
        if msg:
            handle_midi_message(msg, 0)
        time.sleep(0.001)
except KeyboardInterrupt:
    print("\nExiting...")
