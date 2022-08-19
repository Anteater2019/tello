HOST = '192.168.10.1' # Tello drone ip address.
COMMAND_RECIEVE_PORT = 8889 # Tello port for commanding and recieving.
COMMAND_RECIEVE_ADDR = (HOST, COMMAND_RECIEVE_PORT) # Tello address for commanding and recieving.

STATUS_COMMANDS = ['speed?', 'battery?', 'time?', 'wifi?'] # Tello status commands of interest.