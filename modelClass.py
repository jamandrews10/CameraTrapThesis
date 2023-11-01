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
        self.deerModel = keras.models.load_model('deerModel.keras')
    
    def predictDeerModel(self, img):
        """
        Predicts liklihood of a Deer
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.deerModel.predict(pictureArray)
        # print (prediction)
        self.testResults['deer'] = (prediction[0][0])

    def loadSquirrelModel(self):
        """
        Loads the Squirrel Classification Model
        """
        self.squirrelModel = keras.models.load_model('squirrelModel.keras')
    
    def predictSquirrelModel(self, img):
        """
        Predicts liklihood of a Squirrel
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.squirrelModel.predict(pictureArray)
        # print (prediction)
        self.testResults['squirrel'] = (prediction[0][0])
    
    def loadRabbitModel(self):
        """
        Loads the Rabbit Classification Model
        """
        self.rabbitModel = keras.models.load_model('rabbitModel.keras')
    
    def predictRabbitModel(self, img):
        """
        Predicts liklihood of a Rabbit
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.rabbitModel.predict(pictureArray)
        # print (prediction)
        self.testResults['rabbit'] = (prediction[0][0])

    def loadFoxModel(self):
        """
        Loads the Fox Classification Model
        """
        self.foxModel = keras.models.load_model('foxModel.keras')
    
    def predictFoxModel(self, img):
        """
        Predicts liklihood of a Fox
        @Param: the image to predict on
        """
        testPicture = load_img(img, target_size=(224,224))
        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)
        prediction = self.foxModel.predict(pictureArray)
        # print (prediction)
        self.testResults['fox'] = (prediction[0][0])
    
    def predictAll(self, img):
        """
        Predicts liklihood of all animals
        @Param: the image to predict on
        """
        self.loadDeerModel()
        self.predictDeerModel(img)
        self.loadSquirrelModel()
        self.predictSquirrelModel(img)
        self.loadRabbitModel()
        self.predictRabbitModel(img)
        self.loadFoxModel()
        self.predictFoxModel(img)
    
    def displayPredictions(self):
        """
        Displays the Dictrionary with the predictions
        """
        for item in self.testResults:
            print(item, " : ", self.testResults[item])

    def mostLikelyAnimal(self):
        """
        Gives the animal with the highest likely hood
        @Return: The name of the animal with the highest prediction level
        """
        return max(self.testResults, key = self.testResults.get)
        
def main():
    allModels = MultiModels()
    allModels.predictAll('extraTest/testSquirrel/97.jpg___crop01_md_v5a.0.0.pt.jpg')
    allModels.displayPredictions()
    print(allModels.mostLikelyAnimal())


if __name__ == "__main__":
    main()