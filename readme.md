# **PyMacro Documentation**

Created by [Gabriezv1233](https://github.com/gabrielzv1233)  

Welcome to **PyMacro**, a small and simple macro scripting system! This documentation covers all supported commands, configuration options, and usage.

You can find an example script loader at **scriptloader.py**.

Documentation by our savior ChatGPT (slightly modified manually)

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

### **Example**
```plaintext
set x 100;
cursor ${x} 200;
wait 1 s;
clip copy Hello World;
```

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
set test1 Hello
set test2 World
log ${test1} ${test2}
```

---

#### **3. `@CommentOverride = "char(s)"`**
Defines the character(s) that mark the start of a comment. Text after the defined character(s) is ignored. The default is `None` (comments disabled).

**Example**:
```plaintext
@CommentOverride = "//"
set test1 Hello; // This is a comment
log ${test1}; // Another comment
```

**Disable Comments**:
```plaintext
@CommentOverride = "None"
set test1 Hello; # This will NOT be treated as a comment
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
- `{x}`: Horizontal position in pixels.
- `{y}`: Vertical position in pixels.

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

---

### **Clipboard Management**

Perform operations with the clipboard, including copying, pasting, clearing content, and accessing the clipboard value as a variable.

#### **Syntax**
```plaintext
clip {copy/paste/paste-m/clear} {text};
```

#### **Options**
- **`copy`**: Copies the specified text to the clipboard.
- **`paste`**: Pastes the current clipboard content.
- **`paste-m`**: Retrieves the clipboard content and types it using the `write` function. Use this if `paste` does not work with `Ctrl + V` in your setup.
- **`clear`**: Clears the clipboard content.

---

#### **Using Clipboard Content as a Variable**
You can access the current clipboard content directly using the special syntax `!{%clip%}`. This allows you to use the clipboard content in variables or commands.

---

#### **Examples**

1. **Basic Clipboard Operations**:
   ```plaintext
   clip copy Hello, World!;   // Copies "Hello, World!" to the clipboard
   clip paste;               // Pastes the current clipboard content
   clip clear;               // Clears the clipboard content
   ```

2. **Using `paste-m` for Compatibility**:
   ```plaintext
   clip paste-m;             // Types the clipboard content
   ```

3. **Accessing Clipboard Content as a Variable**:
   ```plaintext
   clip copy Clipboard Test!;      // Copies "Clipboard Test!" to the clipboard
   set clipboardContent !{%clip%}; // Retrieves clipboard content into a variable
   log Clipboard contains: ${clipboardContent};
   ```

---

#### **Expected Outputs**

- **Command**:
  ```plaintext
  clip copy Hello, Clipboard!;
  set clipContent !{%clip%};
  log ${clipContent};
  ```
- **Output**:
  ```plaintext
  Hello, Clipboard!
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

// Define variables
set text1 "PyMacro makes automation easy!"
set text2 "Try it out and boost your productivity."
set separator " | "
set finalText join(text1, separator, text2)

// Copy combined text to clipboard
log Copying formatted text to clipboard...
clip copy ${finalText}

// Open notepad to output text
hotkey win r // Opens the Run dialog for windows
wait 500
write notepad.exe
key enter
wait 1 s // Simulate time for loading notepad

// Simulate pasting the text into a document
log Pasting formatted text into the document.
clip paste

// Simulate adding a custom signature
wait 500 ms
write " - Powered by PyMacro"

// Perform some scrolling for demonstration
scroll -10 // Scroll down
scroll 20  // Scroll up

log Press ESC to close the script...
continue esc
log Exiting script. Goodbye!
```

**Output**:
```plaintext
Hello World
```

---

## **Error Handling**

Errors during command execution output the command and exception details. Example:
```plaintext
Error processing command: set x ${undefined_var} + 1
Exception: Invalid expression: ${undefined_var}. Error: name 'undefined_var' is not defined
```
