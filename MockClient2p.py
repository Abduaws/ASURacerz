from socketio import Client
import threading

client = Client()

clientName = None
totalClients = None


def ConstructMessage(message, sender):
    return {
        'msg': message,
        'sender': sender
    }


@client.on('position_update')
def handle_position_update(data):
    print('Received position update for player', data)


@client.on('message')
def handle_message(data: dict):
    global clientName, totalClients
    if 'clientCount' in data.keys():
        totalClients = data['clientCount']
    print(f"{data['sender']}: {data['msg']}")


@client.on('disconnect')
def handle_disconnect():
    print('Disconnected from the server')


@client.on('connect')
def handle_connect():
    print('Connected to the server')


if __name__ == '__main__':
    threading.Thread(target=lambda: print(f"Current Client: {clientName}, Total Connected Clients: {totalClients}"))
    client.connect('http://192.168.1.108:5050')
    while True:
        msg = input()
        if msg == 'ready':
            client.emit('ready')
            continue
        client.emit('message', ConstructMessage(msg, f"Client {clientName}"))