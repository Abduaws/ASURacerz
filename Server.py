import random
from flask import Flask
from flask_socketio import SocketIO, emit
import colorama

app = Flask(__name__)
socketio = SocketIO(app)


selectedCars = list()
playerPositions = list()
clientCount = 0
readyCount = 0
gameStarted = False


def spawnObstacles():
    choices = [False] * 24
    choices.append(True)
    choice = random.choice(choices)
    if choice:
        pos = random.randint(342 + 35, 597 + 35)
        obsType = random.choice(["boulderImage", "spikeImage"])
        data = {'pos': pos, 'obs': obsType}
        emit('spawnObstacle', data, broadcast=True)


def ConstructMessage(message, sender, connectionType=None):
    global clientCount
    if not connectionType:
        return {
            'msg': message,
            'sender': sender
        }
    if connectionType == 'connect':
        clientCount += 1
        return {
            'msg': message,
            'sender': sender,
            'clientCount': clientCount
        }
    else:
        clientCount -= 1
        return {
            'msg': message,
            'sender': sender,
            'clientCount': clientCount
        }


@socketio.on('connect')
def handle_connect():
    global selectedCars
    print(colorama.Fore.GREEN + "[*] Server: Client Connected")
    emit('message', ConstructMessage('Client Connected', "Server", 'connect'), broadcast=True)
    print(colorama.Fore.BLUE + "[*] Server: Sending Car List")
    emit('setCars', selectedCars)


@socketio.on('disconnect')
def handle_disconnect():
    print(colorama.Fore.RED + "[*] Server: Client Disconnected")
    emit('message', ConstructMessage('Client Disconnected', "Server", 'disconnect'), broadcast=True)


@socketio.on('message')
def handle_message(data: dict):
    print(colorama.Fore.YELLOW + "[*] Server: Received Player Message")
    emit('message', data, broadcast=True)
    print(colorama.Fore.YELLOW + "[*] Server: BroadCasting Player Message")


@socketio.on('ready')
def handle_ready():
    global readyCount, clientCount, playerPositions, gameStarted
    readyCount += 1
    emit('playerSet', playerPositions[0])
    playerPositions.pop(0)
    emit('ready', readyCount, broadcast=True)
    print(colorama.Fore.BLUE + "[*] Server: Emitting Player Ready Signal")
    if readyCount == 2:
        print(colorama.Fore.GREEN + "[*] Server: Sending Start Game Signal")
        emit('start', broadcast=True)
        gameStarted = True


@socketio.on('update_position')
def handle_update_position(data):
    emit('position_update', data, broadcast=True, include_self=False)
    # spawnObstacles()


@socketio.on('playerCrash')
def handle_playerCrash(data):
    global selectedCars, readyCount, playerPositions, gameStarted
    if not gameStarted:
        return
    print(colorama.Fore.RED + "[*] Server: Sending End Game Signal")
    emit('endGame', data, broadcast=True)
    initGameVariables()
    emit('setCars', selectedCars, broadcast=True)
    print(colorama.Fore.BLUE + "[*] Server: Sending New Cars")
    gameStarted = False


def initGameVariables():
    global selectedCars, playerPositions, readyCount
    carModels = ["audiCarImage", "blackVCarImage", "CarImage", "miniTruckCarImage", "miniVanCarImage",
                 "policeCarImage", "taxiCarImage", "truckCarImage", "ambulanceCarImage"]
    car1 = random.choice(carModels)
    carModels.remove(car1)
    car2 = random.choice(carModels)
    selectedCars = [car1, car2]
    playerPositions = ['player1Position', 'player2Position']
    readyCount = 0


if __name__ == '__main__':
    initGameVariables()
    print(colorama.Fore.GREEN + "[*] Server: Listening On Port 5050")
    socketio.run(app, "192.168.1.203", 5050)
