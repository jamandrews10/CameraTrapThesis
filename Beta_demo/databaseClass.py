from PySide6 import QtSql, QtGui
import sqlite3
import numpy

class DataBase:
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('beta.db')
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
            "IMAGEPATH TEXT, CROPPEDPATH TEXT, CLASSIFICATION TEXT, CONFIRMED TEXT, CAMERA TEXT, DATETIME TIMESTAMP, DAYNIGHT TEXT, TAGS TEXT)")

    def connect(self):
        """
        Connects to the database in a given path
        """
        return sqlite3.connect('beta.db')
    
    def addRow(self, values):
        """
        Adds a new row to the database
        @Param values - an array of values for each column except ID
        
        EX: myDatabase.addRow(['\images\example0.jpg', '\cropped\cropped_example0.jpg', 'possum', 'False', 'CameraB', 'night', ["tag1", "tag2"]])
        """
        values[-1] = ','.join(values[-1])
        values = [None]+values
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
        #print("filter result: ", output)
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
        print(list(map(lambda x: x[0], cursor.description)))
        sortById = list(map(lambda x: x[0], cursor.description)).index(sortBy.upper())
        output = sorted(rows, key = lambda x: x[sortById], reverse = reversed)
        conn.close()
        #print("sort result: ", output)
        return output

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

# def main():
#     # Creating a database with dummy data
#     myData = DataBase()
#     myData.clear()
#     myData.addRow(['\images\example0.jpg', '\cropped\cropped_example0.jpg', 'possum', 'False', 'CameraB', 'night', ["tag1", "tag2"]])
#     myData.addRow(['\images\example3.jpg', '\cropped\cropped_example3.jpg', 'deer', 'False', 'CameraA', 'night', ["tag2", "tag3"]])
#     myData.addRow(['\images\example1.jpg', '\cropped\cropped_example1.jpg', 'fox', 'False', 'CameraC', 'night', ["tag1", "tag2"]])
#     myData.addRow(['\images\example2.jpg', '\cropped\cropped_example2.jpg', 'squirrel', 'False', 'CameraA', 'day', ["tag1", "tag5"]])

#     # Printing the database
#     print(myData)

#     # Printing all night rows
#     print(myData.filterRows("DAYNIGHT","night"))

#     # Printing all rows sorted alphabetically by classification
#     print(myData.sortRows(myData.filterRows("*","*"),"CLASSIFICATION"))

#     # Change confirmed to true for first row
#     myData.changeValue(1, "CONFIRMED", "True")
#     print(myData)


# if __name__ == "__main__":
#     main()

        
    
