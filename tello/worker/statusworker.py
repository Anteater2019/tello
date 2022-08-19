import socket
from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal
from worker.constants import COMMAND_RECIEVE_ADDR, STATUS_COMMANDS

class StatusWorker(QThread):
    '''Connects to the Tello Drone, initializes sdk, and starts retrieving status commands.'''
    response_dict_signal = pyqtSignal(dict) # Signals a dictionary of status commands mapped to their responses.
    ready_signal = pyqtSignal(bool)  # Signals that worker is connected and ready.

    def __init__(self, host='', port=9000, parent=None):
        '''Initializes StatusWorker.'''
        QThread.__init__(self, parent)
        self.running = False
        self.host = host
        self.port = port
        self.local_addr = (self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.response_dict = {}
        for command in STATUS_COMMANDS:
            self.response_dict[command] = ''

    def run(self):
        '''Starts the StatusWorker.'''
        self.running = True
        try:
            self.__init_sdk()
            while True: 
                for command in STATUS_COMMANDS:
                    self.__send_command(command)
                    data, _server = self.sock.recvfrom(1518)
                    print('data: ', data)
                    self.response_dict[command] = data.decode(encoding="utf-8")
                    print('response: ', self.response_dict[command])
                self.response_dict_signal.emit(self.response_dict)
                sleep(5)
        except Exception as e:
            print('An error has occured: ', e)
            print ('\nExiting \'Recieve From Tello\' Thread. . .\n')
            self.running = False
            self.ready_signal.emit(False); 
            self.sock.close()
            
    def __init_sdk(self):
        '''Connects to the tello drone and tries to initialize the sdk.'''
        self.sock.bind(self.local_addr)
        self.send_command('command')
        data, _server = self.sock.recvfrom(1518)
        if data.decode(encoding="utf-8") == 'error':
            raise Exception('Error Initializing SDK on Tello Drone.')
        self.ready_signal.emit(True); 

    def __send_command(self, command: str):
        '''Sends commands to the tello drone through the Command and Recieve Address.'''
        command = command.encode(encoding="utf-8") 
        sent = self.sock.sendto(command, COMMAND_RECIEVE_ADDR)
        print('sent: ', sent)
