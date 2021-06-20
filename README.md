# VK HotKeys

## 1. Install

- clone repo
- install python ([my version is 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe)) and venv
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

- go to [link](https://oauth.vk.com/authorize?client_id=7884254&display=page&scope=offline,photos&response_type=token&v=5.131), authorize and accept access to required permissions

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
