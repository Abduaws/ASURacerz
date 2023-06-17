# ASURacerz
A Simple Multiplayer Racing Game made with python, pygame and Pyqt5 libraries
that also provide a chatting capability and Multiple Servers that are Robust


# Running the Code
To Configure Server IPs Go to Server.py and ServerBackup.py
And Change the following Lines to the IP of your machine

```python
Line 122: socketio.run(app, "YOUR IP HERE", 'LEAVE ALONE')
```
Run Server.py to run The Main Server

Run ServerBackup.py to run The Backup Server

Run Game.py to run Game


## Game Dependencies
```python
import random
import time
from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import pygame
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.uic import loadUi
from socketio import Client
```

## Server Dependencies
```python
import random
import time
from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import pygame
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.uic import loadUi
from socketio import Client
```

## Extra Pip Installs
```bash
pip install websocket-client
pip install requests
pip install flask_socketio
```

## Youtube Demo Video
https://www.youtube.com/watch?v=KurSgbvI47Q
