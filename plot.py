## Import the libraries for plotting and data reading
import matplotlib.pyplot as plt
import csv
from tkinter.filedialog import askopenfilename

listOfReadyFiles = []

def importReadyData():
    ## Using tkinter, allow a popup box to select the file
    path = askopenfilename()

    ## Set default variables
    importReadyData.fileName = ''
    importReadyData.data = ''

        ## Making sure that the file has '_normalised.txt' at the end
        ## If it does not, it will loop until the user selects one that does
    while path[-15:] != "_normalised.txt":
        print("File selected is not a normalised raman file. Please select another")
        path = askopenfilename()

        ## Once valid file has been selected, open it into the inFile variable
        ## Create a new filename for the graph
        ## Split each of the lines
        ## Then close the file
    else:
        inFile = open(path)
        importReadyData.fileName = inFile.name[-23:-15] + "_normalised_graph.txt" 
        importReadyData.data = inFile.read().splitlines()
        listOfReadyFiles.append(inFile.name[-23:-4])
        inFile.close
    return inFile


## Definition of the plot function
def plot(fp):

    ## Declaration of the variables used in the process
    w = [] ## Holds the wavelength data to plot
    s1 = [] ## Holds the spectra data to plot
    s2 = [] ## Holds the spectra data to plot
    s3 = [] ## Holds the spectra data to plot

    valuesToPlot = 0 ## Defaults the plotting requirements to 0

    ## Read the data and split at "," save individual values to plot
    ## For each entry in the plot values
    plot = csv.reader(importReadyData.data, delimiter=",")  
    for row in plot:
        ## If the error message was thrown (only 1 message) - the graph will show with no content
        if len(row) == 1:
            valuesToPlot = 1
        ## If one spectra value exists 
        ## Append as plottable values to lists  
        if len(row) > 1:
            w.append(float(row[0]))
            s1.append(float(row[1]))
            valuesToPlot = 2
            ## If two spectra values exist
            if len(row) > 2:
                s2.append(float(row[2]))
                valuesToPlot = 3
            ## If three spectra values exist
            if len(row) > 3:    
                s3.append(float(row[3]))
                valuesToPlot = 4

## If there is plottable data 
    if valuesToPlot > 0:
        ## If data is present, but processing error 
        if valuesToPlot==1:
            plt.title(importReadyData.fileName[:8] + "Data is corrupt.")
        ## If one spectra value exists
        ## Plot the wavelength and spectra values with their labels
        if valuesToPlot==2:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra, linewidths=1")
            plt.scatter(w,s1, label="Spectra", linewidths=1)
            plt.title('Spectra Reading for ' + importReadyData.fileName[:8])
        ## If two spectra value exist
        if valuesToPlot==3:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra 1, linewidths=1")
            #plt.plot(s2, label="Spectra 2, linewidths=1")
            plt.scatter(w,s1, label="Spectra 1", linewidths=1)
            plt.scatter(s2, label="Spectra 2", linewidths=1)
            plt.title('Spectra Reading for ' + importReadyData.fileName[:8])
        ## If three spectra value exist
        if valuesToPlot==4:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra 1, linewidths=1")
            #plt.plot(s2, label="Spectra 2, linewidths=1")
            #plt.plot(s3, label="Spectra 3, linewidths=1")
            plt.scatter(w,s1, label="Spectra 1", linewidths=1)
            plt.scatter(s2, label="Spectra 2", linewidths=1)
            plt.scatter(s3, label="Spectra 3", linewidths=1)
            plt.title('Spectra Reading for ' + importReadyData.fileName[:8])

        plt.xlabel('Wavelength') ## Title for the X axis   
        plt.ylabel('Spectra') ## Title for the Y axis
        plt.legend() ## Create a legend
        plt.show() ## Display the graph to the user

## Calls the function 'plot', passing in the inFile variable as the path name
## Only needed to test this file by itself, not needed when calling from GUI
##fp = importReadyData()
##plot(fp)