# Semi-Automated Camera Trap Processing 
## Jameson Andrews, Andrew Coleman, and Yassine Dhouib Senior Project in Computer Science

# Overview
This project was designed to be used by the Hamilton College Biology department in the data collection of animals in the glens around campus. The project allows a user to select images to be classified, organized, displayed, and exported to aid in research.

# How to Install On Your Computer:
To install this project on your computer:
1. Ensure you have python installed on your machine. If you do not know how to check this open a terminal (mac) or cmd (windows) window and type:
```bash
python --version
```
I would recommend having a version between 3.7 and 3.10, however others may work. If the above command does not work, try:
```bash
python3 --version
```
If neither of these worked then you do not have python. To install [go here for windows](https://docs.python.org/3/using/windows.html) [and here for mac](https://macpaw.com/how-to/install-python-mac) 

2. Create a new directory on your machine where you would like the CameraTrapThesis to live.

3. Go to a terminal (mac) or cmd (windows) window and navigate to the directory you just created:
windows:
```bash
cd "path\to\directory"
```
mac:
```bash
cd "path/to/directory"
```

4. Go to [go to this github repository](https://github.com/jamandrews10/CameraTrapThesis/tree/production), and click the green code button. Copy the link displayed. Then go back to your terminal window and type
```bash
git clone
```
and paste the link before clicking enter. This will create a new folder titled: "CameraTrapThesis". 

5. Type the commands:
```bash
cd CameraTrapThesis
pip install -r requirements.txt
```
This will install the majority of packages needed to run the program.

6. Type the command:
```bash
pip install tensorflow
```
This package must be installed seperate from the others.

7. Next, download the models from this [google drive link](https://drive.google.com/drive/folders/1-l_WhgWwZQCCR9G0dE11eaKaDSrQJxfj). Put these models in a folder called "models" in your current directory.

1. Now run:
```bash
python mainwindow.py
```
This will open our user interface onto your computer with our pre-loaded images.

This should be all of the steps needed in order to get the project installed on your computer.

# How to Install If Another User Has Already Installed On Your Computer
If another user has installed this to the full computer (and not just their local user) then there are fewer steps needed to get the program ready for use.

1. Go to a terminal (mac) or cmd (windows) window and navigate to the directory where the "CameraTrapThesis" files are located:
windows:
```bash
cd "path\to\directory\CameraTrapThesis"
```
mac:
```bash
cd "path/to/directory/CameraTrapThesis"
```
2. Type the commands:
```bash
cd CameraTrapThesis
pip install -r requirements.txt
```
This will install the majority of packages needed to run the program.

3. Type the command:
```bash
pip install tensorflow
```
This package must be installed seperate from the others. 

1. Now run:
```bash
python mainwindow.py
```
This will open our user interface onto your computer with our pre-loaded images.

If you are able to see the Image Gallary, then you are installed and ready to use.

# How to Run:
To run the program you need to navigate using your terminal to the location of the program and run one command. There are many ways to create shortcuts in order to run this straight from your desktop. We recommend [creating a batch file](https://www.windowscentral.com/how-create-and-run-batch-file-windows-10).

1. Go to a terminal (mac) or cmd (windows) window and navigate to the directory where the "CameraTrapThesis" files are located:
windows:
```bash
cd "path\to\directory\CameraTrapThesis"
```
mac:
```bash
cd "path/to/directory/CameraTrapThesis"
```

2. Run:
```bash
python mainwindow.py
```
This will open our user interface onto your computer with our pre-loaded images.

3. Add a folder of images you want to identify into the input folder. Note: make sure to add these files in a new folder to organize them by the camera they were taken from.

4. Click the Reload button on the user interface to classify and display these new images (this may take some time).

5. Navigate through the user interface to see all of the different ways you can sort, display, and export your images.

# How to Run on Professor Guidens Lab Computer:
On each users desktop there is an icon called CameraTrap. Click this to open the interface and run the program. Also on the desktop is a folder with the same name. In the folder is where you can see the inputs and exports from the program. If these files are not there, you have to follow the guide for "How to Install If Another User Has Already Installed On Your Computer".
