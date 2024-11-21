from pynput import keyboard
import pyperclip
import pyautogui
import time
import os
import re

variables = {}

def f_wait_for_keys_internal(key_combo):
    key_combo = key_combo.lower().split()
    keys_pressed = set()

    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char:
                keys_pressed.add(key.char.lower())
            elif hasattr(key, 'name') and key.name:
                keys_pressed.add(key.name.lower())
            
            if all(k in keys_pressed for k in key_combo):
                return False
        except Exception as e:
            print(f"Error in key listener: {e}")

    def on_release(key):
        try:
            if hasattr(key, 'char') and key.char:
                keys_pressed.discard(key.char.lower())
            elif hasattr(key, 'name') and key.name:
                keys_pressed.discard(key.name.lower())
        except Exception as e:
            print(f"Error in key listener: {e}")

    print(f"Waiting for keys: {' '.join(key_combo)}")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def f_evaluate_expression_internal(expression):
    try:
        resolved_expression = f_resolve_expression_internal(expression)
        return eval(resolved_expression, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {expression}. Error: {str(e)}")

def f_parse_wrapped_string_internal(arg):
    if arg.startswith('"') and arg.endswith('"'):
        return re.sub(r'\\(["\'])', r'\1', arg[1:-1])
    elif arg.startswith("'") and arg.endswith("'"):
        return re.sub(r'\\(["\'])', r'\1', arg[1:-1])
    return arg

def f_resolve_expression_internal(expression):
    try:
        expression = re.sub(
            r"\!\$\{\%clip\%\}",
            lambda m: pyperclip.paste(),
            expression
        )

        expression = re.sub(
            r"\$\{([^}]+)\}",
            lambda m: str(variables.get(m.group(1), "")),
            expression
        )

        expression = re.sub(
            r"\$\{~([^}]+)~\}",
            lambda m: str(os.getenv(m.group(1), "")),
            expression
        )

        expression = re.sub(
            r"\$\{\+([^}]+)\+\}",
            lambda m: str(os.getenv(m.group(1), "")),
            expression
        )

        return expression
    except Exception as e:
        raise ValueError(f"Error resolving expression: {expression}. Error: {str(e)}")


def f_set_variable_internal(var, value):
    if var.startswith("~") and var.endswith("~"):
        os.environ[var[1:-1]] = value
    elif var.startswith("+") and var.endswith("+"):
        os.system(f"setx {var[1:-1]} {value}")
    else:
        variables[var] = value

def f_join_variables_internal(*args):
    joined = " ".join(f_resolve_expression_internal(f"${{{arg}}}") for arg in args)
    return joined

def f_parse_internal(command):
    try:
        parts = command.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()

        def resolve_args(args):
            return [f_resolve_expression_internal(f_parse_wrapped_string_internal(arg)) for arg in args]

        if cmd == "cursor":
            x = int(f_evaluate_expression_internal(parts[1]))
            y = int(f_evaluate_expression_internal(parts[2]))
            pyautogui.moveTo(x, y)

        elif cmd == "key":
            key = f_resolve_expression_internal(parts[1].lower())
            action = parts[2].lower() if len(parts) > 2 else "press"
            if action == "down":
                pyautogui.keyDown(key)
            elif action == "up":
                pyautogui.keyUp(key)
            elif action == "press":
                pyautogui.press(key)

        elif cmd == "hotkey":
            combo = resolve_args(parts[1:])
            pyautogui.hotkey(*combo)

        elif cmd == "wait":
            if len(parts) > 2 and parts[-1].lower() in {"ms", "s", "sec", "seconds", "milliseconds"}:
                duration_expr = " ".join(parts[1:-1])
                unit = parts[-1].lower()
            else:
                duration_expr = " ".join(parts[1:])
                unit = "ms"

            duration = float(f_evaluate_expression_internal(duration_expr))

            if unit.startswith("ms"):
                time.sleep(duration / 1000)
            elif unit.startswith("s"):
                time.sleep(duration)

        elif cmd == "write":
            text = f_resolve_expression_internal(f_parse_wrapped_string_internal(" ".join(parts[1:])))
            pyautogui.write(text)

        elif cmd == "mb":
            button_map = {1: "left", 2: "right", 3: "middle", 4: "x1", 5: "x2"}
            button = button_map.get(int(f_resolve_expression_internal(parts[1])), "left")
            action = parts[2].lower() if len(parts) > 2 else "press"
            if action == "down":
                pyautogui.mouseDown(button=button)
            elif action == "up":
                pyautogui.mouseUp(button=button)
            elif action == "press":
                pyautogui.click(button=button)

        elif cmd == "scroll":
            amount = int(f_evaluate_expression_internal(parts[1]))
            pyautogui.scroll(amount)

        elif cmd == "clip":
            subcmd = parts[1].lower()
            if subcmd == "copy":
                text = f_resolve_expression_internal(f_parse_wrapped_string_internal(" ".join(parts[2:])))
                pyperclip.copy(text)
            elif subcmd == "paste":
                pyautogui.write(pyperclip.paste())
            elif subcmd == "clear":
                pyperclip.copy("")
            else:
                raise ValueError(f"Invalid clip action: {subcmd}")

        elif cmd == "set":
            var = parts[1]
            if parts[2].startswith("join(") and parts[2].endswith(")"):
                join_content = command[command.index("join(") + 5 : command.rindex(")")]
                args = [arg.strip() for arg in join_content.split(",")]
                value = f_join_variables_internal(*args)
            else:
                value = f_resolve_expression_internal(" ".join(parts[2:]))
            f_set_variable_internal(var, value)

        elif cmd == "del":
            var = parts[1]
            if var.startswith("~") and var.endswith("~"):
                os.environ.pop(var[1:-1], None)
            elif var.startswith("+") and var.endswith("+"):
                os.system(f"setx {var[1:-1]} ''")
            else:
                variables.pop(var, None)

        elif cmd == "continue":
            keys = resolve_args(parts[1:])
            f_wait_for_keys_internal(" ".join(keys))

        elif cmd == "log":
            message = f_resolve_expression_internal(f_parse_wrapped_string_internal(" ".join(parts[1:])))
            print(message)

    except Exception as e:
        print(f"Error processing command: {command}")
        print(f"Exception: {e}")

def f_parse_config_options_internal(script):
    config = {
        "DisableAdminVarWarning": False,
        "FuncSplit": ";",
        "CommentOverride": None,
    }
    new_script_lines = []

    for line in script.splitlines():
        line = line.strip()
        if line.startswith("@"):
            if line.lower() == "@disableadminvarwarning":
                config["DisableAdminVarWarning"] = True
            elif line.lower().startswith("@funcsplit ="):
                split_char = line.split("=", 1)[1].strip().strip('"')
                config["FuncSplit"] = split_char
            elif line.lower().startswith("@commentoverride ="):
                comment_char = line.split("=", 1)[1].strip().strip('"')
                config["CommentOverride"] = None if comment_char.lower() == "none" else comment_char
        else:
            new_script_lines.append(line)

    return config, "\n".join(new_script_lines)

def macro(execstr, echo_errors=True):
    try:
        if execstr is None:
            print("Input cannot be None")
            return

        config, cleaned_script = f_parse_config_options_internal(execstr)

        if not config["DisableAdminVarWarning"]:
            sys_var_pattern = r"set\s+\+([^\+]+)\+\s+"
            matches = re.findall(sys_var_pattern, execstr)
            if matches:
                print("WARNING: This script modifies system environment variables.")
                print("         These changes will only work if the program is run as administrator.")
                print(f"         Detected system variables: {', '.join(matches)}\n\n")

        commands = (
            cleaned_script.split(config["FuncSplit"])
            if config["FuncSplit"] != "\\n"
            else [line for line in cleaned_script.splitlines() if line.strip()]
        )

        for command in commands:
            if config["CommentOverride"] and config["CommentOverride"] in command:
                command = command.split(config["CommentOverride"], 1)[0].strip()

            if not command:
                continue

            f_parse_internal(command.strip())

    except Exception as e:
        if echo_errors:
            print(f"Error running macro:")
            print(f"Exception: {e}")