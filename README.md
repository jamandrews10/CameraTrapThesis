# Semi-Automated Camera Trap Processing 
## Jameson Andrews, Andrew Coleman, and Yassine Dhouib Senior Project in Computer Science

# Overview
This project was designed to aid the Hamilton College Biology department in the collection of animals in the glens around campus. The project allows a user to select images to be classified, organized, displayed, and exported to aid in research.

# How to Run
To run this project:
1. Create a new directory on your machine and pull the branch.

2. Navigate to this branch in your terminal

3. Run the command:
```bash
pip install -r requirements.txt
```
This will ensure that you have everything installed to run the code.

4. Next, download the models from the google drive link found in the header of 
```bash
\Program\modelClass.py
```
In this folder you will see the seven animal classifiers, and a single megadetector model. Leave these in the models directory to ensure the paths within the code do not get changed.

5. Now run:
```bash
python mainwindow.py
```
This will open our user interface onto your computer with our pre-loaded images.

6. Add a folder of images you want to identify into the input folder. Note: make sure to add these files in a new folder to organize them by the camera they were taken from.

7. Click the Reload button on the user interface to classify and display these new images (this may take some time).

8. Navigate through the user interface to see all of the different ways you can sort, display, and export your images.