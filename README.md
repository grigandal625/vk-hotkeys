# VK HotKeys

## 1. Install

- clone repo
- create and activate venv (PowerShell)

```PowerShell
python -m venv venv
./venv/Scripts/activate
```

- run in activated venv

```PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run

- enter `login`, `password` and `peer` to [vk-auth.json](./vk-auth.json) like

```json
{
    "login": "XXXXXXX",
    "password": "XXXXXX",
    "peer": 1234567890
}
```

- enter hotkeys to [hotkeys.json](./hotkeys.json) like

```json
{
    "Alt + X": "HELLO",
    "Alt + W": "GOODBYE",
}
```

> **RESERVED HOTKEYS**

> `Alt + S` - send screenshot

> `Alt + Q` - exit programm

- run in PowerShell or run in file explorer [start.bat](./start.bat)

```PowerShell
./start.bat
```
