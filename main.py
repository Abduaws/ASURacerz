import random
import pygame
import threading

from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi


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
    road3pImage = None
    road3pAspectRatio = None
    road4pImage = None
    road4pAspectRatio = None
    startGameImage = None
    startGameImageAspectRatio = None
    startGameDarkImage = None
    startGameDarkImageAspectRatio = None
    crashImage = None
    crashImageAspectRatio = None
    boulderImage = None
    spikeImage = None

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

        LoadedImages.road3pImage = pygame.image.load("../Resources/Roads/road3p.png").convert_alpha()
        LoadedImages.road3pAspectRatio = LoadedImages.road3pImage.get_height() / LoadedImages.road3pImage.get_width()
        LoadedImages.road3pImage = pygame.transform.scale(LoadedImages.road3pImage, (720 * LoadedImages.road2pAspectRatio, 720))

        LoadedImages.road4pImage = pygame.image.load("../Resources/Roads/road4p.png").convert_alpha()
        LoadedImages.road4pAspectRatio = LoadedImages.road4pImage.get_height() / LoadedImages.road4pImage.get_width()
        LoadedImages.road4pImage = pygame.transform.scale(LoadedImages.road4pImage, (720 * LoadedImages.road2pAspectRatio, 720))

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


class Button:
    def __init__(self, x, y, text, onclickFunction):
        self.x = x
        self.y = y
        self.onclickFunction = onclickFunction
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.btnText = pygame.font.Font("../Resources/TechnoRaceFont.otf", 18).render(text, True, "#000000")
        self.button = pygame.Surface((self.btnText.get_width() + 10, 30))
        self.buttonRect = self.button.get_rect()
        self.buttonRect.x = x
        self.buttonRect.y = y
        self.alreadyPressed = False
        myObjects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.button.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.button.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.button.blit(self.btnText, (
            (self.button.get_width() - self.btnText.get_width()) / 2,
            (self.button.get_height() - self.btnText.get_height()) / 2
        ))
        WIN.blit(self.button, self.buttonRect)


class StartBtn:
    def __init__(self, onclickFunction):
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.startBtn = LoadedImages.startGameImage
        self.startRect = LoadedImages.startGameImage.get_rect()
        self.startRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        myObjects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.startBtn = LoadedImages.startGameImage
        if self.startRect.collidepoint(mousePos):
            self.startBtn = LoadedImages.startGameDarkImage
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        text = pygame.font.Font("../Resources/TechnoRaceFont.otf", 48).render("1/2", True, "#ffffff")
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2 + 150)

        WIN.blit(text, textRect)
        WIN.blit(self.startBtn, self.startRect)


class Obstacle:
    def __init__(self):
        choices = ["boulderImage", "spikeImage"]
        obsType = random.choice(choices)
        self.obstacle = eval(f"LoadedImages.{obsType}")
        self.obstacleRect = eval(f"LoadedImages.{obsType}").get_rect()
        self.obstacleRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
        if playerCount == 2:
            pos1 = pygame.Vector2(342 + 35, 0)
            pos2 = pygame.Vector2(597 + 35, 0)
            self.obstacleRect.center = random.choice([pos1, pos2])
        elif playerCount == 3:
            pos1 = pygame.Vector2(289 + 35, 0)
            pos2 = pygame.Vector2(472 + 35, 0)
            pos3 = pygame.Vector2(650 + 35, 0)
            self.obstacleRect.center = random.choice([pos1, pos2, pos3])
        else:
            pos1 = pygame.Vector2(260 + 35, 0)
            pos2 = pygame.Vector2(402 + 35, 0)
            pos3 = pygame.Vector2(541 + 35, 0)
            pos4 = pygame.Vector2(679 + 35, 0)
            self.obstacleRect.center = random.choice([pos1, pos2, pos3, pos4])
        myObjects.append(self)

    def process(self):
        self.obstacleRect.y += 10
        WIN.blit(self.obstacle, self.obstacleRect)
        if self.obstacleRect.y > 720:
            myObjects.remove(self)
        p1Rect = eval(f"LoadedImages.{playerCar}").get_bounding_rect()
        p1Rect.x, p1Rect.y = player1_pos.x, player1_pos.y
        if p1Rect.colliderect(self.obstacleRect):
            crashPlayer(1)
            print("Player 1 Crashed into Obstacle")


def initGamePlayers():
    global player1_pos, player2_pos, player3_pos, player4_pos, limitRight, limitLeft, playerCount, backPos, backPos2
    if playerCount == 2:
        backPos = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2, 0)
        backPos2 = pygame.Vector2((1080 - LoadedImages.road2pImage.get_width()) / 2,
                                  0 - LoadedImages.road2pImage.get_height())
        player1_pos = pygame.Vector2(342+35, 570)
        player2_pos = pygame.Vector2(597+35, 570)
        limitLeft = 257+35
        limitRight = 683+35
    elif playerCount == 3:
        backPos = pygame.Vector2((1080 - LoadedImages.road3pImage.get_width()) / 2, 0)
        backPos2 = pygame.Vector2((1080 - LoadedImages.road3pImage.get_width()) / 2,
                                  0 - LoadedImages.road3pImage.get_height())
        player1_pos = pygame.Vector2(289+35, 570)
        player2_pos = pygame.Vector2(472+35, 570)
        player3_pos = pygame.Vector2(650+35, 570)
        limitLeft = 239+35
        limitRight = 702+35
    else:
        backPos = pygame.Vector2((1080 - LoadedImages.road4pImage.get_width()) / 2, 0)
        backPos2 = pygame.Vector2((1080 - LoadedImages.road4pImage.get_width()) / 2,
                                  0 - LoadedImages.road4pImage.get_height())
        player1_pos = pygame.Vector2(260+35, 570)
        player2_pos = pygame.Vector2(402+35, 570)
        player3_pos = pygame.Vector2(541+35, 570)
        player4_pos = pygame.Vector2(679+35, 570)
        limitLeft = 228+35
        limitRight = 714+35


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


def crashPlayer(player):
    global player1_pos, player2_pos, player3_pos, player4_pos, crashTime, crashFlag
    if playerCount == 2:
        if player == 1:
            player1_pos = pygame.Vector2(342 + 35, 570)
        if player == 2:
            player2_pos = pygame.Vector2(597 + 35, 570)

    elif playerCount == 3:
        if player == 1:
            player1_pos = pygame.Vector2(289 + 35, 570)
        if player == 2:
            player2_pos = pygame.Vector2(472 + 35, 570)
        if player == 3:
            player3_pos = pygame.Vector2(650 + 35, 570)
    else:
        if player == 1:
            player1_pos = pygame.Vector2(260 + 35, 570)
        if player == 2:
            player2_pos = pygame.Vector2(402 + 35, 570)
        if player == 3:
            player3_pos = pygame.Vector2(541 + 35, 570)
        if player == 4:
            player4_pos = pygame.Vector2(679 + 35, 570)
    crashRect = LoadedImages.crashImage.get_rect()
    crashRect.center = (WIN.get_width() / 2, WIN.get_height() / 2)
    WIN.blit(LoadedImages.crashImage, crashRect)
    crashTime = pygame.time.get_ticks()
    crashFlag = True


def addP():
    global playerCount, playerChangeFlag
    if playerCount < 4: playerCount += 1
    playerChangeFlag = True


def rmP():
    global playerCount, playerChangeFlag
    if playerCount > 2: playerCount -= 1
    playerChangeFlag = True


def startBtnClick():
    global startGameFlag
    startGameFlag = True
    myObjects.pop(-1)


def spawnObstacles():
    choices = [False] * 50
    choices.append(True)
    choice = random.choice(choices)
    if choice:
        Obstacle()


def checkCollision(p1Rect, p2Rect, p3Rect=None, p4Rect=None):
    if p4Rect:
        if p1Rect.colliderect(p2Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 2")
        if p1Rect.colliderect(p3Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 3")
        if p1Rect.colliderect(p4Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 4")
    elif p3Rect:
        if p1Rect.colliderect(p2Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 2")
        if p1Rect.colliderect(p3Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 3")
    else:
        if p1Rect.colliderect(p2Rect):
            crashPlayer(1)
            print("Player 1 Crashed into Player 2")
    displayCrashMsg()


def drawWindow():
    global playerCount, backPos
    p1Rect, p2Rect, p3Rect, p4Rect = [None]*4
    WIN.fill("#7e6d61")
    text = pygame.font.Font("../Resources/TechnoRaceFont.otf", 18).render(f"Number Of Players: {playerCount}", True,
                                                                       "#ffffff", "#7e6d61")
    textRect = text.get_rect()
    textRect.center = (100, 30)
    WIN.blit(text, textRect)
    if backPos.y >= 720: backPos.y = 0
    if playerCount == 2:
        if backPos2.y >= 0: backPos2.y = 0 - LoadedImages.road2pImage.get_height()
        WIN.blit(LoadedImages.road2pImage, backPos)
        WIN.blit(LoadedImages.road2pImage, backPos2)
        WIN.blit(eval(f"LoadedImages.{playerCar}"), player1_pos)
        WIN.blit(LoadedImages.audiCarImage, player2_pos)
        p1Rect = eval(f"LoadedImages.{playerCar}").get_bounding_rect()
        p1Rect.x, p1Rect.y = player1_pos.x, player1_pos.y
        p2Rect = LoadedImages.audiCarImage.get_bounding_rect()
        p2Rect.x, p2Rect.y = player2_pos.x, player2_pos.y
    elif playerCount == 3:
        if backPos2.y >= 0: backPos2.y = 0 - LoadedImages.road3pImage.get_height()
        WIN.blit(LoadedImages.road3pImage, backPos)
        WIN.blit(LoadedImages.road3pImage, backPos2)
        WIN.blit(eval(f"LoadedImages.{playerCar}"), player1_pos)
        WIN.blit(LoadedImages.audiCarImage, player2_pos)
        WIN.blit(LoadedImages.CarImage, player3_pos)
        p1Rect = eval(f"LoadedImages.{playerCar}").get_bounding_rect()
        p1Rect.x, p1Rect.y = player1_pos.x, player1_pos.y
        p2Rect = LoadedImages.audiCarImage.get_bounding_rect()
        p2Rect.x, p2Rect.y = player2_pos.x, player2_pos.y
        p3Rect = LoadedImages.CarImage.get_bounding_rect()
        p3Rect.x, p3Rect.y = player3_pos.x, player3_pos.y
    else:
        if backPos2.y >= 0: backPos2.y = 0 - LoadedImages.road4pImage.get_height()
        WIN.blit(LoadedImages.road4pImage, backPos)
        WIN.blit(LoadedImages.road4pImage, backPos2)
        WIN.blit(eval(f"LoadedImages.{playerCar}"), player1_pos)
        WIN.blit(LoadedImages.audiCarImage, player2_pos)
        WIN.blit(LoadedImages.CarImage, player3_pos)
        WIN.blit(LoadedImages.taxiCarImage, player4_pos)
        p1Rect = eval(f"LoadedImages.{playerCar}").get_bounding_rect()
        p1Rect.x, p1Rect.y = player1_pos.x, player1_pos.y
        p2Rect = LoadedImages.audiCarImage.get_bounding_rect()
        p2Rect.x, p2Rect.y = player2_pos.x, player2_pos.y
        p3Rect = LoadedImages.CarImage.get_bounding_rect()
        p3Rect.x, p3Rect.y = player3_pos.x, player3_pos.y
        p4Rect = LoadedImages.CarImage.get_bounding_rect()
        p4Rect.x, p4Rect.y = player4_pos.x, player4_pos.y

    checkCollision(p1Rect, p2Rect, p3Rect, p4Rect)

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
        if player1_pos.y - 10 < 0:
            player1_pos.y = 0
        else:
            player1_pos.y -= 10
    if keys[pygame.K_DOWN]:
        if player1_pos.y + 10 > (720 - 70 * LoadedImages.carAspectRatio):
            player1_pos.y = (720 - 70 * LoadedImages.carAspectRatio)
        else:
            player1_pos.y += 10
    if keys[pygame.K_LEFT]:
        if player1_pos.x - 10 < limitLeft:
            player1_pos.x = limitLeft
        else:
            player1_pos.x -= 10
            exec(f"LoadedImages.{playerCar} = pygame.transform.rotate(LoadedImages.{playerCar}, 3)")
    if keys[pygame.K_RIGHT]:
        if player1_pos.x + 10 > limitRight:
            player1_pos.x = limitRight
        else:
            player1_pos.x += 10
            exec(f"LoadedImages.{playerCar} = pygame.transform.rotate(LoadedImages.{playerCar}, -3)")


def launchGame():
    global playerChangeFlag, moveFlag
    obstacleSpawner = threading.Timer(500, spawnObstacles)
    run = True
    initGamePlayers()
    Button(20, 50, "Add Player", addP)
    Button(20, 90, "Remove Player", rmP)
    StartBtn(startBtnClick)
    while run:
        if playerChangeFlag:
            initGamePlayers()
            playerChangeFlag = False
        if startGameFlag:
            spawnObstacles()
            if not obstacleSpawner.is_alive():
                obstacleSpawner.start()
            if moveFlag:
                moveCar(pygame.key.get_pressed())
            backPos.y += 10
            backPos2.y += 10
        drawWindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
    pygame.quit()
    obstacleSpawner.cancel()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Resources/UI/MainMenu.ui", self)
        self.joinBtn.clicked.connect(self.joinClick)

    def joinClick(self):
        print(self.ipInput.text())
        self.reInitPygame()
        LoadedImages.init()
        game = threading.Thread(target=launchGame)
        game.start()
        self.stackedWidget.setCurrentIndex(1)

    @staticmethod
    def reInitPygame():
        global WIN, WIDTH, HEIGHT, clock, player1_pos, player2_pos
        global player3_pos, player4_pos, playerCar, playerCount, playerChangeFlag
        global limitLeft, limitRight, startGameFlag, backPos, backPos2, myObjects
        global crashTime, crashFlag, moveFlag, carModels
        pygame.init()
        WIDTH, HEIGHT = 1080, 720
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ASU RacerZ")
        pygame.display.set_icon(pygame.image.load("../Resources/icon.png"))
        clock = pygame.time.Clock()

        playerCount = 2
        playerChangeFlag = False
        startGameFlag = False
        player1_pos = pygame.Vector2(0, 0)
        player2_pos = pygame.Vector2(0, 0)
        player3_pos = pygame.Vector2(0, 0)
        player4_pos = pygame.Vector2(0, 0)
        limitLeft = 0
        limitRight = (1080 - 70)
        backPos = pygame.Vector2(0, 0)
        backPos2 = pygame.Vector2(0, 0)

        myObjects = []
        crashTime = 0
        crashFlag = False
        moveFlag = True

        carModels = ["audiCarImage", "blackVCarImage", "CarImage", "miniTruckCarImage", "miniVanCarImage",
                     "policeCarImage",
                     "taxiCarImage", "truckCarImage", "ambulanceCarImage"]
        playerCar = random.choice(carModels)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle("ASU RacerZ")
    MainWindow.setWindowIcon(QtGui.QIcon("../Resources/icon.png"))
    MainWindow.show()
    sys.exit(app.exec_())
