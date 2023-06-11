import os
import random
import time
import pygame
import threading
import re
import socketio.exceptions
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from socketio import Client
import colorama


pygame.init()
WIDTH, HEIGHT = 1080, 720
clock = pygame.time.Clock()
WIN = pygame.Surface((WIDTH, HEIGHT))

client = Client()
clientName = None
IP = ''
totalClientCount = 0
messageQueue = []
selectedCars = list()

player1Position = pygame.Vector2()
player2Position = pygame.Vector2()
limitRight = 0
limitLeft = 0
backPos = pygame.Vector2()
backPos2 = pygame.Vector2()
player1Car = ''
player2Car = ''

myObjects = []

startGameFlag = False
crashFlag = False
moveFlag = True
run = True
disconnectedWhilePlaying = False
playAgainFlag = False
appRunning = True

totalReadyCount = 0
currPlayerPos = None
gameStatus = 'playing'
crashCount = 0
crashTime = 0

threads = []
connectionHealthCheckerThread = threading.Thread()
connectionInterruptedFlag = False
LoadingWindow = None
clientConnected = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LoadedImages:
    audiCarImage = None
    carAspectRatio = None
    blackVCarImage = None
    CarImage = None
    miniTruckCarImage = None
    miniVanCarImage = None
    policeCarImage = None
    taxiCarImage = None
    truckCarImage = None
    ambulanceCarImage = None
    road2pImage = None
    road2pAspectRatio = None
    startGameImage = None
    startGameImageAspectRatio = None
    startGameDarkImage = None
    startGameDarkImageAspectRatio = None
    crashImage = None
    crashImageAspectRatio = None
    boulderImage = None
    spikeImage = None
    loseImage = None
    winImage = None

    @staticmethod
    def init():
        LoadedImages.audiCarImage = pygame.image.load("Resources/Cars/Audi.png").convert_alpha()
        LoadedImages.carAspectRatio = LoadedImages.audiCarImage.get_height() / LoadedImages.audiCarImage.get_width()
        LoadedImages.audiCarImage = pygame.transform.scale(LoadedImages.audiCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.blackVCarImage = pygame.image.load("Resources/Cars/Black_viper.png").convert_alpha()
        LoadedImages.blackVCarImage = pygame.transform.scale(LoadedImages.blackVCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.CarImage = pygame.image.load("Resources/Cars/Car.png").convert_alpha()
        LoadedImages.CarImage = pygame.transform.scale(LoadedImages.CarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniTruckCarImage = pygame.image.load("Resources/Cars/Mini_truck.png").convert_alpha()
        LoadedImages.miniTruckCarImage = pygame.transform.scale(LoadedImages.miniTruckCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniVanCarImage = pygame.image.load("Resources/Cars/Mini_van.png").convert_alpha()
        LoadedImages.miniVanCarImage = pygame.transform.scale(LoadedImages.miniVanCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.policeCarImage = pygame.image.load("Resources/Cars/Police.png").convert_alpha()
        LoadedImages.policeCarImage = pygame.transform.scale(LoadedImages.policeCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.taxiCarImage = pygame.image.load("Resources/Cars/taxi.png").convert_alpha()
        LoadedImages.taxiCarImage = pygame.transform.scale(LoadedImages.taxiCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.truckCarImage = pygame.image.load("Resources/Cars/truck.png").convert_alpha()
        LoadedImages.truckCarImage = pygame.transform.scale(LoadedImages.truckCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.ambulanceCarImage = pygame.image.load("Resources/Cars/Ambulance.png").convert_alpha()
        LoadedImages.ambulanceCarImage = pygame.transform.scale(LoadedImages.ambulanceCarImage, (70, 70 * LoadedImages.carAspectRatio))

        LoadedImages.road2pImage = pygame.image.load("Resources/Roads/road2p.png").convert_alpha()
        LoadedImages.road2pAspectRatio = LoadedImages.road2pImage.get_height() / LoadedImages.road2pImage.get_width()
        LoadedImages.road2pImage = pygame.transform.scale(LoadedImages.road2pImage, (720 * LoadedImages.road2pAspectRatio, 720))

        LoadedImages.startGameImage = pygame.image.load("Resources/StartGame.png").convert_alpha()
        LoadedImages.startGameImageAspectRatio = LoadedImages.startGameImage.get_height() / LoadedImages.startGameImage.get_width()
        LoadedImages.startGameImage = pygame.transform.scale(LoadedImages.startGameImage, (360, 360 * LoadedImages.startGameImageAspectRatio))

        LoadedImages.startGameDarkImage = pygame.image.load("Resources/StartGameDark.png").convert_alpha()
        LoadedImages.startGameDarkImageAspectRatio = LoadedImages.startGameDarkImage.get_height() / LoadedImages.startGameDarkImage.get_width()
        LoadedImages.startGameDarkImage = pygame.transform.scale(LoadedImages.startGameDarkImage, (360, 360 * LoadedImages.startGameDarkImageAspectRatio))

        LoadedImages.crashImage = pygame.image.load("Resources/crash.png").convert_alpha()
        LoadedImages.crashImageAspectRatio = LoadedImages.crashImage.get_height() / LoadedImages.crashImage.get_width()
        LoadedImages.crashImage = pygame.transform.scale(LoadedImages.crashImage, (360, 360 * LoadedImages.crashImageAspectRatio))

        LoadedImages.boulderImage = pygame.image.load("Resources/Generic/boulder.png").convert_alpha()
        LoadedImages.boulderImage = pygame.transform.scale(LoadedImages.boulderImage, (70, 70 * 73 / 76))

        LoadedImages.spikeImage = pygame.image.load("Resources/Generic/spikes.png").convert_alpha()
        LoadedImages.spikeImage = pygame.transform.scale(LoadedImages.spikeImage, (32, 32 * 177 / 60))

        LoadedImages.winImage = pygame.image.load("Resources/Generic/win.png").convert_alpha()
        LoadedImages.winImageAspectRatio = LoadedImages.winImage.get_height() / LoadedImages.winImage.get_width()
        LoadedImages.winImage = pygame.transform.scale(LoadedImages.winImage,
                                                       (360, 360 * LoadedImages.winImageAspectRatio))

        LoadedImages.loseImage = pygame.image.load("Resources/Generic/lose.png").convert_alpha()
        LoadedImages.loseImageAspectRatio = LoadedImages.loseImage.get_height() / LoadedImages.loseImage.get_width()
        LoadedImages.loseImage = pygame.transform.scale(LoadedImages.loseImage,
                                                        (360, 360 * LoadedImages.loseImageAspectRatio))

    @staticmethod
    def reInitCars():
        LoadedImages.audiCarImage = pygame.image.load("Resources/Cars/Audi.png").convert_alpha()
        LoadedImages.audiCarImage = pygame.transform.scale(LoadedImages.audiCarImage,
                                                           (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.blackVCarImage = pygame.image.load("Resources/Cars/Black_viper.png").convert_alpha()
        LoadedImages.blackVCarImage = pygame.transform.scale(LoadedImages.blackVCarImage,
                                                             (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.CarImage = pygame.image.load("Resources/Cars/Car.png").convert_alpha()
        LoadedImages.CarImage = pygame.transform.scale(LoadedImages.CarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniTruckCarImage = pygame.image.load("Resources/Cars/Mini_truck.png").convert_alpha()
        LoadedImages.miniTruckCarImage = pygame.transform.scale(LoadedImages.miniTruckCarImage,
                                                                (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniVanCarImage = pygame.image.load("Resources/Cars/Mini_van.png").convert_alpha()
        LoadedImages.miniVanCarImage = pygame.transform.scale(LoadedImages.miniVanCarImage,
                                                              (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.policeCarImage = pygame.image.load("Resources/Cars/Police.png").convert_alpha()
        LoadedImages.policeCarImage = pygame.transform.scale(LoadedImages.policeCarImage,
                                                             (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.taxiCarImage = pygame.image.load("Resources/Cars/taxi.png").convert_alpha()
        LoadedImages.taxiCarImage = pygame.transform.scale(LoadedImages.taxiCarImage,
                                                           (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.truckCarImage = pygame.image.load("Resources/Cars/truck.png").convert_alpha()
        LoadedImages.truckCarImage = pygame.transform.scale(LoadedImages.truckCarImage,
                                                            (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.ambulanceCarImage = pygame.image.load("Resources/Cars/Ambulance.png").convert_alpha()
        LoadedImages.ambulanceCarImage = pygame.transform.scale(LoadedImages.ambulanceCarImage,
                                                                (70, 70 * LoadedImages.carAspectRatio))


class LoadingDia(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.CustomizeWindowHint)
        self.setObjectName("Dialog")
        self.setWindowTitle('Working')
        self.setFixedSize(221, 221)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 221, 221))
        self.label.setScaledContents(True)
        self.label.setText("")
        self.label.setObjectName("label")

        self.movie = QtGui.QMovie(f"Resources/Generic/Loading{random.randint(1, 3)}.gif")
        self.label.setMovie(self.movie)
        self.startAnimation()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_done)
        self.timer.start(50)

        QtCore.QMetaObject.connectSlotsByName(self)

    def startAnimation(self):
        self.movie.start()

    def load_done(self):
        global client
        if client.connected:
            self.movie.stop()
            self.close()


class StartBtn:
    def __init__(self, onclickFunction):
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.startBtn = LoadedImages.startGameImage
        self.startRect = LoadedImages.startGameImage.get_rect()
        self.startRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        myObjects.append(self)

    def process(self):
        global totalClientCount, totalReadyCount, clientConnected
        mousePos = pygame.mouse.get_pos()
        self.startBtn = LoadedImages.startGameImage
        if self.startRect.collidepoint(mousePos):
            self.startBtn = LoadedImages.startGameDarkImage
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed and clientConnected:
                    client.emit('ready')
                    print(colorama.Fore.BLUE + "[*] Client: Sending Ready Signal To Server")
                    if totalClientCount == totalReadyCount:
                        self.onclickFunction()
                    self.alreadyPressed = True

        text = pygame.font.Font("Resources/TechnoRaceFont.otf", 48).render(f"{totalReadyCount}/2",
                                                                           True, "#ffffff")
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2 + 150)

        WIN.blit(text, textRect)
        WIN.blit(self.startBtn, self.startRect)


class WinLose:
    def __init__(self):
        self.loseImage = LoadedImages.loseImage
        self.loseImageRect = LoadedImages.loseImage.get_rect()
        self.loseImageRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        self.winImage = LoadedImages.winImage
        self.winImageRect = LoadedImages.winImage.get_rect()
        self.winImageRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        myObjects.append(self)

    def process(self):
        global gameStatus
        if gameStatus == 'lost':
            WIN.blit(self.loseImage, self.loseImageRect)
        else:
            WIN.blit(self.winImage, self.winImageRect)


class Obstacle:
    def __init__(self, data):
        obsType = data['obs']
        self.obstacle = eval(f"LoadedImages.{obsType}")
        self.obstacleRect = eval(f"LoadedImages.{obsType}").get_rect()
        self.obstacleRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        self.obstacleRect.center = pygame.Vector2(int(data['pos']), 0)
        myObjects.append(self)

    def process(self):
        global clientName, player1Position, player2Position
        self.obstacleRect.y += 10
        WIN.blit(self.obstacle, self.obstacleRect)
        if self.obstacleRect.y > 720:
            myObjects.remove(self)

        if currPlayerPos == 'player1Position':
            currPlayerRect = eval(f"LoadedImages.{player1Car}").get_bounding_rect()
            currPlayerRect.x, currPlayerRect.y = eval("player1Position").x, eval("player1Position").y

            otherPlayerRect = eval(f"LoadedImages.{player2Car}").get_bounding_rect()
            otherPlayerRect.x, otherPlayerRect.y = eval("player2Position").x, eval("player2Position").y
        else:
            currPlayerRect = eval(f"LoadedImages.{player2Car}").get_bounding_rect()
            currPlayerRect.x, currPlayerRect.y = eval("player2Position").x, eval("player2Position").y

            otherPlayerRect = eval(f"LoadedImages.{player1Car}").get_bounding_rect()
            otherPlayerRect.x, otherPlayerRect.y = eval("player1Position").x, eval("player1Position").y

        if otherPlayerRect.colliderect(self.obstacleRect):
            myObjects.remove(self)

        if currPlayerRect.colliderect(self.obstacleRect):
            myObjects.remove(self)
            crashPlayer()


def ConstructMessage(message, sender):
    return {
        'msg': message,
        'sender': sender
    }


def initGamePlayers():
    global player1Position, player2Position, limitRight, limitLeft, backPos, backPos2
    global player1Car, player2Car, selectedCars
    backPos = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2, 0)
    backPos2 = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2,
                              0 - LoadedImages.road2pImage.get_height())
    player1Position = pygame.Vector2(342+35, 570)
    player2Position = pygame.Vector2(597+35, 570)
    limitLeft = 257+35
    limitRight = 683+35
    player1Car = selectedCars[0]
    player2Car = selectedCars[1]


def displayCrashMsg():
    global crashTime, crashFlag, moveFlag
    if crashFlag:
        LoadedImages.reInitCars()
        if pygame.time.get_ticks() - crashTime >= 500:
            crashFlag = False
            return
        crashRect = LoadedImages.crashImage.get_rect()
        crashRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        WIN.blit(LoadedImages.crashImage, crashRect)


def crashPlayer():
    global player1Position, player2Position, crashTime, crashFlag, crashCount, client
    if not startGameFlag:
        return
    if crashCount > 3 and client.connected:
        client.emit('playerCrash', {'loser': clientName})
        print(colorama.Fore.RED + "[*] Client: Sending Crash Signal To Server")
        return

    if currPlayerPos == "player1Position":
        player1Position = pygame.Vector2(342 + 35, 570)
    else:
        player2Position = pygame.Vector2(597 + 35, 570)

    crashRect = LoadedImages.crashImage.get_rect()
    crashRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
    WIN.blit(LoadedImages.crashImage, crashRect)
    crashTime = pygame.time.get_ticks()
    crashFlag = True
    crashCount += 1


def startBtnClick():
    global startGameFlag, threads
    startGameFlag = True
    myObjects.pop(-1)

    update_Positioning = threading.Thread(target=updatePositioning)
    threads.append(update_Positioning)
    update_Positioning.start()


def checkCollision(p1Rect, p2Rect):
    if p1Rect.colliderect(p2Rect) or p2Rect.colliderect(p1Rect):
        crashPlayer()
    displayCrashMsg()


def drawWindow():
    global player1Position, player2Position, backPos, backPos2, totalClientCount

    WIN.fill("#7e6d61")
    text = pygame.font.Font("Resources/TechnoRaceFont.otf", 18).render(f"Number Of Players: {totalClientCount}",
                                                                       True, "#ffffff", "#7e6d61")

    textRect = text.get_rect()
    textRect.center = (100, 30)
    WIN.blit(text, textRect)

    if backPos.y >= 720:
        backPos.y = 0
    if backPos2.y >= 0:
        backPos2.y = 0 - LoadedImages.road2pImage.get_height()
    WIN.blit(LoadedImages.road2pImage, backPos)
    WIN.blit(LoadedImages.road2pImage, backPos2)

    WIN.blit(eval(f"LoadedImages.{player1Car}"), player1Position)
    p1Rect = eval(f"LoadedImages.{player1Car}").get_bounding_rect()

    WIN.blit(eval(f"LoadedImages.{player2Car}"), player2Position)
    p2Rect = eval(f"LoadedImages.{player2Car}").get_bounding_rect()

    p1Rect.x, p1Rect.y = player1Position.x, player1Position.y
    p2Rect.x, p2Rect.y = player2Position.x, player2Position.y

    checkCollision(p1Rect, p2Rect)

    for myObject in myObjects:
        myObject.process()

    pygame.display.update()


def moveCar(keys):
    global limitLeft, limitRight

    LoadedImages.reInitCars()

    if keys[pygame.K_UP]:
        if eval(f"{currPlayerPos}").y - 10 < 0:
            eval(f"{currPlayerPos}").y = 0
        else:
            eval(f"{currPlayerPos}").y -= 10
    elif keys[pygame.K_DOWN]:
        if eval(f"{currPlayerPos}").y + 10 > (720 - 70 * LoadedImages.carAspectRatio):
            eval(f"{currPlayerPos}").y = (720 - 70 * LoadedImages.carAspectRatio)
        else:
            eval(f"{currPlayerPos}").y += 10

    else:
        if keys[pygame.K_LEFT]:
            if eval(f"{currPlayerPos}").x - 10 < limitLeft:
                eval(f"{currPlayerPos}").x = limitLeft
            else:
                eval(f"{currPlayerPos}").x -= 10

            if currPlayerPos == "player1Position":
                exec(f"LoadedImages.{player1Car} = pygame.transform.rotate(LoadedImages.{player1Car}, 3)")
            else:
                exec(f"LoadedImages.{player2Car} = pygame.transform.rotate(LoadedImages.{player2Car}, 3)")

        elif keys[pygame.K_RIGHT]:
            if eval(f"{currPlayerPos}").x + 10 > limitRight:
                eval(f"{currPlayerPos}").x = limitRight
            else:
                eval(f"{currPlayerPos}").x += 10

            if currPlayerPos == "player1Position":
                exec(f"LoadedImages.{player1Car} = pygame.transform.rotate(LoadedImages.{player1Car}, -3)")
            else:
                exec(f"LoadedImages.{player2Car} = pygame.transform.rotate(LoadedImages.{player2Car}, -3)")


def launchGame():
    global moveFlag, run
    
    initGamePlayers()
    StartBtn(startBtnClick)

    try:
        while run:
            if startGameFlag and client.connected:
                if moveFlag:
                    moveCar(pygame.key.get_pressed())
                backPos.y += 10
                backPos2.y += 10
            drawWindow()
            clock.tick(60)
    except Exception as e:
        print(e)


def updatePositioning():
    global player1Position, player2Position, run, currPlayerPos, client
    try:
        while run:
            time.sleep(0.1)
            if not client.connected or not run:
                continue

            if currPlayerPos == 'player1Position':
                data = {'SenderPos': 'player1Position',
                        'ReceiverPos': 'player2Position',
                        'player1Position': {'x': player1Position.x, 'y': player1Position.y},
                        'player2Position': {'x': player2Position.x, 'y': player2Position.y}}
            else:
                data = {'SenderPos': 'player2Position',
                        'ReceiverPos': 'player1Position',
                        'player1Position': {'x': player1Position.x, 'y': player1Position.y},
                        'player2Position': {'x': player2Position.x, 'y': player2Position.y}}

            if not client.connected:
                continue
            client.emit('update_position', data)
    except Exception as e:
        print(e)


def InitializeClientEvents():
    global client

    @client.on('message')
    def receiveMessage(data):
        global messageQueue
        print(colorama.Fore.YELLOW + "[*] Client: Received Chat Message From Server")
        messageQueue.append(data)

    @client.on('ready')
    def handle_ready(data):
        global totalReadyCount
        totalReadyCount = int(data)
        print(colorama.Fore.BLUE + "[*] Client: Received Player Ready Signal From Server")

    @client.on('start')
    def handle_start():
        startBtnClick()
        print(colorama.Fore.GREEN + "[*] Client: Received Start Game Signal From Server")

    @client.on('playerSet')
    def handle_playerSet(player):
        global currPlayerPos
        currPlayerPos = player
        print(colorama.Fore.BLUE + "[*] Client: Received Client Player Position From Server")

    @client.on('setCars')
    def handle_setCars(selected_Cars):
        global selectedCars
        print(colorama.Fore.BLUE + "[*] Client: Received Car List From Server")
        selectedCars = selected_Cars

    @client.on('position_update')
    def getNewPositions(data):
        global disconnectedWhilePlaying
        global player1Position, player2Position
        eval(f'{data["SenderPos"]}').x = eval(f'{data[data["SenderPos"]]}')['x']
        eval(f'{data["SenderPos"]}').y = eval(f'{data[data["SenderPos"]]}')['y']
        if disconnectedWhilePlaying:
            eval(f'{data["ReceiverPos"]}').x = eval(f'{data[data["ReceiverPos"]]}')['x']
            eval(f'{data["ReceiverPos"]}').y = eval(f'{data[data["ReceiverPos"]]}')['y']
            disconnectedWhilePlaying = False

    @client.on('spawnObstacle')
    def handle_spawnObstacle(pos):
        global run, startGameFlag
        if run and startGameFlag:
            Obstacle(pos)

    @client.on('endGame')
    def handle_endGame(data):
        global clientName, gameStatus, player1Position, player2Position, run, startGameFlag, myObjects, moveFlag
        global threads, playAgainFlag
        startGameFlag = False
        moveFlag = False
        myObjects.clear()
        print(colorama.Fore.RED + "[*] Client: Received End Game Signal From Server")
        if data['loser'] == clientName:
            gameStatus = 'lost'
        else:
            gameStatus = 'won'
        player1Position = pygame.Vector2(100000, 100000)
        player2Position = pygame.Vector2(10000, 10000)
        WinLose()
        time.sleep(1)
        run = False
        for thread in threads:
            thread.join()
        threads.clear()
        playAgainFlag = True

    @client.on('connect')
    def on_connect():
        global connectionInterruptedFlag, clientConnected
        print(colorama.Fore.GREEN + "[*] Client: Connected To Server")
        connectionInterruptedFlag = False
        clientConnected = True

    @client.on('disconnect')
    def on_disconnect():
        global disconnectedWhilePlaying, startGameFlag, clientConnected, client
        if startGameFlag:
            disconnectedWhilePlaying = True
        print(colorama.Fore.RED + "[*] Client: Disconnected From Server")
        clientConnected = False
        client.disconnect()


def CheckAlive(host, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        return True
    else:
        return False


def ServerConnect(server, port):
    global client, IP, clientConnected
    print(colorama.Fore.BLUE + f"[*] Client: Attempting to Establish Connection To {server}")
    client.disconnect()
    client = Client()
    InitializeClientEvents()
    client.connect(f'http://{IP}:{port}')
    while not clientConnected:
        continue
    print(colorama.Fore.GREEN + f"[*] Client: Connection Established To {server}")


def checkConnectionHealth():
    global appRunning, IP, connectionInterruptedFlag, client
    while appRunning:
        if not clientConnected:
            connectionInterruptedFlag = True

            if client.connection_url == f'http://{IP}:5000':
                print(colorama.Fore.RED + "[*] Client: Couldn't Establish Connection To Backup Server")
            else:
                print(colorama.Fore.RED + "[*] Client: Couldn't Establish Connection To Main Server")

            time.sleep(1)
            if not clientConnected:
                if CheckAlive(IP, 5050):
                    ServerConnect('Main Server', 5000)
                elif CheckAlive(IP, 5000):
                    ServerConnect('Backup Server', 5000)
        else:
            if client.connection_url == f'http://{IP}:5000':
                if CheckAlive(IP, 5050):
                    ServerConnect('Main Server', 5050)

        time.sleep(0.1)


class UserNameInputDia(QtWidgets.QDialog):
    def __init__(self):
        super(UserNameInputDia, self).__init__()
        loadUi("Resources/UI/UsernameInput.ui", self)
        self.setFixedSize(400, 300)
        self.setWindowTitle("Username")
        self.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
        self.label_2.setPixmap(QtGui.QPixmap('Resources/Roads/road2p.png'))

    def getUserName(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.lineEdit.text()
        else:
            return False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Resources/UI/MainMenu.ui", self)
        self.setFixedSize(800, 600)
        self.label_3.setPixmap(QtGui.QPixmap('Resources/Roads/road2p.png'))
        self.label_4.setPixmap(QtGui.QPixmap('Resources/Roads/road2p.png'))
        self.label_5.setPixmap(QtGui.QPixmap('Resources/Cars/Audi.png'))
        self.label_6.setPixmap(QtGui.QPixmap('Resources/Cars/Police.png'))
        self.label_7.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.label_8.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.label_9.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.label_10.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.label_11.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.label_12.setPixmap(QtGui.QPixmap('Resources/Generic/tree.png'))
        self.playAgainBtn.setIcon(QtGui.QIcon('Resources/playAgain.png'))
        self.playAgainBtn.clicked.connect(self.playAgainClick)
        self.joinBtn.clicked.connect(self.joinClick)
        self.ipInput.returnPressed.connect(self.joinClick)
        self.sendBtn.clicked.connect(self.sendClick)
        self.msgInput.returnPressed.connect(self.sendClick)
        self.timer = QTimer()
        self.timer.timeout.connect(self.processMessage)
        self.timer.start(50)
        self.exitClicked = False
        self.connectionError = False

    def sendClick(self):
        global clientName, client
        if not client.connected:
            return
        client.emit('message', ConstructMessage(self.msgInput.text(), clientName))
        print(colorama.Fore.YELLOW + "[*] Client: Sending Chat Message To Server")
        self.msgInput.clear()

    def processMessage(self):
        global totalClientCount, playAgainFlag, connectionInterruptedFlag, LoadingWindow
        if connectionInterruptedFlag:
            self.sendBtn.setDisabled(True)
            self.msgInput.setDisabled(True)
            LoadingWindow = LoadingDia()
            LoadingWindow.exec_()
            connectionInterruptedFlag = False
            self.sendBtn.setDisabled(False)
            self.msgInput.setDisabled(False)
        if playAgainFlag:
            MainWindow.setFixedSize(800, 710)
            time.sleep(1)
            pygame.display.iconify()
            playAgainFlag = False
        if messageQueue:
            for data in messageQueue:
                if 'clientCount' in data.keys():
                    totalClientCount = data['clientCount']
                self.serverText.append(f"\n{data['sender']}: {data['msg']}")
            messageQueue.clear()

    def playAgainClick(self):
        global WIN, threads, run, WIDTH, HEIGHT, myObjects, moveFlag, startGameFlag, player2Car, player1Car
        global crashFlag, totalReadyCount, gameStatus, crashCount, disconnectedWhilePlaying, selectedCars
        self.setFixedSize(800, 600)

        myObjects = []

        startGameFlag = False
        crashFlag = False
        moveFlag = True
        run = True
        disconnectedWhilePlaying = False

        totalReadyCount = 0
        gameStatus = 'playing'
        crashCount = 0

        LoadedImages.init()

        player1Car = selectedCars[0]
        player2Car = selectedCars[1]

        game = threading.Thread(target=launchGame)
        threads.append(game)
        game.start()

    def joinClick(self):
        global connectionHealthCheckerThread
        if not re.fullmatch(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)|(localhost)', self.ipInput.text()):
            self.errorPopup('Enter IP in Correct Format')
            return

        self.connectToServer()

        while not client.connected:
            if self.connectionError:
                self.errorPopup(f"Couldn't connect to EndPoint http://{self.ipInput.text()}:5050")
                self.connectionError = False
                return

        connectionHealthCheckerThread = threading.Thread(target=checkConnectionHealth)
        connectionHealthCheckerThread.start()

        self.InitPygame()

        self.stackedWidget.setCurrentIndex(1)

    def connectToServer(self):
        global clientName, threads, IP

        IP = self.ipInput.text()

        inputDia = UserNameInputDia()
        clientName = inputDia.getUserName()
        if not clientName:
            return

        connectionThread = threading.Thread(target=lambda: self.ServerConnectionHandler(IP))
        threads.append(connectionThread)
        connectionThread.start()

    def closeEvent(self, event):
        global client, startGameFlag, run, connectionHealthCheckerThread, appRunning
        appRunning = False
        startGameFlag = False
        run = False
        self.exitClicked = True

        client.disconnect()
        self.timer.stop()
        for thread in threads:
            thread.join()
        connectionHealthCheckerThread.join()
        pygame.quit()

    def ServerConnectionHandler(self, IP):
        try:
            client.connect(f"http://{IP}:5050")
        except socketio.exceptions.ConnectionRefusedError as connectionRefusedError:
            print(connectionRefusedError)
            self.connectionError = True
        except socketio.exceptions.ConnectionError as connectionErr:
            print(connectionErr)
            self.connectionError = True
        except socketio.exceptions.TimeoutError as timeoutError:
            print(timeoutError)
            self.connectionError = True
        except socketio.exceptions.BadNamespaceError as badNamespaceError:
            print(badNamespaceError)
            self.connectionError = True
        except socketio.exceptions.SocketIOError as socketIOError:
            print(socketIOError)
            self.connectionError = True
        except Exception as exception:
            print(exception)
            self.connectionError = True

    @staticmethod
    def InitPygame():
        global WIN, threads, run
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ASU RacerZ")
        pygame.display.set_icon(pygame.image.load("Resources/icon.png"))

        run = True

        LoadedImages.init()

        game = threading.Thread(target=launchGame)
        threads.append(game)
        game.start()

    @staticmethod
    def errorPopup(err_msg, extra=""):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
        msg.setText("An Error Occurred!")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setInformativeText(err_msg)
        if extra != "": msg.setDetailedText(extra)
        msg.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle("ASU RacerZ")
    MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
    MainWindow.show()

    InitializeClientEvents()

    sys.exit(app.exec_())
