# **PyMacro Documentation**

Created by [Gabriezv1233](https://github.com/gabrielzv1233)  

Welcome to **PyMacro**, a versatile and simple macro scripting system! This documentation covers all supported commands, configuration options, and usage.

You can find an example script loader at **scriptloader.py**.

Documentation by our savior ChatGPT (enhanced manually).

---

## **Table of Contents**

1. [General Syntax](#general-syntax)
2. [Configuration Options](#configuration-options)
3. [Command List](#command-list)
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
4. [Examples](#examples)
5. [Error Handling](#error-handling)

---

## **General Syntax**

- Commands are separated by semicolons (`;`) unless redefined by a configuration option.
- Arguments are separated by spaces.
- Variables can be defined and used in any command using `${var}`.
- Environment variables are referenced using `${~envvar~}` (user) or `${+envvar+}` (system).
- Clipboard content can be referenced as `!{%clip%}`.

---

## **Configuration Options**

Configuration options allow customization of how the macro script behaves. They must be defined at the start of the script and begin with `@`.

### **Available Options**

#### **1. `@DisableAdminVarWarning`**
Disables warnings when the script attempts to modify system environment variables.

**Example**:
```plaintext
@DisableAdminVarWarning
```

---

#### **2. `@FuncSplit = "char(s)"`**
Defines the character(s) used to split commands in the script. The default is `;`.

- Use `"\n"` to split commands by newlines, treating each non-blank line as a command.
- Use any custom character or string for splitting.

**Example**:
```plaintext
@FuncSplit = "\n"
set var1 Hello
set var2 World
log ${var1} ${var2}
```

---

#### **3. `@CommentOverride = "char(s)"`**
Defines the character(s) that mark the start of a comment. Text after the defined character(s) is ignored. The default is `None` (comments disabled).

**Example**:
```plaintext
@CommentOverride = "//"
set var1 Hello; // This is a comment
log ${var1}; // Another comment
```

**Disable Comments**:
```plaintext
@CommentOverride = "None"
set var1 Hello; # This will NOT be treated as a comment
```

---

## **Command List**

### **Cursor Control**

Move the mouse cursor to specific screen coordinates.

**Syntax**:
```plaintext
cursor {x} {y};
```

**Arguments**:
- `{x}`: Horizontal position in pixels. Supports math and variables.
- `{y}`: Vertical position in pixels. Supports math and variables.

**Examples**:
```plaintext
cursor 500 300;
cursor ${x} + 50 ${y} - 100;
```

---

### **Key Press**

Simulate pressing or releasing a key.

**Syntax**:
```plaintext
key {key} [(press)/up/down];
```

---

### **Hotkey Combination**

Simulate pressing multiple keys simultaneously.

**Syntax**:
```plaintext
hotkey {key1} {key2} ... {keyN};
```

---

### **Wait**

Pause the macro for a specified duration.

**Syntax**:
```plaintext
wait {time} [(ms)/s/sec];
```

**Examples**:
```plaintext
wait 1000 ms;
wait ${delay} * 2 s;
```

---

### **Write Text**

Type a string of text.

**Syntax**:
```plaintext
write {text};
```

---

### **Mouse Buttons**

Simulate mouse button actions.

**Syntax**:
```plaintext
mb {button} [(press)/up/down];
```

---

### **Scrolling**

Simulate mouse wheel scrolling.

**Syntax**:
```plaintext
scroll {amount};
```

**Arguments**:
- `{amount}`: Scroll units. Supports math and variables.

**Examples**:
```plaintext
scroll -5;
scroll ${scrollSpeed} * 10;
```

---

### **Clipboard Management**

Perform operations with the clipboard, including copying, pasting, clearing content, and accessing the clipboard value as a variable.

#### **Syntax**
```plaintext
clip {copy/paste/paste-m/clear} {text};
```

---

#### **Using Clipboard Content as a Variable**
You can access the current clipboard content directly using the special syntax `!{%clip%}`. This allows you to use the clipboard content in variables or commands.

---

#### **Examples**

1. **Basic Clipboard Operations**:
   ```plaintext
   clip copy Hello, World!;
   clip paste;
   clip clear;
   ```

2. **Using `paste-m` for Compatibility**:
   ```plaintext
   clip paste-m;
   ```

3. **Accessing Clipboard Content as a Variable**:
   ```plaintext
   clip copy Clipboard Test!;
   set clipboardContent !{%clip%};
   log Clipboard contains: ${clipboardContent};
   ```

---

### **Variable Management**

Define, use, and delete variables.

**Syntax**:
```plaintext
set {varname} {value};
del {varname};
```

---

### **Environment Variable Management**

Retrieve, set, or delete environment variables.

**Syntax**:
```plaintext
set {~var~|+var+} {value};
del {~var~|+var+};
```

---

### **Continue**

Pause the macro until a specific key or key combination is pressed.

**Syntax**:
```plaintext
continue {key};
```

---

### **Log**

Print a message to the console.

**Syntax**:
```plaintext
log {message};
```

---

## **Examples**

**Example Script**:
```plaintext
@FuncSplit = "\n"
@CommentOverride = "//"

set text1 "Hello, Macro World!"
set text2 "Powered by PyMacro."
set combinedText "${text1}${text2}"

// Simulate opening Notepad and typing text
hotkey win r
wait 500 ms
write notepad
key enter
wait 1 s
write ${combinedText}
key enter
write "Goodbye!"
```

---

## **Error Handling**

Errors during command execution output the command and exception details. Example:
```plaintext
Error processing command: set x ${undefined_var} + 1
Exception: Invalid expression: ${undefined_var}. Error: name 'undefined_var' is not defined
```