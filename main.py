import serial
import time
import keyboard
import os
import sys
import json
import subprocess

COM_PORT = 'COM1'
BAUD_RATE = 115200
CONFIG_FILE = 'config.json'

COLORS = {
    "BLACK": 0x0000, "WHITE": 0xFFFF, "RED": 0xF800, "GREEN": 0x07E0,
    "BLUE": 0x001F, "CYAN": 0x07FF, "MAGENTA": 0xF81F, "YELLOW": 0xFFE0,
    "ORANGE": 0xFDA0, "PURPLE": 0x780F, "NAVY": 0x000F, "DARKGREEN": 0x03E0,
    "DARKCYAN": 0x03EF, "MAROON": 0x7800, "DARKGRAY": 0x3186
}

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"[!] Error loading {CONFIG_FILE}: {e}")
        return None

def sync_deck(ser, config_data):
    print("\n[?] Sending layout to Stream Deck...")
    for btn in config_data.get('buttons', []):
        b_id = btn.get('id', 0)
        label = btn.get('label', '')[:12]
        color_name = btn.get('color', 'BLUE').upper()
        color_val = COLORS.get(color_name, 0x001F)
        is_toggle = 1 if btn.get('isToggle', False) else 0
        
        cmd = f"CFG:{b_id}:{label}:{color_val}:{is_toggle}\n"
        ser.write(cmd.encode('utf-8'))
        time.sleep(0.05) 
        
    ser.write(b"CFG_DONE\n")
    print("[✔] Layout synced successfully!")

def handle_action(btn_id, config_data):
    button = next((b for b in config_data['buttons'] if b['id'] == btn_id), None)
    if button:
        print(f"[✔] Triggered [{button['label']}]")
        action_type = button.get('action_type', 'none')
        action = button.get('action', '')
        
        if action_type == 'hotkey' and action:
            keyboard.send(action)
        elif action_type in ['command', 'hold_command'] and action:
            try:
                if ".exe" in action.lower():
                    split_idx = action.lower().find(".exe") + 4
                    exe_path = action[:split_idx]
                    args = action[split_idx:].strip()
                    if args:
                        subprocess.Popen([exe_path] + args.split())
                    else:
                        os.startfile(exe_path)
                else:
                    os.system(action)
            except Exception as e:
                print(f"[!] Failed to launch '{button['label']}': {e}")

def main():
    active_holds = {}
    
    try:
        while True:
            print(f"\n[?] Awaiting Stream Deck connection on {COM_PORT}")
            
            while True:
                try:
                    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
                    time.sleep(3)
                    ser.reset_input_buffer()
                    print("[✔] Connected to ESP32!")
                    break
                except serial.SerialException:
                    time.sleep(2)

            config_data = load_config()
            if config_data:
                sync_deck(ser, config_data)

            try:
                while True:
                    if ser.in_waiting > 0:
                        raw_data = ser.readline().decode('utf-8').strip()
                        
                        if raw_data == "READY":
                            config_data = load_config() 
                            if config_data: sync_deck(ser, config_data)
                                    
                        elif raw_data.startswith("BTN_DOWN:"):
                            btn_id = int(raw_data.split(":")[1])
                            button = next((b for b in config_data['buttons'] if b['id'] == btn_id), None)
                            if button:
                                if button.get('action_type') == 'hold_command':
                                    active_holds[btn_id] = time.time()
                                    print(f"[?] Holding [{button['label']}]... Keep holding for 5 seconds!")
                                else:
                                    handle_action(btn_id, config_data) 
                                    
                        elif raw_data.startswith("BTN_UP:"):
                            btn_id = int(raw_data.split(":")[1])
                            if btn_id in active_holds:
                                print(f"[X] Hold cancelled for button (released too early).")
                                del active_holds[btn_id]

                        elif raw_data.startswith("BTN:"):
                            btn_id = int(raw_data.split(":")[1])
                            handle_action(btn_id, config_data)
                    
                    current_time = time.time()
                    for h_id, start_time in list(active_holds.items()):
                        if current_time - start_time >= 5.0:
                            button = next((b for b in config_data['buttons'] if b['id'] == h_id), None)
                            if button:
                                print(f"\n[✔] HOLD COMPLETE! Triggering [{button['label']}]...")
                                handle_action(h_id, config_data)
                            del active_holds[h_id] 
                    
                    time.sleep(0.01) 
                    
            except (serial.SerialException, OSError):
                print(f"\n[!] Stream Deck disconnected! (COM port vanished)")
                ser.close()
                active_holds.clear()
                time.sleep(1)
                
                continue 
            
    except KeyboardInterrupt:
        print("\n[X] Exiting script...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()