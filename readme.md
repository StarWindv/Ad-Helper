# 🎮 Auto Public Chat Ad Assistant

[中文](./readme_cn.md)

> An automated tool designed for gamers to send scheduled ad messages in game public chats (e.g., guild recruitment, item trading)

## 🌟 Key Features

- **Precise Coordinate Control**: Set exact coordinates for in-game text boxes and send buttons through a visual interface
  
- **Content Customization**: Freely edit ad content to be sent (supports Chinese, English, and special characters)
  
- **Smart Timing**: Customize send intervals (0.1s to 1 hour) and send count (supports infinite loops)
  
- **Operation Feedback**: Provides operation prompts and real-time logging
  
- **Dark Theme**: Modern dark UI design reduces eye strain during extended use
  
- **Configuration Saving**: Automatically saves all settings, no need to reconfigure on next launch
  
- **Safe & Reliable**: Pure Python development, no game memory modification, only simulates mouse/keyboard operations, not a cheat
  

## 📦 Project Structure

```plaintext
.
├── pyproject.toml
├── readme.md
├── requirements.txt
└── src
    └── stv_AdHelper
        ├── core
        │   ├── window.py
        │   └── worker.py
        ├── main-ui.py
        ├── main.py
        └── utils
            └── utils.py
```

## ⚙️ Usage Guide

### 1. Set Coordinates

1. Click the "Get Coordinates" button
2. Within the 5-second countdown, move mouse to in-game positions:
  - **Point A**: Chat input box position
  - **Point B**: Send button position
3. Program automatically captures and saves coordinates

### 2. Edit Content

Enter ad text to be sent in public chat in the "Content Settings" area. Use #n for line breaks

### 3. Configure Parameters

- **Operation Interval**: Set time between ad sends (seconds)
- **Repeat Count**: 0 = infinite loop, n = stops after n executions
- **Sound Prompt**: Enable/disable operation sound prompts

### 4. Start Execution

Click "Start Execution" to automatically send ads according to settings

## 🛠 System Requirements

- **OS**: Windows 10/11, macOS, Linux
  
- **Python Version**: 3.10+
  
- **Dependencies**:
  
  ```bash
  pip install PyQt5 pyautogui pyperclip stv_utils
  ```
  

## 🚀 Installation & Running

1. Clone repository:
  
  ```bash
  git clone https://github.com/yourusername/stv_AdHelper.git
  cd stv_AdHelper
  ```
  
2. Install program:
  
  ```bash
  pip install .
  ```
  
3. Run program:
  
  `sadui` is the GUI mode. For CLI mode, run `sad`.
  
  `sad` stands for `send Ad`.
  

```bash
sadui
```

## ⚠️ Important Notes

1. Ensure game window position is fixed before use
2. Do not move mouse or switch windows during operation
3. Comply with game rules to avoid bans from excessive sending
4. Recommended interval: 15-30 seconds
5. For legal use only. Any violation is prohibited

## 📜 Open Source License

This project uses [GPL v3 License](https://github.com/StarWindv/Ad-Helper/blob/main/LICENSE)

## 📕 Contributions Welcome

We welcome contributions from experts to build a better automation assistant!
