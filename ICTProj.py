## Open raman file target
infile = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")

## declaration of variables used in the process
waves = [] ## holds wavelength name values
counter = 0 ## holds value used to determine the number of unique wavelength names
n1 = [] ## empty list to hold spectra 1 values
n2 = [] ## empty list to hold spectra 2 values
n1Total = 0 ## holds the sum of values in n1 list
n1Average=0 ## holds average for values in n1 list
n1List = [] ## empty list to hold all average values for spectra 1
n2Total = 0 ## holds the sum of values in n2 list
n2Average=0 ## holds average for values in n2 list
n2List = [] ## empty list to hold all average values for spectra 2
occurance = 0 ## holds value used to determine the number of frames in the file
frames = 0 ## holds value used to store number of frames from the file
finalWaves = [] ## holds shifted wavelength values
waveSection1 = 0 ## holds first section of wavelength for shift
waveSection2= 0 ## holds second section of wavelength for shift


## imported file titled data
data = infile.readlines()

## for each line of the imported file
for line in data: 
    
    ## add the first three characters in the line to waveList and remove duplicate values
    waves.append(line[:7])
    waveList = list(dict.fromkeys(waves))

## while count is less than the length of the waveList 
while counter < len(waveList):
    
    ## for each line of the imported file
    for line in data: 
        
        ## if first three characters of the line are equal to the referenced wave length name
        
        if line[:7]==waveList[counter]:
            ## add that lines spectra values to the relevant list and increase the occurances of matching lines
            n1.append(int(line[8:11]))
            ##n2.append(int(line[8:11]))
            occurance = occurance + 1  
    
    ## if there was a match found during the if loop
    if occurance > 0:

        ## add together all the values that were found to get the total
        ## find the average value of all instances found and round to 1 decimal point
        ## add the average values to a list with the other average values found
        n1Total=int(sum(n1))
        n1Average=round(n1Total/occurance, 1)
        n1List.append(n1Average)

        ## n2Total=int(sum(n2))
        ## n2Average=round(n2Total/occurance, 1)
        ## n2List.append(n2Average)

    ## empty the list used to hold found values so they can be used for the next unique wavelength
    n1 = []
    n1Total = []
    n1Average = []

    ## n2 = []
    ## n2Total = []
    ## n2Average = []

    ## if frames havent been recorded yet take the occurance value and move to frames
    if frames == 0:
        frames = occurance

    occurance = 0 ## reverts occurance count to zero
    counter = counter + 1 ## increase count to search for next wavelength


## reset count value to 0
counter = 0

## while the counter is less than the length of the waveList
## for each line in the waveList
## define first/second part of wavelength to perform shift
while counter < len(waveList):
    for line in waveList: 
        waveSection1 = int(line[:3])
        waveSection2 = int(line[4:7])

        ## check the values provided are both greater than 0
        ## runs the sections through the shift equation provided
        ## append shifted values to a final wave list
        ## increase count by 1 to end while loop at end of list
        if waveSection1 > 0 and waveSection2 > 0:
            normalisedWaves = ((1 / waveSection1) - (1 / waveSection2)) * 10**7
            finalWaves.append(normalisedWaves)
            counter = counter + 1

## prints out the list generated - To test
print(waveList, n1List) 
print(finalWaves)
print(waveSection1, waveSection2)
