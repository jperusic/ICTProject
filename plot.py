## import libraries for plotting and data reading
import matplotlib.pyplot as plt
import csv

## Open  file target
## specify file name to be used when writing out new data
## imported file titled data
## close the in file
inFile = open("//Users/JarradPerusic/Desktop/ICTCode/plot/raman_01_normalised.txt", "r")
fileName = inFile.name[-23:-15] + "_normalised_graph.txt" 
data = inFile.read().splitlines()
inFile.close

## declaration of variables used in the process
w = [] ## holds wavelength data to plot
s1 = [] ## holds spectra data to plot
s2 = [] ## holds spectra data to plot
s3 = [] ## holds spectra data to plot

valuesToPlot = 0 ## defaults plotting requirements to 0

## read data and split at "," save individual values to plot
## for each entry in the plot values
plot = csv.reader(data, delimiter=",")  
for row in plot:
    ## if the error message was thrown (only 1 message) - graph will show with no content
    if len(row) == 1:
        valuesToPlot = 1
    ## if one spectra value  
    ## append as plottable values to lists  
    if len(row) > 1:
        w.append(float(row[0]))
        s1.append(float(row[1]))
        valuesToPlot = 2
        ## if two spectra values
        if len(row) > 2:
            s2.append(float(row[2]))
            valuesToPlot = 3
        ## if three spectra values
        if len(row) > 3:    
            s3.append(float(row[3]))
            valuesToPlot = 4

## if there is plottable data 
if valuesToPlot > 0:
    ## if data present, but processing error 
    if valuesToPlot==1:
        plt.title(fileName[:8] + " data is corrupt")
    ## if one spectra value
    ## plot the wavelength and spectra values with labels
    if valuesToPlot==2:
        plt.plot(w,s1, label="Spectra")
        plt.title('Spectra Reading for ' + fileName[:8])
    ## if two spectra value
    if valuesToPlot==3:
        plt.plot(w,s1, label="Spectra 1")
        plt.plot(s2, label="Spectra 2")
        plt.title('Spectra Reading for ' + fileName[:8])
    ## if three spectra value
    if valuesToPlot==4:
        plt.plot(w,s1, label="Spectra 1")
        plt.plot(s2, label="Spectra 2")
        plt.plot(s3, label="Spectra 3")
        plt.title('Spectra Reading for ' + fileName[:8])

    ## title the x and y axis, create a legend and display the graph
    plt.xlabel('Wavelength')
    plt.ylabel('Spectra')
    plt.legend()
    plt.show()