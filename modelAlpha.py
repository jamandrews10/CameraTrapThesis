#####################################
###### TITLE: modelAlpha ############
###### AUTHOR: Jameson Andrews ######
###### DATE: 09/13/2023 #############
#####################################

#### Editor   |  Date |  EDITS:
#   JAMESON   | 09/13 | initial creation
#########################################

import numpy as np
import tensorflow as tf
import keras
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions
from keras.applications.vgg19 import VGG19



def loadModel():

    tf.keras.applications.VGG16(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",
    )




def main():
    loadModel()




if __name__ == "__main__":
    main()






