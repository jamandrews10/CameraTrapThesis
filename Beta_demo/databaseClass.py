from PyQt6 import QtSql, QtGui
import sqlite3
import numpy
import datetime
import os
import csv
from my_run_detector_batch import *
import crop_detections
import modelClass

class DataBase:
    def __init__(self, path = 'beta.db'):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(path)
        self.path = path
        if not self.db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
            QtGui.qApp.tr("Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read "
                "the Qt SQL driver documentation for information "
                "how to build it.\n\n" "Click Cancel to exit."),
            QtGui.QMessageBox.Cancel)

            return False
        query = QtSql.QSqlQuery()

        query.exec("CREATE TABLE paths(ID INTEGER PRIMARY KEY, "
            "IMAGEPATH TEXT, CROPPEDPATH TEXT, CLASSIFICATION TEXT, CONFIRMED TEXT, CAMERA TEXT, DATETIME TEXT, DAYNIGHT TEXT, TAGS TEXT)")
        
    def connect(self):
        return sqlite3.connect(self.path)
    
    def addRow(self, values):
        """
        Adds a new row to the database
        @Param values - an array of values for each column except ID
        
        EX: myDatabase.addRow(['\images\example0.jpg', '\cropped\cropped_example0.jpg', 'possum', 'False', 'CameraB', 'night', ["tag1", "tag2"]])
        """
        values[-1] = ','.join(values[-1])
        values = [None]+values
        # Might actually want to put this code in the input function
        # for img in values:
        #     values.insert(datetime.fromtimestamp(os.path.getmtime(img[1])).date())
        conn = self.connect()
        conn.execute("INSERT into Paths Values ("+("?,"*len(values))[:-1]+")", values)
        conn.commit()
        conn.close()

    def deleteRow(self, id):
        """
        Deletes a row from the database
        @Param id - the id of the row to delete (integer or string)
        """
        conn = self.connect()
        conn.execute("DELETE FROM Paths WHERE ID=?", (id,))
        conn.commit()
        conn.close()

    def clear(self):
        """
        Deletes all rows from database
        """
        conn = self.connect()
        conn.execute("DELETE FROM Paths")
        conn.commit()
        conn.close()

    def getRow(self, id):
        """
        Retrieves a row from the database as a list
        @Param id - the id of the row to retrieve (integer or string)
        @Returns a one dimensional array of the values of the specified row
        """
        conn = self.connect()
        cursor = conn.execute("SELECT * FROM Paths WHERE ID=?", (id,))
        output = []
        for row in cursor:
            for col in row:
                output.append(col)
        conn.close()
        return output
    
    def changeValue(self, id, colToChange, value):
        """
        Changes the value of one column for one row
        @Param id - the id of the row to change
        @Param colToChange - the name of the column to change
        @Param value - the value to change 
        """
        conn = self.connect()
        conn.execute("UPDATE Paths SET {} = ? WHERE ID = ?".format(colToChange), (value, id))
        conn.commit()
        conn.close()

    def filterRows(self, filter, filterValue):
        """
        Retrieves a list of rows from the database
        @Param filter - a string representing the name of the column to filter within
        @Param filterValue - the value to filter by
            ---set either parameter to '*' to retrieve all rows in the database
        @Returns a two dimensional array containg lists for each row that matches the filter
        """
        conn = self.connect()
        if (filter == '*' or filterValue == '*'):
            cursor = conn.execute("SELECT * FROM Paths")
        else:
            cursor = conn.execute("SELECT * FROM Paths WHERE {}=?".format(filter), (filterValue,))
        output = []
        for row in cursor:
            output_row = []
            for col in row:
                output_row.append(col)
            output.append(output_row)
        conn.close()
        return output
    
    def sortRows(self, rows, sortBy, reversed = False):
        """
        Sorts a list of rows by the specified column name
        @Param rows - a two dimensional array containg lists for each row (output of the 'filterRows()' method)
        @Param sortBy - a string representing the name of the column to sort by
        @Param reversed - an optional boolean to determine whether to sort in reverse order
        @Returns a two dimensional array containg lists for each row in sorted order
        """
        conn = self.connect()
        cursor = conn.execute("SELECT * FROM Paths")
        sortById = list(map(lambda x: x[0], cursor.description)).index(sortBy.upper())
        return sorted(rows, key = lambda x: x[sortById], reverse = reversed)
    
    def toCSV(self):
        conn = self.connect()
        cursor = conn.execute("SELECT * FROM Paths")

        with open("output.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)

    def detectNew(self,input_path, cropped_path):
        conn = self.connect()
        
        # cameraNames = []
        cameraPaths = [f.path for f in os.scandir(input_path) if f.is_dir()]
        for cameraPath in cameraPaths:
            imageQueue = []
            cameraPath = cameraPath.replace('\\','/')
            for imgName in os.listdir(cameraPath):
                imgPath = os.path.join(cameraPath,imgName).replace('\\','/')
                #Check that image does noe already exist in database
                if conn.execute("SELECT ID FROM Paths where IMAGEPATH = ?", (imgPath,)).fetchone() is None:
                    print("Adding", imgPath)
                    imageQueue.append(imgPath)
                else:
                    print("Already in:", imgPath)
            
            if len(imageQueue) == 0:
                print("No new images for", cameraPath)
                continue

            detector_file = 'c:\\megadetector\\md_v5a.0.0.pt'
            output_file='c:\\megadetector\\newDetections.json'
            threshold=0.5                   #This could be changed later if we want to implement a sensitivity slider

            self.detectCamera(imageQueue,detector_file,output_file,threshold)
            print("Done Detection for", cameraPath)

            #Create dirs for cropped images they dont already exist
            # croppedCameraPaths = [f.path for f in os.scandir(cropped_path) if f.is_dir()]
            croppedCameraPath = cameraPath.replace(input_path,cropped_path)
            print(croppedCameraPath)
            if not os.path.exists(croppedCameraPath):
                os.mkdir(croppedCameraPath)

            self.cropCamera(output_file,croppedCameraPath,cameraPath,threshold,imageQueue)
            print("Done Cropping for", cameraPath)


            #Now run our classification
            cropped_files = sorted(os.listdir(croppedCameraPath))
            uncropped_files = sorted(imageQueue)
            allModels = modelClass.MultiModels()

            # Iterate over all files
            for cropped_file, uncropped_file in zip(cropped_files, uncropped_files):
                # Skip files with the name ".DS_Store"
                if cropped_file == ".DS_Store" or uncropped_file == ".DS_Store":
                    continue

                testPicture_path = os.path.join(croppedCameraPath, cropped_file).replace("\\","/")
                originalPicture_path = os.path.join(cameraPath, uncropped_file).replace("\\","/")

                allModels.predictAll(testPicture_path)
                predClass = allModels.mostLikelyAnimal()
                print("found", predClass)
                daynight = ""
                hr = int(str(datetime.fromtimestamp(os.path.getmtime(originalPicture_path)).time())[:2])
                if hr>=7 and hr<18: 
                    daynight="day"
                else: 
                    daynight = "night" 
                print("detected",daynight)
                self.addRow([originalPicture_path, testPicture_path, predClass, 'Pending', cameraPath[cameraPath.rfind('/')+1:], datetime.fromtimestamp(os.path.getmtime(originalPicture_path)), daynight, []])
        
        print("Done!")


    

    def detectCamera(self,imageQueue, detector_file, output_file, threshold):
        detector_file=detector_file
        output_file = output_file
        threshold = threshold
        include_max_conf=False
        quiet=True
        image_size=None
        use_image_queue=False
        ncores=0
        class_mapping_filename=None
        include_image_size=False
        include_image_timestamp=False
        include_exif_data=False


        assert os.path.exists(detector_file), \
        'detector file {} does not exist'.format(detector_file)
        assert 0.0 < threshold <= 1.0, 'Confidence threshold needs to be between 0 and 1'
        assert output_file.endswith('.json'), 'output_file specified needs to end with .json'
        
            
        results = []
        start_time = time.time()
        results = load_and_run_detector_batch(model_file=detector_file,
                                          image_file_names=imageQueue,
                                          confidence_threshold=threshold,
                                          results=results,
                                          n_cores=ncores,
                                          use_image_queue=use_image_queue,
                                          quiet=quiet,
                                          image_size=image_size,
                                          class_mapping_filename=class_mapping_filename,
                                          include_image_size=include_image_size,
                                          include_image_timestamp=include_image_timestamp,
                                          include_exif_data=include_exif_data)

        elapsed = time.time() - start_time
        images_per_second = len(results) / elapsed
        print('Finished inference for {} images in {} ({:.2f} images per second)'.format(
            len(results),humanfriendly.format_timespan(elapsed),images_per_second))

        write_results_to_file(results, output_file, 
                            detector_file=detector_file,include_max_conf=include_max_conf)


    def cropCamera(self,output_file,croppedCameraPath,cameraPath,threshold,imageQueue):
            crop_detections.main(detections_json_path=output_file,
            cropped_images_dir=croppedCameraPath,
            images_dir=cameraPath,
            container_url=None,
            detector_version=None,
            save_full_images=None,
            square_crops=True,
            check_crops_valid=None,
            confidence_threshold=threshold,
            threads=None,
            logdir='c:\\megadetector',
            imageQueue = imageQueue
            )
            print("Cropped new imgs in", cameraPath)
        



    def __str__(self):
        """
        Prints the values of for each row in the database
        """
        output = ""
        conn = self.connect()
        cursor = conn.execute("SELECT * from PATHS")
        for row in cursor:
            for col in row:
                output += str(col)+" | "
            output = output[:-1] + '\n'
        conn.commit()
        conn.close()
        return output

def main():
    # Creating a database with dummy data
    myData = DataBase()
    # myData.clear()
    # myData.addRow(["\images\example0.jpg", '\cropped\cropped_example0.jpg', 'possum', 'False', 'CameraB', 'faketime', 'night', ["tag1", "tag2"]])
    # myData.addRow(['\images\example3.jpg', '\cropped\cropped_example3.jpg', 'deer', 'False', 'CameraA', 'faketime','night', ["tag2", "tag3"]])
    # myData.addRow(['\images\example1.jpg', '\cropped\cropped_example1.jpg', 'fox', 'False', 'CameraC', 'faketime','night', ["tag1", "tag2"]])
    # myData.addRow(['\images\example2.jpg', '\cropped\cropped_example2.jpg', 'squirrel', 'False', 'CameraA', 'faketime','day', ["tag1", "tag5"]])

    # # Printing the database
    # print(myData)

    # # Printing all night rows
    # print(myData.filterRows("DAYNIGHT","night"))

    # # Printing all rows sorted alphabetically by classification
    # print(myData.sortRows(myData.filterRows("*","*"),"CLASSIFICATION"))

    # # Change confirmed to true for first row
    # myData.changeValue(1, "CONFIRMED", "True")

    # print(myData)
    # myData.toCSV()

    myData.detectNew("c:/input","c:/croppedImgs")
    print(myData)


if __name__ == "__main__":
    main()

        
    