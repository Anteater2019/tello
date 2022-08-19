from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from worker.statusworker import StatusWorker
from worker.constants import STATUS_COMMANDS

class TelloGui(QWidget):
    '''Main GUI Widget for the Tello drone.'''
    def __init__(self):
        '''Initializes the Tello GUI Widget.'''
        super().__init__()
        self.title = 'Tello GUI'
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 500
        self.__init_gui()
        self.__init_workers()

    def __init_gui(self):
        '''Initializes the GUI for the Widget.'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.top_level_layout = QVBoxLayout()
        self.setLayout(self.top_level_layout)
        self.__init_status_bar()
        self.show()

    def __init_status_bar(self):
        '''Initializes the Status Bar GUI on the Tello GUI Widget.'''
        self.status_labels = {}
        layout = QHBoxLayout()
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.__start_status_worker)
        layout.addWidget(self.connect_button)
        self.status_labels['connected'] = QLabel('Connection: Not Established')
        layout.addWidget(self.status_labels['connected'])
        for command in STATUS_COMMANDS:
            self.status_labels[command] = QLabel(command.replace('?', ': ').capitalize())
            layout.addWidget(self.status_labels[command])
        self.top_level_layout.addLayout(layout)
        

    def __init_workers(self):
        '''Initializes the Workers for the Tello GUI Widget.'''
        self.status_worker = StatusWorker(self)
        self.status_worker.response_dict_signal.connect(self.__update_status_bar)
        self.status_worker.ready_signal.connect(self.__start_other_workers)

    def __start_status_worker(self):
        '''Starts and connects the StatusWorker with the Status Bar GUI.'''
        self.status_worker.start()
        self.connect_button.setDisabled(True)
        self.status_labels['connected'].setText('Connection: Attempting to Connect')

    def __start_other_workers(self, connected: bool):
        '''Starts all other workers if the StatusWorker signals back true.'''
        self.status_labels['connected'].setText('Connection: Established' if connected else 'Connection: Not Established')
        if connected:
            pass
        else:
            self.connect_button.setDisabled(False)

    def __update_status_bar(self, responseDict: dict):
        print('recieved data')
        units = {'speed?': 'cm/s', 'battery?': '%', 'time?': '', 'wifi?': 'dB'}
        for command in enumerate(STATUS_COMMANDS):
            self.status_labels[command].setText(command.replace('?', ': ').capitalize() + responseDict[command] + ' ' + units[command])