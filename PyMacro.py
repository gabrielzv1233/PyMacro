from pynput import keyboard
import pyperclip
import pyautogui
import time
import os
import re

variables = {}

pyautogui_key_mapping = {
    keyboard.Key.alt: 'alt',
    keyboard.Key.alt_l: 'altleft',
    keyboard.Key.alt_gr: 'altright',
    keyboard.Key.backspace: 'backspace',
    keyboard.Key.caps_lock: 'capslock',
    keyboard.Key.cmd: 'win',
    keyboard.Key.cmd_l: 'winleft',
    keyboard.Key.cmd_r: 'winright',
    keyboard.Key.ctrl: 'ctrl',
    keyboard.Key.ctrl_l: 'ctrlleft',
    keyboard.Key.ctrl_r: 'ctrlright',
    keyboard.Key.delete: 'delete',
    keyboard.Key.down: 'down',
    keyboard.Key.end: 'end',
    keyboard.Key.enter: 'enter',
    keyboard.Key.esc: 'esc',
    keyboard.Key.f1: 'f1',
    keyboard.Key.f2: 'f2',
    keyboard.Key.f3: 'f3',
    keyboard.Key.f4: 'f4',
    keyboard.Key.f5: 'f5',
    keyboard.Key.f6: 'f6',
    keyboard.Key.f7: 'f7',
    keyboard.Key.f8: 'f8',
    keyboard.Key.f9: 'f9',
    keyboard.Key.f10: 'f10',
    keyboard.Key.f11: 'f11',
    keyboard.Key.f12: 'f12',
    keyboard.Key.home: 'home',
    keyboard.Key.insert: 'insert',
    keyboard.Key.left: 'left',
    keyboard.Key.page_down: 'pagedown',
    keyboard.Key.page_up: 'pageup',
    keyboard.Key.pause: 'pause',
    keyboard.Key.right: 'right',
    keyboard.Key.scroll_lock: 'scrolllock',
    keyboard.Key.shift: 'shift',
    keyboard.Key.shift_l: 'shiftleft',
    keyboard.Key.shift_r: 'shiftright',
    keyboard.Key.space: 'space',
    keyboard.Key.tab: 'tab',
    keyboard.Key.up: 'up',
    keyboard.Key.media_next: 'nexttrack',
    keyboard.Key.media_play_pause: 'playpause',
    keyboard.Key.media_previous: 'prevtrack',
    keyboard.Key.media_volume_down: 'volumedown',
    keyboard.Key.media_volume_mute: 'volumemute',
    keyboard.Key.media_volume_up: 'volumeup',
}

# Add printable characters to the mapping
for char in (
    '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
    ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '{', '|', '}', '~'
):
    pyautogui_key_mapping[keyboard.KeyCode.from_char(char)] = char

def normalize_key(key):
    """Normalize a key to its PyAutoGUI-compatible name."""
    if key in pyautogui_key_mapping:
        return pyautogui_key_mapping[key]
    elif hasattr(key, 'char') and key.char:
        return key.char.lower()
    return None

def wait_for_keys(key_combo):
    """
    Wait for a specific key or key combination to be pressed.

    Args:
        key_combo (str): Space-separated key combination to wait for (e.g., "ctrl j").
    """
    key_combo = key_combo.lower().split()
    keys_pressed = set()

    def on_press(key):
        try:
            normalized_key = normalize_key(key)
            if normalized_key:
                keys_pressed.add(normalized_key)
            # Check if all keys in the combo are pressed
            if all(k in keys_pressed for k in key_combo):
                print(f"Keys detected: {' '.join(key_combo)}")
                return False
        except Exception as e:
            print(f"Error in key listener: {e}")

    def on_release(key):
        try:
            normalized_key = normalize_key(key)
            if normalized_key:
                keys_pressed.discard(normalized_key)
        except Exception as e:
            print(f"Error in key listener: {e}")

    print(f"Waiting for keys: {' '.join(key_combo)}")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def f_resolve_expression_internal(expression):
    try:
        
        expression = re.sub(r"\$\{([^}]+)\}", lambda m: str(variables.get(m.group(1), "")), expression)
        expression = re.sub(r"\$\{~([^}]+)~\}", lambda m: str(os.getenv(m.group(1), "")), expression)

        try:
            return eval(expression)  
        except:
            pass  

        return expression
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")

def f_parse_internal(command):
    try:
        parts = command.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        
        if cmd == "cursor":
            x, y = map(int, parts[1:3])
            pyautogui.moveTo(x, y)
        
        elif cmd == "key":
            key = parts[1].lower()
            action = parts[2].lower() if len(parts) > 2 else "press"
            if action == "down":
                pyautogui.keyDown(key)
            elif action == "up":
                pyautogui.keyUp(key)
            elif action == "press":
                pyautogui.press(key)
        
        elif cmd == "hotkey":
            combo = [key.lower() for key in parts[1:]]
            pyautogui.hotkey(*combo)
        
        elif cmd == "wait":
            duration = float(f_resolve_expression_internal(parts[1]))
            unit = parts[2].lower() if len(parts) > 2 else "ms"
            if unit.startswith("ms"):
                time.sleep(duration / 1000)
            elif unit.startswith("s"):
                time.sleep(duration)
        
        elif cmd == "write":
            text = f_resolve_expression_internal(command[6:].strip())
            pyautogui.write(text)
        
        elif cmd == "mb":
            button_map = {1: "left", 2: "right", 3: "middle", 4: "x1", 5: "x2"}
            button = button_map.get(int(parts[1]), "left")
            action = parts[2].lower() if len(parts) > 2 else "press"
            if action == "down":
                pyautogui.mouseDown(button=button)
            elif action == "up":
                pyautogui.mouseUp(button=button)
            elif action == "press":
                pyautogui.click(button=button)
        
        elif cmd == "scroll":
            amount = int(f_resolve_expression_internal(parts[1]))
            pyautogui.scroll(amount)

        elif cmd == "clip":
            subcmd = parts[1].lower()
            if subcmd == "copy":
                text = f_resolve_expression_internal(" ".join(parts[2:]))
                pyperclip.copy(text)
            elif subcmd == "paste":
                pyautogui.write(pyperclip.paste())
            elif subcmd == "clear":
                pyperclip.copy("")
            else:
                raise ValueError(f"Invalid clip action: {subcmd}")
        
        elif cmd == "set":
            varname = parts[1]
            value = f_resolve_expression_internal(" ".join(parts[2:]))
            variables[varname] = value
        
        elif cmd == "del":
            varname = parts[1]
            if varname.startswith("~") and varname.endswith("~"):  
                os.environ.pop(varname[1:-1], None)
            else:  
                variables.pop(varname, None)
        
        elif cmd == "write":
            if parts[1].startswith("user") or parts[1].startswith("sys"):
                scope, env_var = parts[1], parts[2]
                value = f_resolve_expression_internal(" ".join(parts[3:]))
                if scope == "user":
                    os.environ[env_var] = value
                elif scope == "sys":
                    os.system(f"setx {env_var} {value}")
        
        elif cmd == "continue":
            keys = " ".join(parts[1:])
            wait_for_keys(keys)

        
        elif cmd == "log":
            message = " ".join(parts[1:])  # Combine the rest of the parts as the log message
            print(message)

        
    except Exception as e:
        print(f"Error processing command: {command}")
        print(f"Exception: {e}")

def macro(execstr, echo_errors=True):
    try:
        if execstr == None:
            print("Input cannot be None")
        elif execstr != None:
            for command in execstr.split(";"):
                f_parse_internal(command)
    except Exception as e:
        if echo_errors == True:
            print(f"Error running macro:")
            print(f"Exception: {e}")