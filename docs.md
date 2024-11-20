# PyMacro Documentation

Welcome to **PyMacro**, a flexible macro scripting system! This documentation covers all supported commands and their usage.

---

## Table of Contents

1. [General Syntax](#general-syntax)
2. [Command List](#command-list)
    - [Cursor Control](#cursor-control)
    - [Key Press](#key-press)
    - [Hotkey Combination](#hotkey-combination)
    - [Wait](#wait)
    - [Write Text](#write-text)
    - [Mouse Buttons](#mouse-buttons)
    - [Scrolling](#scrolling)
    - [Clipboard Management](#clipboard-management)
    - [Variable Management](#variable-management)
    - [Environment Variable Management](#environment-variable-management)
    - [Continue](#continue)
    - [Log](#log)
3. [Examples](#examples)
4. [Error Handling](#error-handling)

---

## General Syntax

- Commands are separated by semicolons (`;`).
- Arguments are separated by spaces.
- Variables can be defined and used in any command using `${var}`.
- Environment variables are referenced using `${~envvar~}`.

### Example

```plaintext
set x 100;
cursor ${x} 200;
wait 1 s;
clip copy Hello World;
```

---

## Command List

### Cursor Control

Move the mouse cursor to specific screen coordinates.

**Syntax**:
```plaintext
cursor {x} {y};
```

**Arguments**:
- `{x}`: Horizontal position in pixels.
- `{y}`: Vertical position in pixels.

**Example**:
```plaintext
cursor 500 300;
```

---

### Key Press

Simulate pressing or releasing a key.

**Syntax**:
```plaintext
key {key} [(press)/up/down];
```

**Arguments**:
- `{key}`: The key to press (e.g., `a`, `1`, `enter`).
- `(press)` (default): Press and release the key.
- `up`: Release the key.
- `down`: Hold the key down.

**Example**:
```plaintext
key a press;
key enter up;
```

---

### Hotkey Combination

Simulate pressing multiple keys simultaneously.

**Syntax**:
```plaintext
hotkey {key1} {key2} ... {keyN};
```

**Arguments**:
- `{keyN}`: Keys to press in combination.

**Example**:
```plaintext
hotkey f1 f2;
```

---

### Wait

Pause the macro for a specified duration.

**Syntax**:
```plaintext
wait {time} [(ms)/s/sec];
```

**Arguments**:
- `{time}`: Duration to wait.
- `(ms)` (default): Time in milliseconds.
- `(s/sec)`: Time in seconds.

**Example**:
```plaintext
wait 100 ms;
wait 2 s;
```

---

### Write Text

Type a string of text.

**Syntax**:
```plaintext
write {text};
```

**Arguments**:
- `{text}`: The text to type.

**Example**:
```plaintext
write Hello, World!;
```

---

### Mouse Buttons

Simulate mouse button actions.

**Syntax**:
```plaintext
mb {button} [(press)/up/down];
```

**Arguments**:
- `{button}`: Button index (1=Left, 2=Right, 3=Middle, 4=X1, 5=X2).
- `(press)` (default): Click the button.
- `up`: Release the button.
- `down`: Hold the button down.

**Example**:
```plaintext
mb 1 press;
```

---

### Scrolling

Simulate mouse wheel scrolling.

**Syntax**:
```plaintext
scroll {amount};
```

**Arguments**:
- `{amount}`: Number of units to scroll (positive for up, negative for down).

**Example**:
```plaintext
scroll -10;  # Scroll down
scroll 20;   # Scroll up
```

---

### Clipboard Management

Perform operations with the clipboard.

**Syntax**:
```plaintext
clip {copy/paste/clear} {text};
```

**Arguments**:
- `copy`: Copy the specified text to the clipboard.
- `paste`: Paste the current clipboard content.
- `clear`: Clear the clipboard.
- `{text}`: (Required for `copy`) The text to copy.

**Examples**:
```plaintext
clip copy Hello, World!;
clip paste;
clip clear;
```

---

### Variable Management

Define, use, and delete variables.

**Set a Variable**:
```plaintext
set {varname} {value};
```

- `{varname}`: Name of the variable.
- `{value}`: Can include math, other variables (`${var}`), or environment variables (`${~envvar~}`).

**Delete a Variable**:
```plaintext
del {varname};
```

**Examples**:
```plaintext
set x 10 + 5;
write The value is ${x};
del x;
```

---

### Environment Variable Management

Retrieve, set, or delete environment variables.

**Retrieve Environment Variable**:
```plaintext
${~envvar~};
```

**Set Environment Variable**:
```plaintext
write {user/sys} ~envvar~ {value};
```

- `user`: Set for the current user.
- `sys`: Set system-wide.
- `{value}`: Value to assign.

**Delete Environment Variable**:
```plaintext
del ~envvar~;
```

**Examples**:
```plaintext
set path ${~PATH~};
write user ~MY_ENV_VAR~ Hello;
del ~MY_ENV_VAR~;
```

---

### Continue

Pause the macro until a specific key or key combination is pressed.

**Syntax**:
```plaintext
continue {key};
```

**Arguments**:
- `{key}`: The key to wait for (e.g., `j`, `enter`, `f1`).

**Examples**:
```plaintext
continue j;
continue enter;
continue f1;
```

---

### Log

Print a message to the console.

**Syntax**:
```plaintext
log {message};
```

**Arguments**:
- `{message}`: The text to log.

**Examples**:
```plaintext
log Starting the macro!;
log Current variable value: ${x};
```

---

## Examples

**Example Script**:
```plaintext
set x 100;
log Starting macro execution;
cursor ${x} 200;
continue j;
log Detected key, moving forward;
clip copy Macro executed successfully!;
clip paste;
```

---

## Error Handling

Errors during command execution will output the command and the exception. Example:
```plaintext
Error processing command: set x ${undefined_var} + 1
Exception: Invalid expression: ${undefined_var}. Error: name 'undefined_var' is not defined
```