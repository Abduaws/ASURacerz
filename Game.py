import time
import pygame
import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.uic import loadUi
from socketio import Client


pygame.init()
WIDTH, HEIGHT = 1080, 720
clock = pygame.time.Clock()
WIN = pygame.Surface((WIDTH, HEIGHT))

client = Client()
clientName = None
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

totalReadyCount = 0
currPlayerPos = None
gameStatus = 'playing'
crashCount = 0
crashTime = 0

threads = []


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


class StartBtn:
    def __init__(self, onclickFunction):
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.startBtn = LoadedImages.startGameImage
        self.startRect = LoadedImages.startGameImage.get_rect()
        self.startRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        myObjects.append(self)

    def process(self):
        global totalClientCount, totalReadyCount
        mousePos = pygame.mouse.get_pos()
        self.startBtn = LoadedImages.startGameImage
        if self.startRect.collidepoint(mousePos):
            self.startBtn = LoadedImages.startGameDarkImage
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed:
                    client.emit('ready')
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
        global gameStatus
        if gameStatus == 'lost':
            self.loseImage = LoadedImages.loseImage
            self.loseImageRect = LoadedImages.loseImage.get_rect()
            self.loseImageRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        else:
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
            pRect = eval(f"LoadedImages.{player1Car}").get_bounding_rect()
        else:
            pRect = eval(f"LoadedImages.{player2Car}").get_bounding_rect()

        pRect.x, pRect.y = eval(f"{currPlayerPos}").x, eval(f"{currPlayerPos}").y
        if pRect.colliderect(self.obstacleRect):
            crashPlayer()
            print(f"Player {clientName} Crashed into Obstacle")


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
        moveFlag = False
        LoadedImages.reInitCars()
        if pygame.time.get_ticks() - crashTime >= 500:
            crashFlag = False
            moveFlag = True
            return
        crashRect = LoadedImages.crashImage.get_rect()
        crashRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        WIN.blit(LoadedImages.crashImage, crashRect)


def crashPlayer():
    global player1Position, player2Position, crashTime, crashFlag, crashCount
    if crashCount > 3:
        client.emit('playerCrash', {'loser': clientName})
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
    
    while run:
        if startGameFlag and client.connected:
            if moveFlag:
                moveCar(pygame.key.get_pressed())
            backPos.y += 10
            backPos2.y += 10
        drawWindow()
        clock.tick(60)

    pygame.quit()


def updatePositioning():
    global player1Position, player2Position, run, currPlayerPos
    while run:
        time.sleep(0.1)
        if not client.connected:
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

        client.emit('update_position', data)


class UserNameInputDia(QtWidgets.QDialog):
    def __init__(self):
        super(UserNameInputDia, self).__init__()
        loadUi("Resources/UI/UsernameInput.ui", self)
        self.setWindowTitle("Username")
        self.setWindowIcon(QtGui.QIcon("Resources/icon.png"))

    def getUserName(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.lineEdit.text()
        else:
            return False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Resources/UI/MainMenu.ui", self)
        self.joinBtn.clicked.connect(self.joinClick)
        self.ipInput.returnPressed.connect(self.joinClick)
        self.sendBtn.clicked.connect(self.sendClick)
        self.msgInput.returnPressed.connect(self.sendClick)
        self.timer = QTimer()
        self.timer.timeout.connect(self.processMessage)
        self.timer.start(50)

    def sendClick(self):
        global clientName
        client.emit('message', ConstructMessage(self.msgInput.text(), clientName))

    def processMessage(self):
        global totalClientCount
        if messageQueue:
            for data in messageQueue:
                if 'clientCount' in data.keys():
                    totalClientCount = data['clientCount']
                self.serverText.append(f"\n{data['sender']}: {data['msg']}")
            messageQueue.clear()

    def joinClick(self):
        self.connectToServer()

        self.InitPygame()

        self.stackedWidget.setCurrentIndex(1)

    def connectToServer(self):
        global clientName, threads

        inputDia = UserNameInputDia()
        clientName = inputDia.getUserName()
        if not clientName:
            return

        connectionThread = threading.Thread(target=lambda: self.ServerConnectionHandler(self.ipInput.text()))
        threads.append(connectionThread)
        connectionThread.start()

        while not client.connected:
            pass

    def closeEvent(self, event):
        global client
        self.timer.stop()
        client.disconnect()
        for thread in threads:
            thread.join()
        print('All Threads Ended')

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
    def ServerConnectionHandler(IP):
        client.connect(f"http://{IP}:5050")
        while True:
            time.sleep(1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle("ASU RacerZ")
    MainWindow.setWindowIcon(QtGui.QIcon("Resources/icon.png"))
    MainWindow.show()


    @client.on('message')
    def receiveMessage(data):
        messageQueue.append(data)


    @client.on('ready')
    def handle_ready(data):
        global totalReadyCount
        totalReadyCount = int(data)


    @client.on('start')
    def handle_start():
        startBtnClick()


    @client.on('playerSet')
    def handle_playerSet(player):
        global currPlayerPos
        currPlayerPos = player


    @client.on('setCars')
    def handle_setCars(selected_Cars):
        global selectedCars
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
        Obstacle(pos)

    @client.on('endGame')
    def handle_endGame(data):
        global clientName, gameStatus, player1Position, player2Position, run, startGameFlag
        if data['loser'] == clientName:
            gameStatus = 'lost'
        else:
            gameStatus = 'won'
        player1Position = pygame.Vector2(100000, 100000)
        player2Position = pygame.Vector2(100000, 100000)
        startGameFlag = False
        WinLose()
        time.sleep(3)
        run = False

    @client.on('connect')
    def on_connect():
        print('connected')

    @client.on('disconnect')
    def on_disconnect():
        global disconnectedWhilePlaying
        if startGameFlag:
            disconnectedWhilePlaying = True


    sys.exit(app.exec_())
