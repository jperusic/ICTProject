## Open raman file target
infile = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")

## declaration of variables used in the process
waves = [] ## holds wavelength name values
spectra1 = [] ## empty list to hold spectra 1 values
spectra2 = [] ## empty list to hold spectra 2 values
spectra1List = [] ## empty list to hold all average values for spectra 1
spectra2List = [] ## empty list to hold all average values for spectra 2
finalWaves = [] ## holds shifted wavelength values
finalSpectra1 = [] ## holds normalised spectra1 values
finalSpectra2 = [] ## holds normalised spectra2 values
counter = 0 ## holds value used to determine the number of unique wavelength names
occurance = 0 ## holds value used to determine the number of frames in the file
frames = 0 ## holds value used to store number of frames from the file

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
        ## add that lines spectra values to the relevant list 
        ## increase the occurances of matching lines
        if line[:7]==waveList[counter]:
            spectra1.append(int(line[8:11]))
            #spectra2.append(int(line[8:11]))
            occurance = occurance + 1  
    
    ## if there was a match found during the if loop
    ## add together all the values that were found to get the total
    ## find the average value of all instances found and round to 1 decimal point
    ## add the average values to a list with the other average values found
    if occurance > 0:
        spectra1Total=int(sum(spectra1))
        spectra1Average=round(spectra1Total/occurance, 1)
        spectra1List.append(spectra1Average)

        ## spectra2Total=int(sum(spectra2))
        ## spectra2Average=round(spectra2Total/occurance, 1)
        ## spectra2List.append(spectra2Average)

    ## empty the list used to hold found values so they can be used for the next unique wavelength
    spectra1 = []
    spectra1Total = []
    spectra1Average = []

    # spectra2 = []
    # spectra2Total = []
    # spectra2Average = []

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
            shiftedWave = ((1 / waveSection1) - (1 / waveSection2)) * 10**7
            shiftedWave = round(shiftedWave)
            finalWaves.append(shiftedWave)
            counter = counter + 1


## reset count value to 0
counter = 0

## while the counter is less than the length of spectra1List
## for each line in spectra1List
## check the value provided is greater than 0
while counter < len(spectra1List):
    for line in spectra1List: 
        if spectra1List[counter] > 0:
        ## run the spectraList1 values through the normalisation formula
        ## append the rounded and normalised spectra value to a finalSpectra1 list
        ## increase the counter by 1 to move to the next value in spectra1List
            normalisedSpectra = (1 / frames * (spectra1List[counter]))
            normalisedSpectra = round(normalisedSpectra,1)
            finalSpectra1.append(normalisedSpectra)
            counter = counter + 1

## reset count value to 0
# counter = 0

## while the counter is less than the length of spectra2List
## for each line in spectra2List
## check the value provided is greater than 0
# while counter < len(spectra2List):
    # for line in spectra2List: 

        ## run the spectraList1 values through the normalisation formula
        ## append the normalised spectra value to a finalSpectra1 value list
        ## increase the counter by 1 to move to the next value in spectra1List
        # normalisedSpectra = (1 / frames * (spectra2List[counter]))
        # finalSpectra2.append(normalisedSpectra)
        # counter = counter + 1

## prints out the list generated - To test
print(finalSpectra1)


