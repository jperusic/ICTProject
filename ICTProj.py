## Open raman file target
infile = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")

## declaration of variables used in the process
waves = [] ## holds wavelength name values
count = 0 ## holds value used to determine the number of unique wavelength names
n1 = [] ## empty list to hold spectra 1 values
n2 = [] ## empty list to hold spectra 2 values
n1Total = 0 ## holds the sum of values in n1 list
n1Average=0 ## holds average for values in n1 list
n1List = [] ## empty list to hold all average values for spectra 1
n2Total = 0 ## holds the sum of values in n2 list
n2Average=0 ## holds average for values in n2 list
n2List = [] ## empty list to hold all average values for spectra 2
occurance = 0 ## holds value used to determine the number of frames in the file

## imported file titled data
data = infile.readlines()

## for each line of the imported file
for line in data: 
    
    ## add the first three characters in the line to waveList and remove duplicate values
    waves.append(line[:3])
    waveList = list(dict.fromkeys(waves))

## while count is less than the length of the waveList 
while count < len(waveList):
    
    ## for each line of the imported file
    for line in data: 
        
        ## if first three characters of the line are equal to the referenced wave length name
        
        if line[:3]==waveList[count]:
            ## add that lines spectra values to the relevant list and increase the occurances of matching lines
            n1.append(int(line[4:7]))
            n2.append(int(line[8:11]))
            occurance = occurance + 1  
    
    ## if there was a match found during the if loop
    if occurance > 0:

        ## add together all the values that were found to get the total
        ## find the average value of all instances found and round to 1 decimal point
        ## add the average values to a list with the other average values found
        n1Total=int(sum(n1))
        n1Average=round(n1Total/occurance, 1)
        n1List.append(n1Average)

        n2Total=int(sum(n2))
        n2Average=round(n2Total/occurance, 1)
        n2List.append(n2Average)

    ## empty the list used to hold found values so they can be used for the next unique wavelength
    n1 = []
    n1Total = []
    n1Average = []

    n2 = []
    n2Total = []
    n2Average = []

    occurance = 0
    count = count + 1

## prints out the list generated
print(waveList, n1List, n2List) 
