import rtmidi
import vgamepad as vg
import time

# Initialize MIDI input
midiin = rtmidi.MidiIn()
ports = midiin.get_ports()
print("Available MIDI Ports:", ports)

# Select DDJ-RB port (adjust index if needed)
ddj_port_index = 0
midiin.open_port(ddj_port_index)

# Initialize virtual gamepad
gamepad = vg.VX360Gamepad()

# Steering state
steering_value = 0.0  # -1.0 (left) to +1.0 (right)
touch_active = False

# Fader smoothing
last_accel = 0.0
last_brake = 0.0
smoothing_factor = 0.2

def handle_midi_message(message, delta_time):
    global touch_active, steering_value, last_accel, last_brake

    msg, _ = message
    status, control, value = msg[0], msg[1], msg[2]

    print (msg)

    # --- Steering ---
    if control == 54 and status == 145:  # Jog touch on/off
        touch_active = (value > 0)
        if not touch_active:
            steering_value = 0.0
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
            print("Touch released -> Centered")

    elif control == 34 and touch_active and status == 177:  # Jog rotation
        delta = (value - 64) / 64.0  # Normalize rotation delta (-1 to +1)
        steering_value += delta * 0.5  # Sensitivity
        steering_value = max(-1.0, min(1.0, steering_value))
        gamepad.left_joystick_float(x_value_float=steering_value, y_value_float=0.0)
        gamepad.update()
        print(f"Steering: {steering_value:.2f} Message: {msg}")

    # --- Acceleration ---
    if control == 19 and status == 177:  # Right fader
        # Invert fader if top = max acceleration physically
        # value = 127 - value  # comment out if fader already goes 0->bottom,127->top

        # Map fader to acceleration
        accel = value / 127.0

        # Optional brake at bottom
        # brake = 1.0 if value <= 117 else 0.0
        # if brake == 1.0:
        #     accel = 0.0

        # Smoothing to reduce jitter
        if abs(accel - last_accel) < 0.01:
            accel = last_accel  # ignore tiny fluctuations
        accel = last_accel * (1 - smoothing_factor) + accel * smoothing_factor
        last_accel = accel

        # Send to virtual gamepad
        gamepad.right_trigger_float(value_float=accel)
        # gamepad.left_trigger_float(value_float=brake)
        gamepad.update()

        # Print live values in terminal
        print(f"Accel: {accel:.2f}")
        

    # --- Brake ---
    if control == 19 and status == 176:  # left fader
        brake = value / 127.0

            # Map fader to acceleration
        

        # Optional brake at bottom
        # brake = 1.0 if value <= 117 else 0.0
        # if brake == 1.0:
        #     accel = 0.0

        # Smoothing to reduce jitter
        if abs(brake - last_brake) < 0.01:
            brake = last_brake  # ignore tiny fluctuations
        brake = last_brake * (1 - smoothing_factor) + brake * smoothing_factor
        last_brake = brake

        # Send to virtual gamepad
        gamepad.left_trigger_float(value_float=1-brake)
        # gamepad.left_trigger_float(value_float=brake)
        gamepad.update()

        # Print live values in terminal
        print(f"brake: {brake:.2f}")

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
