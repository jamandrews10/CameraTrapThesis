"""
@Author: Jameson Andrews
@Date: 12/04/2023
@Links: https://drive.google.com/drive/folders/1-l_WhgWwZQCCR9G0dE11eaKaDSrQJxfj
@Description: Manages the models, makes predicitons, and organizes solution of 
              models. Model files can be found in the above drive.
"""
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
    
    def loadDeerModel(self):
        """Loads the Deer Classification Model"""
        self.currentModel = keras.models.load_model('models/deerModel.keras')
    
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
        self.currentModel = keras.models.load_model('models/squirrelModel.keras')
    
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
        self.currentModel = keras.models.load_model('models/rabbitModel.keras')
    
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
        self.currentModel = keras.models.load_model('models/foxModel.keras')
    
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
        self.currentModel = keras.models.load_model('models/dogModel.keras')
    
    def predictDogModel(self, img):
        """
        Predicts liklihood of a Dog
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
        Loads the Cat Classification Model
        """
        self.currentModel = keras.models.load_model('models/catModel.keras')
    
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
        self.currentModel = keras.models.load_model('models/coyoteModel.keras')
    
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