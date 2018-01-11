import numpy as np
import zmq

from agent import JoystickAgent
from tools import Dashboard
from tools import send_array, receive_array


def server_run():
    print('Init Dashboard.')
    dashboard = Dashboard()

    print('Init communication.')
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print('Wait for the first result...')
    data = receive_array(socket)
    print('Com success.')

    print('Init Agent')
    sample_state = np.random.randint(0, 256, (320, 240, 3), dtype=np.uint8)
    sample_action = np.random.random_sample(2)

    agent = JoystickAgent(sample_state, sample_action)

    input('Press "Enter" to start...')

    close = False
    while not close:
        ob, reward, done, info = data

        close = dashboard.update(ob, info)

        action = agent.act(ob, reward, done)

        print('Send action...', end='\t')
        send_array(socket, action)
        print('Done.')

        print('Wait for result...', end='\t')
        data = receive_array(socket)
        print('Received.')

    agent.close()


if __name__ == '__main__':
    server_run()
