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
        self.testResults = {'deer'     : 0,
                            'squirrel' : 0,
                            'mouse'    : 0,
                            'fox'      : 0,
                            'coyote'   : 0,
                            'dog'      : 0, #(pets off leash)
                            'cat'      : 0,
                            'rabbit'   : 0,
                            'weasel'   : 0,}
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
    
    def loadWeaselModel(self):
        """
        Loads the Weasel Classification Model
        """
        self.currentModel = keras.models.load_model('../models/weaselModel.keras')
    
    def predictWeaselModel(self, img):
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
        self.testResults['weasel'] = (prediction[0][0])
    
    def predictAll(self, img):
        """
        Predicts liklihood of all animals
        @Param: the image to predict on
        """
        self.testResults = {'deer' : 0, 'squirrel' : 0, 'mouse' : 0, 'fox' : 0, 'coyote' : 0, 'dog' : 0, 'cat' : 0,
                            'rabbit' : 0, 'weasel' : 0,}

        self.loadDeerModel()
        self.predictDeerModel(img)
        self.loadSquirrelModel()
        self.predictSquirrelModel(img)
        self.loadRabbitModel()
        self.predictRabbitModel(img)
        self.loadFoxModel()
        self.predictFoxModel(img)
        self.loadDogModel()
        self.predictDogModel(img)
        self.loadCatModel()
        self.predictCatModel(img)
        self.loadCoyoteModel()
        self.predictCoyoteModel(img)
        self.loadWeaselModel()
        self.predictWeaselModel(img)
    
    def displayPredictions(self):
        """
        Displays the Dictrionary with the predictions
        """
        return self.testResults
        # for item in self.testResults:
            # print(item, " : ", self.testResults[item])

    def mostLikelyAnimal(self):
        """
        Gives the animal with the highest likely hood
        @Return: The name of the animal with the highest prediction level
        """
        return max(self.testResults, key = self.testResults.get)
        
def main():
    allModels = MultiModels()
    # allModels.predictAll('../deerNightCrop.jpg')
    # allModels.displayPredictions()
    # print(allModels.mostLikelyAnimal())

    outputFile = open("outputFile.txt", "a")
    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Cats: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testCat'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Cat Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Coyotes: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testCoyote'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Coyote Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Deer: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testDeer'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Deer Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Dogs: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testDog'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Dog Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Fox: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testFox'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Fox Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Rabbit: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testRabbit'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Rabbit Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    # i = 0
    # #cat, coyote, deer, dog, fox, rabbit, squirrel
    # outputFile.write("Squirrel: \n")
    # results = [0, 0, 0, 0, 0, 0, 0, 0]
    # directory = 'extraTest/testSquirrel'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         outputFile.write(str(i))
    #         outputFile.write(": ")
    #         outputFile.write(str(f))
    #         outputFile.write("\n")
    #         allModels.predictAll(f)
    #         outputFile.write(str(allModels.displayPredictions()))
    #         outputFile.write("\n\n")
    #         animal = allModels.mostLikelyAnimal()
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
    #         elif animal == 'weasel':
    #             results[7] += 1
    #     i += 1
    # outputFile.write("Squirrel Results: ")
    # outputFile.write(str(results))
    # outputFile.write("\n")

    i = 0
    #cat, coyote, deer, dog, fox, rabbit, squirrel, weasel
    outputFile.write("Weasel: \n")
    results = [0, 0, 0, 0, 0, 0, 0, 0]
    directory = 'extraTest/testWeasel'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            outputFile.write(str(i))
            outputFile.write(": ")
            outputFile.write(str(f))
            outputFile.write("\n")
            allModels.predictAll(f)
            outputFile.write(str(allModels.displayPredictions()))
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
            elif animal == 'rabbit':
                results[5] += 1
            elif animal == 'squirrel':
                results[6] += 1
            elif animal == 'weasel':
                results[7] += 1
        i += 1
    outputFile.write("Weasel Results: ")
    outputFile.write(str(results))
    outputFile.write("\n")



if __name__ == "__main__":
    main()