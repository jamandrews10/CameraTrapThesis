import os
import keras
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions
import sqlite3



model = keras.models.load_model('alphaModel.keras')

# Get all files from the folders
cropped_folder = '/Users/yassine/TrapCam/alphaCropped'
uncropped_folder = '/Users/yassine/TrapCam/alphaUncropped'
cropped_files = sorted(os.listdir(cropped_folder))
uncropped_files = sorted(os.listdir(uncropped_folder))

conn = sqlite3.connect('alpha.db')
# clear the database
conn.execute("DELETE FROM PATHS")

id = 0
# Iterate over all files
for cropped_file, uncropped_file in zip(cropped_files, uncropped_files):
    # Skip files with the name ".DS_Store"
    if cropped_file == ".DS_Store" or uncropped_file == ".DS_Store":
        continue

    # Check if the first 8 characters of the file names are the same
    if cropped_file[:8] == uncropped_file[:8]:
        testPicture_path = os.path.join(cropped_folder, cropped_file)
        originalPicture_path = os.path.join(uncropped_folder, uncropped_file)

        testPicture = load_img(testPicture_path, target_size=(224,224))
        originalPicture = load_img(originalPicture_path)

        pictureArray = img_to_array(testPicture)
        pictureArray = pictureArray.reshape((1, pictureArray.shape[0], pictureArray.shape[1], pictureArray.shape[2]))
        pictureArray = preprocess_input(pictureArray)

        yhat = model.predict(pictureArray)

        predClass = "Deer" if (yhat[0][0]>yhat[0][1]) else "notDeer"

        #Putting the same path as images in project folder to demonstrate that we get paths from db
        conn.execute("INSERT into Paths Values (?,?,?,?)",(id,originalPicture_path,testPicture_path, predClass))
        id += 1


cursor = conn.execute("SELECT id, imagePath, croppedPath, class from PATHS")
#for row in cursor:
#    print ("ID = ", row[0])
#   print ("Path = ", row[1])
#    print ("CroppedPath = ", row[2])
#    print ("Class = ", row[3], "\n")

#conn.close()
