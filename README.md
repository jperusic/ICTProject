# ICTProject

Written by Jarrad Perusic, Jordan Winter & Liuyu Zhao.

This project is a python-written program that will allow the importing of spectroscopy data, so that it can be normalised, 
viewed, plotted on a graph, and then exported for future plotting.



## Installation
This program has been created to be portable for ease of use. After you have downloaded the 'cRaman Installer', run it and
this will install to your chosen location. Included in the directory is a 'cRaman System Shortcut' file. Move this file to your
Desktop. You will now be able to double-click this shortcut file to begin the program.

You will need python installed on your machine to be able to run this software. This can be downloaded from: 
https://www.python.org/downloads/

If the program does not run or is missing some stuff, you may need to install the packages listed in the 'Required Packages.txt'.
Simply paste each single line in that .txt file into a Command Line and hit enter, allowing the packages to install.



## Files
The root directory will contain the following files
- cRaman System Shortcut
- data_process.py
- gui_app.py
- plot_tool.py
- README.md
- Required Packages.txt



## Importing Data Tab

### Importing Raw Files
- To import a raw data file(s), just select the 'Import Raw' button on the right-hand side. From here you will see a window pop up. 
- In this window, select one or more files that you would like to import (must be .txt format)
- After you are happy that you have selected all the files that you need, now hit Open.
- You should now see those select files sitting in the first pane of the program under the 'Raw' heading.

### Importing Already Normalised Files
- Just like the raw files, you will select the 'Import Normalised' button on the right-hand side of the first tab.
- Select the files you wish to open in the popup window.
- Once you are happy with the selection, hit 'Open'.
- You should now see these files in the second pane, under the 'Normalised' heading.

### Setting the Wave Shift
- To set the Wave Shift of your newly imported Raw Files, you have two options:
  #### Individually
  - You may choose individual shift values for each raw file by setting this in the Wave Shift column in the Raw pane.
  #### Batch Set
  - If you would like to set a single value across all your raw files, you may select the 'Batch Set Shift' button on the right-hand
  side of the interface, and enter in the value.
  - Once you have entered in this value, hit the 'OK' button to set this.
  
### Clearing Files
- To clear files in either pane, simply click their respective 'Clear' button on the right-hand side of the interface.

### Normalising
- To normalise the files that you just imported, you have two options:
  #### Individually
  - You may choose individual files to normalise by hitting their corresponding 'Normalise' button in the Raw pane.
  #### Batch Normalise
  - If you would like to normalise all Raw files at once, simply click the 'Batch Normalise' button on the right-hand side of 
  the interface

### Importing a Labbook
- To import a Labbook, simply click the 'Import Labbook' button on the bottom left-hand corner of the interface.



## Normalised Data Tab

### Viewing Normalised Data
- To view your normalised data, select the file you wish to view in the dropdown menu near the top of the Nomalised Data tab.
- You should now see the data in the scrollable pane below



## Plot Data Tab
- To plot your data after importing and normalising, simply head to the Plot Data tab.
- From here you can choose which file you would like to plot in the drop-down menu.
- Once happy with your selection, you may also choose if you would like a scatter graph, or a line graph.
- Hitting the 'Plot' button will now generate your graph below.



## Exporting
- Your nomalised data files will be exported automatically after they have been run through the normalisation process. 
- Check the same path location that the files were imported from. There should be a new folder called 'Normalised' where the normalised
files will be stored. 
- They will be named '{originalFileName}_normalised.txt'



## Contact the Developers
If you have any issues or feedback you would like to relay to us, we can be reached at 
