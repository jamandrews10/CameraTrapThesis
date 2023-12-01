import os
import numpy as np
import tensorflow as tf
import keras
from tensorflow.keras import models
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.applications.vgg19 import preprocess_input

class MultiModels:
    """
    A Class to hold the different models and manage predictions
    """
    def __init__(self):
        """
        Initializes the dictionary to be filled with prediciton
        """
        self.testResults = {'cat'      : 0,
                            'coyote'   : 0,
                            'deer'     : 0,
                            'dog'      : 0,
                            'fox'      : 0,
                            'rabbit'   : 0,
                            'squirrel' : 0}
                            # Maybe groundhogs
    
    def loadDeerModel(self):
        """Loads the Deer Classification Model"""
        self.currentModel = keras.models.load_model('../models/deerModel.keras')
    
    def predictDeerModel(self, img):
        """
        Predicts liklihood of a Deer
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['deer'] = (prediction[0][0])

    def loadSquirrelModel(self):
        """
        Loads the Squirrel Classification Model
        """
        self.currentModel = keras.models.load_model('../models/squirrelModel.keras')
    
    def predictSquirrelModel(self, img):
        """
        Predicts liklihood of a Squirrel
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['squirrel'] = (prediction[0][0])
    
    def loadRabbitModel(self):
        """
        Loads the Rabbit Classification Model
        """
        self.currentModel = keras.models.load_model('../models/rabbitModel.keras')
    
    def predictRabbitModel(self, img):
        """
        Predicts liklihood of a Rabbit
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['rabbit'] = (prediction[0][0])

    def loadFoxModel(self):
        """
        Loads the Fox Classification Model
        """
        self.currentModel = keras.models.load_model('../models/foxModel.keras')
    
    def predictFoxModel(self, img):
        """
        Predicts liklihood of a Fox
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['fox'] = (prediction[0][0])

    def loadDogModel(self):
        """
        Loads the Dog Classification Model
        """
        self.currentModel = keras.models.load_model('../models/dogModel.keras')
    
    def predictDogModel(self, img):
        """
        Predicts liklihood of a Dod
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['dog'] = (prediction[0][0])

    def loadCatModel(self):
        """
        Loads the cat Classification Model
        """
        self.currentModel = keras.models.load_model('../models/catModel.keras')
    
    def predictCatModel(self, img):
        """
        Predicts liklihood of a Cat
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['cat'] = (prediction[0][0])
    
    def loadCoyoteModel(self):
        """
        Loads the Coyote Classification Model
        """
        self.currentModel = keras.models.load_model('../models/coyoteModel.keras')
    
    def predictCoyoteModel(self, img):
        """
        Predicts liklihood of a Coyote
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['coyote'] = (prediction[0][0])
    
    # def loadWeaselModel(self):
    #     """
    #     Loads the Weasel Classification Model
    #     """
    #     self.currentModel = keras.models.load_model('../models/weaselModel.keras')
    
    # def predictWeaselModel(self, img):
    #     """
    #     Predicts liklihood of a Weasel
    #     @Param: the image to predict on
    #     """
    #     testPicture = load_img(img, target_size=(224,224))
    #     pictureArray = img_to_array(testPicture)
    #     pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
    #     pictureArray = preprocess_input(pictureArray)
    #     prediction = self.currentModel.predict(pictureArray)
    #     # print (prediction)
    #     self.testResults['weasel'] = (prediction[0][0])

    # def loadMouseModel(self):
    #     """
    #     Loads the Weasel Classification Model
    #     """
    #     self.currentModel = keras.models.load_model('../models/mouseModel.keras')

    # # def loadAllModels()
    
    # def predictMouseModel(self, img):
        """
        Predicts liklihood of a Weasel
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.currentModel.predict(pictureArray)
        # print (prediction)
        self.testResults['mouse'] = (prediction[0][0])
    
    def predictAll(self, img):
        """
        Predicts liklihood of all animals
        @Param: the image to predict on
        """
        self.testResults = {'cat' : 0, 'coyote' : 0, 'deer' : 0, 'dog' : 0, 
                            'fox' : 0, 'mouse' : 0, 'squirrel' : 0}

        self.loadDeerModel()
        self.predictDeerModel(img)
        if self.testResults['deer'] >= 0.5:
            return
        self.loadSquirrelModel()
        self.predictSquirrelModel(img)
        if self.testResults['squirrel'] >= 0.5:
            return
        self.loadFoxModel()
        self.predictFoxModel(img)
        if self.testResults['fox'] >= 0.75:
            return
        self.loadDogModel()
        self.predictDogModel(img)
        if self.testResults['dog'] >= 0.75:
            return
        self.loadCatModel()
        self.predictCatModel(img)
        if self.testResults['cat'] >= 0.75:
            return
        self.loadCoyoteModel()
        self.predictCoyoteModel(img)
        if self.testResults['coyote'] >= 0.75:
            return
        self.loadRabbitModel()
        self.predictRabbitModel(img)
        if self.testResults['rabbit'] >= 0.75:
            return
    
    def getPredictions(self):
        """
        Returns the Dictrionary with the predictions
        """
        return self.testResults

    def mostLikelyAnimal(self):
        """
        Gives the animal with the highest likely hood
        @Return: The name of the animal with the highest prediction level
        """
        return max(self.testResults, key = self.testResults.get)
    
    def highestPercent(self):
        """
        Gives the animal with the highest likely hood
        @Return: The name of the animal with the highest prediction level
        """
        return (self.testResults[self.mostLikelyAnimal()])
    

def realTest(allModels, outputFile, otherFile):
    i = 0
    # cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Animals: \n")
    results = [0, 0, 0, 0, 0, 0, 0]
    directory = '../testData'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            # outputFile.write(str(i))
            # outputFile.write(": ")
            # outputFile.write(str(f))
            # outputFile.write("\n")
            allModels.predictAll(f)
            # outputFile.write(str(allModels.getPredictions()))
            animal = allModels.mostLikelyAnimal()
            outputFile.write(animal)
            otherFile.write(str(allModels.highestPercent()))
            outputFile.write("\n")
            otherFile.write("\n")
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1  
            elif animal == 'rabbit':
                results[5] += 1
            elif animal == 'squirrel':
                results[6] += 1
        i += 1
    outputFile.write("Test Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")
    

# def catTest(allModels, outputFile):
    # i = 0
    # # cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Cats: \n")
    # results = [0, 0, 0, 0, 0, 0, 0]
    # directory = 'testData/testCat'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         animal = allModels.mostLikelyAnimal()
    #         outputFile.write(str(allModels.getPredictions()))
    #         outputFile.write("\n")
    #         # animal = allModels.mostLikelyAnimal()
    #         if animal == 'cat':
    #             results[0] += 1
    #         elif animal == 'coyote':
    #             results[1] += 1
    #         elif animal == 'deer':
    #             results[2] += 1
    #         elif animal == 'dog':
    #             results[3] += 1
    #         elif animal == 'fox':
    #             results[4] += 1  
    #         elif animal == 'rabbit':
    #             results[5] += 1
    #         elif animal == 'squirrel':
    #             results[6] += 1
    #     i += 1
    # outputFile.write("Cat Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n\n")

def coyoteTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Coyotes: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testCoyote'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Coyote Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def deerTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Deer: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testDeer'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Deer Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def dogTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Dogs: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testDog'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Dog Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def foxTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Fox: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testFox'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Fox Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def rabbitTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Rabbit: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testRabbit'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Rabbit Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def squirrelTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    outputFile.write("Squirrel: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testSquirrel'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Squirrel Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def weaselTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, mouse, rabbit, squirrel, weasel
    outputFile.write("Weasel: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testWeasel'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Weasel Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def mouseTest(allModels, outputFile):
    i = 0
    #cat, coyote, deer, dog, fox, mouse, rabbit, squirrel, weasel
    outputFile.write("Mouse: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testMouse'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.getPredictions()))
            outputFile.write("\n\n")
            animal = allModels.mostLikelyAnimal()
            if animal == 'cat':
                results[0] += 1
            elif animal == 'coyote':
                results[1] += 1
            elif animal == 'deer':
                results[2] += 1
            elif animal == 'dog':
                results[3] += 1
            elif animal == 'fox':
                results[4] += 1
            elif animal == 'mouse':
                results[5] += 1   
            elif animal == 'rabbit':
                results[6] += 1
            elif animal == 'squirrel':
                results[7] += 1
            elif animal == 'weasel':
                results[8] += 1
        i += 1
    outputFile.write("Mouse Results: ")
    outputFile.write(str(results))
    outputFile.write("\n\n")

def main():
    allModels = MultiModels()

    img = ('../testData/IMG_0071 (3).JPG___crop00_md_v5a.0.0.pt.jpg')
    allModels.predictAll(img)
    testPicture = load_img(img, target_size=(224,224))
    testPicture.show()
    print(allModels.getPredictions())
    print(allModels.mostLikelyAnimal(), allModels.highestPercent())
    
    # outputFile = open("outputFilenum10.txt", "a")  
    # otherFile = open("outputFile7.txt", "a") 
    # directory = '../testData'
    
    
    
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         # outputFile.write(str(i))
    #         # outputFile.write(": ")
    #         outputFile.write(str(f))
            # outputFile.write("\n")



    # realTest(allModels, outputFile, otherFile)
    # catTest(allModels, outputFile)
    # coyoteTest(allModels, outputFile)
    # deerTest(allModels, outputFile)
    # dogTest(allModels, outputFile)
    # foxTest(allModels, outputFile)
    # squirrelTest(allModels, outputFile)
    # rabbitTest(allModels, outputFile)
    # weaselTest(allModels, outputFile)
    # mouseTest(allModels, outputFile)


if __name__ == "__main__":
    main()