import random
from flask import Flask
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
socketio = SocketIO(app)


selectedCars = list()
playerPositions = list()
clientCount = 0
readyCount = 0


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
    emit('message', ConstructMessage('Client Connected', "Server", 'connect'), broadcast=True)
    emit('setCars', selectedCars)


@socketio.on('disconnect')
def handle_disconnect():
    emit('message', ConstructMessage('Client Disconnected', "Server", 'disconnect'), broadcast=True)


@socketio.on('message')
def handle_message(data: dict):
    emit('message', data, broadcast=True)


@socketio.on('ready')
def handle_ready():
    global readyCount, clientCount, playerPositions
    readyCount += 1
    emit('playerSet', playerPositions[0])
    playerPositions.pop(0)
    emit('ready', readyCount, broadcast=True)
    if readyCount == 2:
        emit('start', broadcast=True)


@socketio.on('update_position')
def handle_update_position(data):
    emit('position_update', data, broadcast=True, include_self=False)
    # spawnObstacles()


@socketio.on('retrievePositions')
def handle_retrievePositions(data):
    print('[*] Received Positions from Player')
    print('[*] Forwarding Positions to other Player\n')
    emit('recoverPositions', data, broadcast=True, include_self=False)


@socketio.on('recoverPositions')
def handle_recoverPositions():
    print('[*] A Client Reconnected While Game is Being Played')
    print('[*] Retrieving Positions from other Player\n')
    emit('retrievePositions', broadcast=True, include_self=False)


@socketio.on('playerCrash')
def handle_playerCrash(data):
    global selectedCars, readyCount, playerPositions
    emit('endGame', data, broadcast=True)
    initGameVariables()


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
    socketio.run(app, "192.168.1.203", 5050)
