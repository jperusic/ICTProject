## Import the libraries for plotting and data reading
import matplotlib.pyplot as plt
import csv

## The below code before the definition of the plot function will not be needed in the final version,
## The GUI will eventually handle this, but this is just for testing purposes for now
## Opens the file target
## Specifies the file name to be used when writing out new data
## Imports the file into a variable labelled 'data'
## Closes the file
inFile = open(r'C:\Users\JordanWinter\Documents\GitHub\ICTProject\raman_01_normalised.txt')
fileName = inFile.name[-23:-15] + "_normalised_graph.txt" 
data = inFile.read().splitlines()
inFile.close

def plot(fp):

    ## Declaration of the variables used in the process
    w = [] ## Holds the wavelength data to plot
    s1 = [] ## Holds the spectra data to plot
    s2 = [] ## Holds the spectra data to plot
    s3 = [] ## Holds the spectra data to plot

    valuesToPlot = 0 ## Defaults the plotting requirements to 0

    ## Read the data and split at "," save individual values to plot
    ## For each entry in the plot values
    plot = csv.reader(data, delimiter=",")  
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
            plt.title(fileName[:8] + "Data is corrupt.")
        ## If one spectra value exists
        ## Plot the wavelength and spectra values with their labels
        if valuesToPlot==2:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra, linewidths=1")
            plt.scatter(w,s1, label="Spectra", linewidths=1)
            plt.title('Spectra Reading for ' + fileName[:8])
        ## If two spectra value exist
        if valuesToPlot==3:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra 1, linewidths=1")
            #plt.plot(s2, label="Spectra 2, linewidths=1")
            plt.scatter(w,s1, label="Spectra 1", linewidths=1)
            plt.scatter(s2, label="Spectra 2", linewidths=1)
            plt.title('Spectra Reading for ' + fileName[:8])
        ## If three spectra value exist
        if valuesToPlot==4:
            ## Options for line plot vs. scatter plot - Scatter in use   
            #plt.plot(w,s1, label="Spectra 1, linewidths=1")
            #plt.plot(s2, label="Spectra 2, linewidths=1")
            #plt.plot(s3, label="Spectra 3, linewidths=1")
            plt.scatter(w,s1, label="Spectra 1", linewidths=1)
            plt.scatter(s2, label="Spectra 2", linewidths=1)
            plt.scatter(s3, label="Spectra 3", linewidths=1)
            plt.title('Spectra Reading for ' + fileName[:8])

        plt.xlabel('Wavelength') ## Title for the X axis   
        plt.ylabel('Spectra') ## Title for the Y axis
        plt.legend() ## Create a legend
        plt.show() ## Display the graph to the user

## Calls the function 'plot', passing in the inFile variable as the path name
plot(inFile)