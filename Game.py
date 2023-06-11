import time
import pygame
import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.uic import loadUi
from socketio import Client


client = Client()
clientName = None
messageQueue = []
totalClientCount = 0
totalReadyCount = 0
currPlayerPos = None
gameStatus = 'playing'
crashCount = 0
run = True
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
        LoadedImages.audiCarImage = pygame.image.load("../Resources/Cars/Audi.png").convert_alpha()
        LoadedImages.carAspectRatio = LoadedImages.audiCarImage.get_height() / LoadedImages.audiCarImage.get_width()
        LoadedImages.audiCarImage = pygame.transform.scale(LoadedImages.audiCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.blackVCarImage = pygame.image.load("../Resources/Cars/Black_viper.png").convert_alpha()
        LoadedImages.blackVCarImage = pygame.transform.scale(LoadedImages.blackVCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.CarImage = pygame.image.load("../Resources/Cars/Car.png").convert_alpha()
        LoadedImages.CarImage = pygame.transform.scale(LoadedImages.CarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniTruckCarImage = pygame.image.load("../Resources/Cars/Mini_truck.png").convert_alpha()
        LoadedImages.miniTruckCarImage = pygame.transform.scale(LoadedImages.miniTruckCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.miniVanCarImage = pygame.image.load("../Resources/Cars/Mini_van.png").convert_alpha()
        LoadedImages.miniVanCarImage = pygame.transform.scale(LoadedImages.miniVanCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.policeCarImage = pygame.image.load("../Resources/Cars/Police.png").convert_alpha()
        LoadedImages.policeCarImage = pygame.transform.scale(LoadedImages.policeCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.taxiCarImage = pygame.image.load("../Resources/Cars/taxi.png").convert_alpha()
        LoadedImages.taxiCarImage = pygame.transform.scale(LoadedImages.taxiCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.truckCarImage = pygame.image.load("../Resources/Cars/truck.png").convert_alpha()
        LoadedImages.truckCarImage = pygame.transform.scale(LoadedImages.truckCarImage, (70, 70 * LoadedImages.carAspectRatio))
        LoadedImages.ambulanceCarImage = pygame.image.load("../Resources/Cars/Ambulance.png").convert_alpha()
        LoadedImages.ambulanceCarImage = pygame.transform.scale(LoadedImages.ambulanceCarImage, (70, 70 * LoadedImages.carAspectRatio))

        LoadedImages.road2pImage = pygame.image.load("../Resources/Roads/road2p.png").convert_alpha()
        LoadedImages.road2pAspectRatio = LoadedImages.road2pImage.get_height() / LoadedImages.road2pImage.get_width()
        LoadedImages.road2pImage = pygame.transform.scale(LoadedImages.road2pImage, (720 * LoadedImages.road2pAspectRatio, 720))

        LoadedImages.startGameImage = pygame.image.load("../Resources/StartGame.png").convert_alpha()
        LoadedImages.startGameImageAspectRatio = LoadedImages.startGameImage.get_height() / LoadedImages.startGameImage.get_width()
        LoadedImages.startGameImage = pygame.transform.scale(LoadedImages.startGameImage, (360, 360 * LoadedImages.startGameImageAspectRatio))

        LoadedImages.startGameDarkImage = pygame.image.load("../Resources/StartGameDark.png").convert_alpha()
        LoadedImages.startGameDarkImageAspectRatio = LoadedImages.startGameDarkImage.get_height() / LoadedImages.startGameDarkImage.get_width()
        LoadedImages.startGameDarkImage = pygame.transform.scale(LoadedImages.startGameDarkImage, (360, 360 * LoadedImages.startGameDarkImageAspectRatio))

        LoadedImages.crashImage = pygame.image.load("../Resources/crash.png").convert_alpha()
        LoadedImages.crashImageAspectRatio = LoadedImages.crashImage.get_height() / LoadedImages.crashImage.get_width()
        LoadedImages.crashImage = pygame.transform.scale(LoadedImages.crashImage, (360, 360 * LoadedImages.crashImageAspectRatio))

        LoadedImages.boulderImage = pygame.image.load("../Resources/Generic/boulder.png").convert_alpha()
        LoadedImages.boulderImage = pygame.transform.scale(LoadedImages.boulderImage, (70, 70 * 73 / 76))

        LoadedImages.spikeImage = pygame.image.load("../Resources/Generic/spikes.png").convert_alpha()
        LoadedImages.spikeImage = pygame.transform.scale(LoadedImages.spikeImage, (32, 32 * 177 / 60))

        LoadedImages.winImage = pygame.image.load("../Resources/Generic/win.png").convert_alpha()
        LoadedImages.winImageAspectRatio = LoadedImages.winImage.get_height() / LoadedImages.winImage.get_width()
        LoadedImages.winImage = pygame.transform.scale(LoadedImages.winImage,
                                                       (360, 360 * LoadedImages.winImageAspectRatio))

        LoadedImages.loseImage = pygame.image.load("../Resources/Generic/lose.png").convert_alpha()
        LoadedImages.loseImageAspectRatio = LoadedImages.loseImage.get_height() / LoadedImages.loseImage.get_width()
        LoadedImages.loseImage = pygame.transform.scale(LoadedImages.loseImage,
                                                        (360, 360 * LoadedImages.loseImageAspectRatio))


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

        text = pygame.font.Font("../Resources/TechnoRaceFont.otf", 48).render(f"{totalReadyCount}/{totalClientCount}",
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
        global clientName, player1_pos, player2_pos
        self.obstacleRect.y += 10
        WIN.blit(self.obstacle, self.obstacleRect)
        if self.obstacleRect.y > 720:
            myObjects.remove(self)
        pRect = eval(f"LoadedImages.{eval(f'{currPlayerPos}Car')}").get_bounding_rect()
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
    global player1_pos, player2_pos, limitRight, limitLeft, backPos, backPos2
    backPos = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2, 0)
    backPos2 = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2,
                              0 - LoadedImages.road2pImage.get_height())
    player1_pos = pygame.Vector2(342+35, 570)
    player2_pos = pygame.Vector2(597+35, 570)
    limitLeft = 257+35
    limitRight = 683+35


def displayCrashMsg():
    global crashTime, crashFlag, moveFlag
    if crashFlag:
        moveFlag = False
        reposCars()
        if pygame.time.get_ticks() - crashTime >= 500:
            crashFlag = False
            moveFlag = True
            return
        crashRect = LoadedImages.crashImage.get_rect()
        crashRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        WIN.blit(LoadedImages.crashImage, crashRect)


def crashPlayer():
    global player1_pos, player2_pos, crashTime, crashFlag, crashCount
    if crashCount > 3:
        client.emit('playerCrash', {'loser': clientName})
        return
    if currPlayerPos == "player1_pos":
        player1_pos = pygame.Vector2(342 + 35, 570)
    else:
        player2_pos = pygame.Vector2(597 + 35, 570)
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
    global startGameFlag
    if (p1Rect.colliderect(p2Rect) or p2Rect.colliderect(p1Rect)) and startGameFlag:
        crashPlayer()
    displayCrashMsg()


def drawWindow():
    global player1_pos, player2_pos, backPos, backPos2, totalClientCount
    WIN.fill("#7e6d61")
    text = pygame.font.Font("../Resources/TechnoRaceFont.otf", 18).render(f"Number Of Players: {totalClientCount}",
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

    WIN.blit(eval(f"LoadedImages.{player1_posCar}"), player1_pos)
    p1Rect = eval(f"LoadedImages.{player1_posCar}").get_bounding_rect()

    WIN.blit(eval(f"LoadedImages.{player2_posCar}"), player2_pos)
    p2Rect = eval(f"LoadedImages.{player2_posCar}").get_bounding_rect()

    p1Rect.x, p1Rect.y = player1_pos.x, player1_pos.y
    p2Rect.x, p2Rect.y = player2_pos.x, player2_pos.y

    checkCollision(p1Rect, p2Rect)

    for myObject in myObjects:
        myObject.process()

    pygame.display.update()


def reposCars():
    LoadedImages.audiCarImage = pygame.image.load("../Resources/Cars/Audi.png").convert_alpha()
    LoadedImages.carAspectRatio = LoadedImages.audiCarImage.get_height() / LoadedImages.audiCarImage.get_width()
    LoadedImages.audiCarImage = pygame.transform.scale(LoadedImages.audiCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.blackVCarImage = pygame.image.load("../Resources/Cars/Black_viper.png").convert_alpha()
    LoadedImages.blackVCarImage = pygame.transform.scale(LoadedImages.blackVCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.CarImage = pygame.image.load("../Resources/Cars/Car.png").convert_alpha()
    LoadedImages.CarImage = pygame.transform.scale(LoadedImages.CarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.miniTruckCarImage = pygame.image.load("../Resources/Cars/Mini_truck.png").convert_alpha()
    LoadedImages.miniTruckCarImage = pygame.transform.scale(LoadedImages.miniTruckCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.miniVanCarImage = pygame.image.load("../Resources/Cars/Mini_van.png").convert_alpha()
    LoadedImages.miniVanCarImage = pygame.transform.scale(LoadedImages.miniVanCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.policeCarImage = pygame.image.load("../Resources/Cars/Police.png").convert_alpha()
    LoadedImages.policeCarImage = pygame.transform.scale(LoadedImages.policeCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.taxiCarImage = pygame.image.load("../Resources/Cars/taxi.png").convert_alpha()
    LoadedImages.taxiCarImage = pygame.transform.scale(LoadedImages.taxiCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.truckCarImage = pygame.image.load("../Resources/Cars/truck.png").convert_alpha()
    LoadedImages.truckCarImage = pygame.transform.scale(LoadedImages.truckCarImage, (70, 70 * LoadedImages.carAspectRatio))
    LoadedImages.ambulanceCarImage = pygame.image.load("../Resources/Cars/Ambulance.png").convert_alpha()
    LoadedImages.ambulanceCarImage = pygame.transform.scale(LoadedImages.ambulanceCarImage, (70, 70 * LoadedImages.carAspectRatio))


def moveCar(keys):
    reposCars()
    if keys[pygame.K_UP]:
        if eval(f"{currPlayerPos}").y - 10 < 0:
            eval(f"{currPlayerPos}").y = 0
        else:
            eval(f"{currPlayerPos}").y -= 10
    if keys[pygame.K_DOWN]:
        if eval(f"{currPlayerPos}").y + 10 > (720 - 70 * LoadedImages.carAspectRatio):
            eval(f"{currPlayerPos}").y = (720 - 70 * LoadedImages.carAspectRatio)
        else:
            eval(f"{currPlayerPos}").y += 10
    if keys[pygame.K_LEFT]:
        if eval(f"{currPlayerPos}").x - 10 < limitLeft:
            eval(f"{currPlayerPos}").x = limitLeft
        else:
            eval(f"{currPlayerPos}").x -= 10
            exec(f"LoadedImages.{eval(f'{currPlayerPos}Car')} = pygame.transform.rotate(LoadedImages.{eval(f'{currPlayerPos}Car')}, 3)")
    if keys[pygame.K_RIGHT]:
        if eval(f"{currPlayerPos}").x + 10 > limitRight:
            eval(f"{currPlayerPos}").x = limitRight
        else:
            eval(f"{currPlayerPos}").x += 10
            exec(f"LoadedImages.{eval(f'{currPlayerPos}Car')} = pygame.transform.rotate(LoadedImages.{eval(f'{currPlayerPos}Car')}, -3)")


def launchGame():
    global moveFlag, run
    run = True
    initGamePlayers()
    StartBtn(startBtnClick)
    while run:
        if startGameFlag:
            if moveFlag:
                moveCar(pygame.key.get_pressed())
            backPos.y += 10
            backPos2.y += 10
        drawWindow()
        clock.tick(60)
    pygame.quit()
    print('launch End')


def updatePositioning():
    global player1_pos, player2_pos, startGameFlag
    while startGameFlag:
        time.sleep(0.1)
        data = {'playerPos': currPlayerPos, 'x': eval(f"{currPlayerPos}").x, 'y': eval(f"{currPlayerPos}").y}
        client.emit('update_position', data)
    print('UpdatePos End')


class UserNameInputDia(QtWidgets.QDialog):
    def __init__(self):
        super(UserNameInputDia, self).__init__()
        loadUi("../Resources/UI/UsernameInput.ui", self)
        self.setWindowTitle("Username")
        self.setWindowIcon(QtGui.QIcon("../Resources/icon.png"))

    def getUserName(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.lineEdit.text()
        else:
            return False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("../Resources/UI/MainMenu.ui", self)
        self.joinBtn.clicked.connect(self.joinClick)
        self.ipInput.returnPressed.connect(self.joinClick)
        self.sendBtn.clicked.connect(self.sendClick)
        self.msgInput.returnPressed.connect(self.sendClick)
        self.connectionThread = QThread()
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
        global clientName, threads
        inputDia = UserNameInputDia()
        res = inputDia.getUserName()
        if not res:
            return
        clientName = res
        self.connectionThread.started.connect(lambda: client.connect(f"http://{self.ipInput.text()}:5050"))
        self.connectionThread.start()
        self.reInitPygame()
        LoadedImages.init()
        game = threading.Thread(target=launchGame)
        threads.append(game)
        game.start()
        self.stackedWidget.setCurrentIndex(1)

    @staticmethod
    def reInitPygame():
        global WIN, WIDTH, HEIGHT, clock, player1_pos, player2_pos
        global limitLeft, limitRight, startGameFlag, backPos, backPos2, myObjects
        global crashTime, crashFlag, moveFlag, selectedCars, player1_posCar, player2_posCar

        pygame.init()
        WIDTH, HEIGHT = 1080, 720
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ASU RacerZ")
        pygame.display.set_icon(pygame.image.load("../Resources/icon.png"))
        clock = pygame.time.Clock()

        startGameFlag = False
        player1_pos = pygame.Vector2(0, 0)
        player2_pos = pygame.Vector2(0, 0)
        limitLeft = 0
        limitRight = (1080 - 70)
        backPos = pygame.Vector2(0, 0)
        backPos2 = pygame.Vector2(0, 0)

        myObjects = []
        crashTime = 0
        crashFlag = False
        moveFlag = True

        player1_posCar = selectedCars[0]
        player2_posCar = selectedCars[1]

    def closeEvent(self, event):
        global client
        self.connectionThread.quit()
        self.timer.stop()
        client.disconnect()
        for thread in threads:
            thread.join()
        print('All Threads Ended')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle("ASU RacerZ")
    MainWindow.setWindowIcon(QtGui.QIcon("../Resources/icon.png"))
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
    def getNewPositions(newPos):
        global player1_pos, player2_pos
        eval(f"{newPos['playerPos']}").x = newPos['x']
        eval(f"{newPos['playerPos']}").y = newPos['y']

    @client.on('spawnObstacle')
    def handle_spawnObstacle(pos):
        Obstacle(pos)

    @client.on('endGame')
    def handle_endGame(data):
        global clientName, gameStatus, player1_pos, player2_pos, startGameFlag, run
        if data['loser'] == clientName:
            gameStatus = 'lost'
        else:
            gameStatus = 'won'
        player1_pos = pygame.Vector2(100000, 100000)
        player2_pos = pygame.Vector2(100000, 100000)
        startGameFlag = False
        WinLose()
        time.sleep(3)
        run = False

    sys.exit(app.exec_())
