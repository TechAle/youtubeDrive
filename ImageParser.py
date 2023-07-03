import json

from cv2 import cv2
import os
import shutil
import sys
import numpy as np

class imageParser:
    def __init__(self, path):
        self.canvas = None
        self.path = path
        self.idxColumn = 0
        self.idxRow = 0
        self.colors = {
            "colors": ["", "", ""],
            "idx": 0
        }
        self.__loadConfiguration()

    '''
        Loads configuration.json in the system
    '''
    def __loadConfiguration(self):
        with open("configuration.json", 'r') as file:
            data = json.load(file)
            self.width = data["width"]
            self.height = data["height"]
            self.pixelDimensions = data["pixelDimension"]
            self.refreshRate = data["refreshRate"]
            self.bandwidth = data["bandwidth"]

    '''
        Main function for generating the image
    '''
    def generateImages(self):
        # We start with an empty image
        self.createNewImage()
        self.createOutputDirectory()
        self.iterateFiles(self.path)
        self.generateVideo()
        self.deleteOutputDirectory()
        cv2.waitKey(0)

    def createNewImage(self):
        # Create a blank image
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.imshow("Testing", self.canvas)

    def iterateFiles(self, path):
        if os.path.isfile(path):
            self.createNewImage(path)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.createImage(file_path)
                for dir in dirs:
                    self.iterateFiles(dir)

    def createImage(self, file):
        # 384/8 = 48 max len string
        if file.__len__() > 48:
            sys.exit(-1)
        self.writeSentence(file, 384)
        with open(file, 'rb') as f:
            text = f.read()
            self.writeSentence(text)

    def writeSentence(self, text, padding=-1):
        '''
        :param text: What we want to write
        :param padding: If we have a string with len 30, but our padding is 48, we'll add enough padding to make it len 48
        '''
        if type(text) is str:
            text = text.encode("utf-8")
        if padding != -1:
            bytearray_obj = bytearray(text)
            for i in range(padding//8 - text.__len__()):
                bytearray_obj.insert(0, 0)
            text = bytes(bytearray_obj)
        tempAddLater = ""
        for i in range(8 - self.bandwidth // 2):
            tempAddLater += "0"
        for byte in text:
            bits = bin(byte)[2:]
            toAdd = 8 - bits.__len__()
            for i in range(toAdd):
                bits = '0' + bits
            avaibleSlots = 8 - self.colors["colors"][self.colors["idx"]].__len__() - self.bandwidth // 2
            if avaibleSlots == 0:
                self.colors["colors"][self.colors["idx"]] += tempAddLater
                self.colors["idx"]+=1
                if self.colors["idx"] == 3:
                    self.draw()
                    self.colors["idx"] = 0
                    for i in range(3):
                        self.colors["colors"][i] = ""
                avaibleSlots = 8 - self.colors["colors"][self.colors["idx"]].__len__() - self.bandwidth // 2
            firstPart = bits[:avaibleSlots]
            secondPart = bits[avaibleSlots:]
            self.colors["colors"][self.colors["idx"]] += firstPart + tempAddLater
            self.colors["idx"] += 1
            if self.colors["idx"] == 3:
                self.draw()
                self.colors["idx"] = 0
                for i in range(3):
                    self.colors["colors"][i] = ""
            self.colors["colors"][self.colors["idx"]] = secondPart

    def draw(self):
        self.canvas = cv2.rectangle(self.canvas, (self.idxColumn, self.idxRow), (self.idxColumn + self.pixelDimensions, self.idxRow + self.pixelDimensions),
                                    (int(self.colors["colors"][0], 2), int(self.colors["colors"][1], 2), int(self.colors["colors"][2], 2)), -1)
        cv2.imshow("Testing", self.canvas)
        cv2.waitKey(1)
        self.idxColumn += self.pixelDimensions
        if self.idxColumn >= self.width:
            self.idxColumn = 0
            self.idxRow += self.pixelDimensions
            if self.idxRow >= self.height:
                b = 0








    def generateVideo(self):
        pass

    def createOutputDirectory(self):
        # Create the directory if it does not exist
        if not os.path.exists("outputTemp"):
            os.makedirs("outputTemp")
        else:
            # We dont want anything in the output directory if it already exists
            self.deleteOutputDirectory()
            self.createOutputDirectory()

    def deleteOutputDirectory(self):
        shutil.rmtree("outputTemp")

