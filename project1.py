from pathlib import Path
from collections import namedtuple

class DeviceManager:
    """
    A class for managing devices and simulating communication.

    Attributes:
        deviceList (dict): A dictionary of devices with their properties.
        simLength (int): The length of the simulation.
        allMessages (list): A list of all messages exchanged during the simulation.
        alertMessages (dict): A dictionary to store alert messages and their timestamps.
        cancelMessages (dict): A dictionary to store cancellation messages and their timestamps.
        pairs (list): A list to store message pairs (alert and cancellation).
        finalMessages (list): A list of final messages after processing pairs.
        infoStorer (namedtuple): A named tuple for storing message information.
    """

    def __init__(self):
        self.deviceList = {}
        self.simLength = 0
        self.allMessages = []
        self.alertMessages = {}
        self.cancelMessages = {}
        self.pairs = []
        self.finalMessages = []
        self.infoStorer = namedtuple('infoStorer', 'id time description alertType outputStr')

    def numDevices(self):
        """
        Get the number of devices.

        Returns:
            int: The number of devices.
        """
        return len(self.deviceList)

    def setLength(self, simLength):
        """
        Set the length of the simulation.

        Args:
            simLength (int): The length of the simulation.
        """
        self.simLength = simLength

    def getLength(self):
        """
        Get the length of the simulation.

        Returns:
            int: The length of the simulation.
        """
        return self.simLength

    def addDevice(self, deviceID):
        """
        Add a device to the simulation.

        Args:
            deviceID: The ID of the device.
        """
        self.deviceList[deviceID] = [0, 0, False]
    def processPropagate(self, ID, receiver, propDuration):
        """
        Process message propagation between devices.

        Args:
            ID: The ID of the device.
            receiver: The ID of the receiving device.
            propDuration: The duration of message propagation.
        """
        self.deviceList[ID] = [receiver, propDuration, False]

    def determineCancelTime(self):
        """
        Determine the total time required for cancellation.

        Returns:
            int: The total time for cancellation.
        """
        time = 0
        for i in self.deviceList:
            time += int(self.getPropDuration(i))
        return time

    def getReceiver(self, ID):
        """
        Get the receiver of a device's message.

        Args:
            ID: The ID of the device.

        Returns:
            receiver: The ID of the receiving device.
        """
        if ID in self.deviceList:
            return self.deviceList[ID][0]
        else:
            return None

    def getPropDuration(self, ID):
        """
        Get the propagation duration for a device.

        Args:
            ID: The ID of the device.

        Returns:
            int: The propagation duration.
        """
        if ID in self.deviceList:
            return self.deviceList[ID][1]
        else:
            return -1

    def processAlert(self, ID, message, startTime): #process alert and adding messages, outputstr causes program to stop
        """
        Process an alert message from a device.

        Args:
            ID: The ID of the device.
            message: The alert message.
            startTime: The timestamp of the alert message.
        """
        self.alertMessages[message] = startTime
        time = int(startTime)
        myID = ID
        while time < int(self.simLength):
            alertMsg = self.infoStorer(id=myID, time=time, description=message, alertType="alertS", outputStr=f"@{time}: #{myID} SENT ALERT TO #{self.getReceiver(myID)}: {message}")
            self.allMessages.append(alertMsg)
            tempProp = int(self.getPropDuration(myID))
            time += tempProp
            if time > int(self.simLength):
                break
            receiveMsg = self.infoStorer(id=myID, time=time, description=message, alertType="alertR", outputStr=f"@{time}: #{self.getReceiver(myID)} RECEIVED ALERT FROM #{myID}: {message}")
            self.allMessages.append(receiveMsg)
            myID = self.getReceiver(myID)

    def processCancellation(self, ID, message, startTime):
        """
        Process a cancellation message from a device.

        Args:
            ID: The ID of the device.
            message: The cancellation message.
            startTime: The timestamp of the cancellation message.
        """
        self.cancelMessages[message] = startTime
        myID = ID
        time = int(startTime)
        while time < int(self.simLength):
            alertMsg = self.infoStorer(myID, time, message, "cancel", f"@{time}: #{myID} SENT CANCELLATION TO #{self.getReceiver(myID)}: {message}")
            self.allMessages.append(alertMsg)
            tempProp = int(self.getPropDuration(myID))
            time += tempProp
            if time > int(self.simLength):
                break
            receiveMsg = self.infoStorer(myID, time, message, "cancel", f"@{time}: #{myID} RECEIVED CANCELLATION FROM #{self.getReceiver(myID)}: {message}")
            self.allMessages.append(receiveMsg)
            myID = self.getReceiver(myID)

    def sortAndPrintMessages(self):
        """
        Sort and print the stored messages.
        """
        endMsg = self.infoStorer("", int(self.simLength), "", "end", f"@{self.simLength}: END")
        self.allMessages = sorted(self.allMessages, key=lambda msg: msg.time)

        for key, value in self.alertMessages.items():
            if key not in self.cancelMessages:
                for messages in self.allMessages:  # All message descriptions are trouble
                    if messages.description == key:
                        self.finalMessages.append(messages)
                        #pass

        for key, value in self.cancelMessages.items():
            if key not in self.alertMessages:
                for messages in self.allMessages:  # All message descriptions are trouble
                    if messages.description == key:
                        self.finalMessages.append(messages)

        self.processPairs()
        self.finalMessages = sorted(self.finalMessages, key=lambda msg: msg.time)
        self.finalMessages.append(endMsg)
        for i in self.finalMessages:
            print(i.outputStr)

    def processPairs(self):
        """
        Process message pairs and print final messages.
        """
        pairMessages = []
        for key, value in self.alertMessages.items():
            if key in self.cancelMessages:
                self.pairs.append(key)

        for pair in self.pairs:
            oneDescription = []

            myStopTime = 0

            for messages in self.allMessages:  # All message descriptions are trouble
                if messages.description == pair:
                    oneDescription.append(messages)

            for messages in oneDescription:
                if messages.alertType == "cancel":
                    myStopTime = messages.time + self.determineCancelTime()
                    break

            for messages in oneDescription:
                if messages.time <= myStopTime:
                    pairMessages.append(messages)

            for i in pairMessages:
                self.finalMessages.append(i)

            return pairMessages

def runFile(devManager: DeviceManager, fileLines):
    """
    Process input file lines and execute corresponding operations.

    Args:
        devManager (DeviceManager): The device manager object.
        fileLines (list): List of lines from the input file.
    """
    for line in fileLines:
        line.strip()
        tempList = line.split()
        if len(tempList) == 0: #added 2 lines, list was out of range
            continue
        elif tempList[0] == "LENGTH":
            devManager.setLength(tempList[1])
        elif tempList[0] == "DEVICE":
            devManager.addDevice(tempList[1])
        elif tempList[0] == "PROPAGATE":
            devManager.processPropagate(tempList[1], tempList[2], tempList[3])
        elif tempList[0] == "ALERT":
            devManager.processAlert(tempList[1], tempList[2], tempList[3])
        elif tempList[0] == "CANCEL":
            devManager.processCancellation(tempList[1], tempList[2], tempList[3])
        else:
            continue
#uncovered because it only runs with main
def _read_input_file_path() -> Path:
    """
    Reads the input file path from the standard input.

    Returns:
        Path: The path to the input file.
    """
    return Path(input())
#uncovered because it only runs with main
def runMain(myFile):
    """
    Run the simulation program using the provided input file.

    Args:
        myFile: The path to the input file.
    """
    with open(myFile, 'r') as file:
        return file.readlines()

#uncovered because it only runs with main
def main() -> None:
    """
    Runs the simulation program in its entirety.
    """
    input_file_path = _read_input_file_path()
    lines = runMain(input_file_path)
    myDeviceManager = DeviceManager()
    runFile(myDeviceManager, lines) #problem line
    myDeviceManager.sortAndPrintMessages()
if __name__ == '__main__':
    main()