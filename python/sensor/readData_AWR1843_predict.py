import serial
import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets

import os

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

from sklearn.model_selection import train_test_split

# Change the configuration file name
configFileName = 'con2d_v3.cfg'

CLIport = {}
Dataport = {}
byteBuffer = np.zeros(2**15,dtype = 'uint8')
byteBufferLength = 0;


# ------------------------------------------------------------------

# Function to configure the serial ports and send the data from
# the configuration file to the radar
def serialConfig(configFileName):
    
    global CLIport
    global Dataport
    # Open the serial ports for the configuration and the data ports
    
    # Raspberry pi
    CLIport = serial.Serial('/dev/ttyACM0', 115200)
    Dataport = serial.Serial('/dev/ttyACM1', 921600)
    
    # Windows
    #CLIport = serial.Serial('COM8', 115200)
    #Dataport = serial.Serial('COM9', 921600)

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        CLIport.write((i+'\n').encode())
        print(i)
        time.sleep(0.01)
        
    return CLIport, Dataport

# ------------------------------------------------------------------

# Function to parse the data inside the configuration file
def parseConfigFile(configFileName):
    configParameters = {} # Initialize an empty dictionary to store the configuration parameters
    
    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        
        # Split the line
        splitWords = i.split(" ")
        
        # Hard code the number of antennas, change if other configuration is used
        numRxAnt = 4
        numTxAnt = 3
        
        # Get the information about the profile configuration
        if "profileCfg" in splitWords[0]:
            startFreq = int(float(splitWords[2]))
            idleTime = int(splitWords[3])
            rampEndTime = float(splitWords[5])
            freqSlopeConst = float(splitWords[8])
            numAdcSamples = int(splitWords[10])
            numAdcSamplesRoundTo2 = 1;
            
            while numAdcSamples > numAdcSamplesRoundTo2:
                numAdcSamplesRoundTo2 = numAdcSamplesRoundTo2 * 2;
                
            digOutSampleRate = int(splitWords[11]);
            
        # Get the information about the frame configuration    
        elif "frameCfg" in splitWords[0]:
            
            chirpStartIdx = int(splitWords[1]);
            chirpEndIdx = int(splitWords[2]);
            numLoops = int(splitWords[3]);
            numFrames = int(splitWords[4]);
            framePeriodicity = float(splitWords[5]);

            
    # Combine the read data to obtain the configuration parameters           
    numChirpsPerFrame = (chirpEndIdx - chirpStartIdx + 1) * numLoops
    configParameters["numDopplerBins"] = numChirpsPerFrame / numTxAnt
    configParameters["numRangeBins"] = numAdcSamplesRoundTo2
    configParameters["rangeResolutionMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * numAdcSamples)
    configParameters["rangeIdxToMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * configParameters["numRangeBins"])
    configParameters["dopplerResolutionMps"] = 3e8 / (2 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * configParameters["numDopplerBins"] * numTxAnt)
    configParameters["maxRange"] = (300 * 0.9 * digOutSampleRate)/(2 * freqSlopeConst * 1e3)
    configParameters["maxVelocity"] = 3e8 / (4 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * numTxAnt)
    
    return configParameters
   
# ------------------------------------------------------------------

# Funtion to read and parse the incoming data
def readAndParseData18xx(Dataport, configParameters):
    global byteBuffer, byteBufferLength
    
    # Constants
    OBJ_STRUCT_SIZE_BYTES = 12;
    BYTE_VEC_ACC_MAX_SIZE = 2**15;
    MMWDEMO_UART_MSG_DETECTED_POINTS = 1;
    MMWDEMO_UART_MSG_RANGE_PROFILE   = 2;
    maxBufferSize = 2**15;
    tlvHeaderLengthInBytes = 8;
    pointLengthInBytes = 16;
    magicWord = [2, 1, 4, 3, 6, 5, 8, 7]
    
    # Initialize variables
    magicOK = 0 # Checks if magic number has been read
    dataOK = 0 # Checks if the data has been read correctly
    frameNumber = 0
    detObj = {}
    
    readBuffer = Dataport.read(Dataport.in_waiting)
    byteVec = np.frombuffer(readBuffer, dtype = 'uint8')
    byteCount = len(byteVec)
    
    # Check that the buffer is not full, and then add the data to the buffer
    if (byteBufferLength + byteCount) < maxBufferSize:
        byteBuffer[byteBufferLength:byteBufferLength + byteCount] = byteVec[:byteCount]
        byteBufferLength = byteBufferLength + byteCount
        
    # Check that the buffer has some data
    if byteBufferLength > 16:
        
        # Check for all possible locations of the magic word
        possibleLocs = np.where(byteBuffer == magicWord[0])[0]

        # Confirm that is the beginning of the magic word and store the index in startIdx
        startIdx = []
        for loc in possibleLocs:
            check = byteBuffer[loc:loc+8]
            if np.all(check == magicWord):
                startIdx.append(loc)
               
        # Check that startIdx is not empty
        if startIdx:
            
            # Remove the data before the first start index
            if startIdx[0] > 0 and startIdx[0] < byteBufferLength:
                byteBuffer[:byteBufferLength-startIdx[0]] = byteBuffer[startIdx[0]:byteBufferLength]
                byteBuffer[byteBufferLength-startIdx[0]:] = np.zeros(len(byteBuffer[byteBufferLength-startIdx[0]:]),dtype = 'uint8')
                byteBufferLength = byteBufferLength - startIdx[0]
                
            # Check that there have no errors with the byte buffer length
            if byteBufferLength < 0:
                byteBufferLength = 0
                
            # word array to convert 4 bytes to a 32 bit number
            word = [1, 2**8, 2**16, 2**24]
            
            # Read the total packet length
            totalPacketLen = np.matmul(byteBuffer[12:12+4],word)
            
            # Check that all the packet has been read
            if (byteBufferLength >= totalPacketLen) and (byteBufferLength != 0):
                magicOK = 1
    
    # If magicOK is equal to 1 then process the message
    if magicOK:
        # word array to convert 4 bytes to a 32 bit number
        word = [1, 2**8, 2**16, 2**24]
        
        # Initialize the pointer index
        idX = 0
        
        # Read the header
        magicNumber = byteBuffer[idX:idX+8]
        idX += 8
        version = format(np.matmul(byteBuffer[idX:idX+4],word),'x')
        idX += 4
        totalPacketLen = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4
        platform = format(np.matmul(byteBuffer[idX:idX+4],word),'x')
        idX += 4
        frameNumber = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4
        timeCpuCycles = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4
        numDetectedObj = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4
        numTLVs = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4
        subFrameNumber = np.matmul(byteBuffer[idX:idX+4],word)
        idX += 4

        # Read the TLV messages
        for tlvIdx in range(numTLVs):
            
            # word array to convert 4 bytes to a 32 bit number
            word = [1, 2**8, 2**16, 2**24]

            # Check the header of the TLV message
            tlv_type = np.matmul(byteBuffer[idX:idX+4],word)
            idX += 4
            tlv_length = np.matmul(byteBuffer[idX:idX+4],word)
            idX += 4

            # Read the data depending on the TLV message
            if tlv_type == MMWDEMO_UART_MSG_DETECTED_POINTS:

                # Initialize the arrays
                x = np.zeros(numDetectedObj,dtype=np.float32)
                y = np.zeros(numDetectedObj,dtype=np.float32)
                z = np.zeros(numDetectedObj,dtype=np.float32)
                velocity = np.zeros(numDetectedObj,dtype=np.float32)
                
                for objectNum in range(numDetectedObj):
                    
                    # Read the data for each object
                    x[objectNum] = byteBuffer[idX:idX + 4].view(dtype=np.float32)
                    idX += 4
                    y[objectNum] = byteBuffer[idX:idX + 4].view(dtype=np.float32)
                    idX += 4
                    z[objectNum] = byteBuffer[idX:idX + 4].view(dtype=np.float32)
                    idX += 4
                    velocity[objectNum] = byteBuffer[idX:idX + 4].view(dtype=np.float32)
                    idX += 4
                
                # Store the data in the detObj dictionary
                detObj = {"numObj": numDetectedObj, "x": x, "y": y, "z": z, "velocity":velocity}
                dataOK = 1
                
 
        # Remove already processed data
        if idX > 0 and byteBufferLength>idX:
            shiftSize = totalPacketLen
            
                
            byteBuffer[:byteBufferLength - shiftSize] = byteBuffer[shiftSize:byteBufferLength]
            byteBuffer[byteBufferLength - shiftSize:] = np.zeros(len(byteBuffer[byteBufferLength - shiftSize:]),dtype = 'uint8')
            byteBufferLength = byteBufferLength - shiftSize
            
            # Check that there are no errors with the buffer length
            if byteBufferLength < 0:
                byteBufferLength = 0         

    return dataOK, frameNumber, detObj

# ------------------------------------------------------------------

# Funtion to update the data and display in the plot
def update(prev_keypoints):
     
    dataOk = 0
    global detObj
    x = []
    y = []
    keypoints = []
      
    # Read and parse the received data
    dataOk, frameNumber, detObj = readAndParseData18xx(Dataport, configParameters)
    
    if dataOk and len(detObj["x"])>0:
        x = detObj["x"]
        y = detObj["y"]

        numObj = detObj["numObj"]

        minObjNum = 5

        if numObj > minObjNum:
            x = x[:minObjNum]
            y = y[:minObjNum]
        elif numObj < minObjNum:
            end = np.zeros(minObjNum - numObj)
            x = np.concatenate((x, end))
            y = np.concatenate((y, end))

        for i in range(minObjNum):
            if x[i] > 0.3 or x[i] < -0.3:
                x[i] = 0
                y[i] = 0
            elif y[i] > 0.5 or y[i] < 0.085:
                x[i] = 0
                y[i] = 0

        non_zero_x = x[x != 0]
        non_zero_y = y[y != 0]

        if (len(non_zero_x) == 0) or (len(non_zero_y) == 0):
            return 0, keypoints
        
        mean_x = np.average(non_zero_x)
        mean_y = np.average(non_zero_y)

        for i in range(minObjNum):
            if x[i] == 0 or y[i] == 0:
                x[i] = mean_x
                y[i] = mean_y
        
        keypoints = np.concatenate((x, y))

        if (len(prev_keypoints) != 0):

            for i in range(len(keypoints)):
                if abs(keypoints[i] - prev_keypoints[i]) > 0.1:
                    
                    average = (keypoints[i] + prev_keypoints[i]) / 2
                    keypoints[i] = average
                    if i < minObjNum:
                        x[i] = average
                    elif i < 2 * minObjNum:
                        y[i - minObjNum] = average

        s.setData(x, y)
        QtWidgets.QApplication.processEvents()

        

    return dataOk, keypoints


# -------------------------    MAIN   -----------------------------------------  

# Configurate the serial port
CLIport, Dataport = serialConfig(configFileName)

# Get the configuration parameters from the configuration file
configParameters = parseConfigFile(configFileName)

# START QtAPPfor the plot
app = QtWidgets.QApplication([])

# Set the plot 
pg.setConfigOption('background','w')
win = pg.GraphicsLayoutWidget(title="2D scatter plot")
p = win.addPlot()
p.setXRange(-0.3, 0.3)
p.setYRange(0,0.7)
p.setLabel('left',text = 'Y position (m)')
p.setLabel('bottom', text= 'X position (m)')
s = p.plot([],[],pen=None,symbol='o')
win.show()


no_sequences = 30
sequence_length = 10

DATA_PATH = os.path.join('collected_data') # path for exported np arrays
actions = np.array(['left', 'right', 'up'])

label_map = {label:num for num, label in enumerate(actions)}

sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            if (len(res) != 21):
                print(action, len(res))
            
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

x = np.array(sequences)

shape = x.shape

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(shape[1], shape[2])))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model.load_weights('model_v4.h5')

# Main loop 
detObj = {}  

sequence = []
sentence = []
threshold = 0.9
keypoints_prev = np.zeros(0)
found = 0
count = 0

while True:
    try:
        # Update the data and check if the data is okay
        dataOk, keypoints = update(keypoints_prev)
        
        if dataOk:
            keypoints_prev = keypoints
            sequence.append(keypoints)
            sequence = sequence[-10:]
            if len(sequence) == 10:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                confidence = res[np.argmax(res)]
                if (res[np.argmax(res)] > threshold):
                    print(actions[np.argmax(res)])
                    found = 1
        
        if found == 1:
            while(count < 1000):
                count += 1
            count = 0
            found = 0


        
        time.sleep(0.025) # Sampling frequency of 30 Hz
        
    # Stop the program and close everything if Ctrl + c is pressed
    except KeyboardInterrupt:
        CLIport.write(('sensorStop\n').encode())
        CLIport.close()
        Dataport.close()
        win.close()
        break
        
    





