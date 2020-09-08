## import libraries for specifying the dynamic file path
import os.path

## Open  file target
## specify file name to be used when writing out new data
## imported file titled data
## close the in file
inFile = open(r'C:\Users\JordanWinter\Documents\GitHub\ICTProject\raman_01.txt')
fileName = inFile.name[-12:-4] + "_normalised.txt" 
data = inFile.readlines()
inFile.close
   
## declaration of variables used in the process
waves = [] ## holds wavelength name values
finalWaves = [] ## holds shifted wavelength values

spectra1 = [] ## empty list to hold spectra values
spectra1List = [] ## empty list to hold all average values for spectra 
spectra1Total = 0 ## total of the spectra value - needs to be declared as 0 for the sake of if statement
finalSpectra1 = [] ## holds normalised spectra1 values

spectra2 = [] ## empty list to hold spectra values
spectra2List = [] ## empty list to hold all average values for spectra 
spectra2Total = 0 ## total of the spectra value - needs to be declared as 0 for the sake of if statement
finalSpectra2 = [] ## holds normalised spectra values

spectra3 = [] ## empty list to hold spectra values
spectra3List = [] ## empty list to hold all average values for spectra
spectra3Total = 0 ## total of the spectra value - needs to be declared as 0 for the sake of if statement
finalSpectra3 = [] ## holds normalised spectra values

counter = 0 ## holds value used to determine the number of unique wavelength names
occurance = 0 ## holds value used to determine the number of frames in the file
frames = 0 ## holds value used to store number of frames from the file

## prompt user to enter an offset used to shift the wavelength - warns of the need to be numeric
shiftInput = input("Enter the offset used to shift wavelength. Please note: Needs to be a numeric value. Please enter your selection here: ")
## if the user enters a valid number
## use this entry as a float as the shift offset
if shiftInput.isnumeric():
    shiftInput = float(shiftInput)
## if the user doesnt enter a valid number
## have them re enter the value - warn another error will result in use of default offset of 1
else:
    shiftInput = input("You did not enter a numeric value, another incorrect entry will result in default offset of 1 being used. Please enter a numeric offset to shift wavelength: ")        
    ## if the user enters a valid number
    ## use this entry as a float as the shift offset
    if shiftInput.isnumeric():
        shiftInput = float(shiftInput)
    ## if the user doesnt enter a valid number
    ## used the default offset of 1 as the shift offset
    else:
        shiftInput = float(1) 

## for each line of the imported file
## add the first three characters in the line to waveList and remove duplicate values
for line in data: 
    waves.append(line[:7]) ## need to rever from hardcode
    waveList = list(dict.fromkeys(waves))

## while count is less than the length of the waveList 
## for each line of the imported file
while counter < len(waveList):
    for line in data: 
        ## if first three characters of the line are equal to the referenced wave length name
        ## add that lines spectra values to the relevant list 
        ## increase the occurances of matching lines
        if line[:7]==waveList[counter]:
            spectra1.append(int(line[8:11])) ## need to rever from hardcode
            ## if two spectra values
            if len(line) > 14:
                spectra2.append(int(line[12:15])) ## need to rever from hardcode
            ## if three spectra values
            if len(line) > 18:
                spectra3.append(int(line[16:19])) ## need to rever from hardcode
            occurance = occurance + 1  
    
    ## if there was a match found during the if loop
    ## add together all the values that were found to get the total
    ## find the average value of all instances found and round to 1 decimal point
    ## add the average values to a list with the other average values found
    if occurance > 0:
        spectra1Total=int(sum(spectra1))
        spectra1Average=round(spectra1Total/occurance, 1)
        spectra1List.append(spectra1Average)

        ## if there is a second spectra value found
        if spectra2Total > 0:
            spectra2Total=int(sum(spectra2))
            spectra2Average=round(spectra2Total/occurance, 1)
            spectra2List.append(spectra2Average)

        ## if there is a third spectra value found
        if spectra3Total > 0:
            spectra3Total=int(sum(spectra3))
            spectra3Average=round(spectra3Total/occurance, 1)
            spectra3List.append(spectra3Average)

    ## empty the lists used to hold found values so they can be used for the next value
    spectra1 = []
    spectra2 = []
    spectra3 = []

    ## if frames havent been recorded yet take the occurance value and move to frames
    if frames == 0:
        frames = occurance

    occurance = 0 ## reverts occurance count to zero
    counter = counter + 1 ## increase count to search for next wavelength

## reset count value to 0
## while the counter is less than the length of the waveList
## for each line in the waveList
counter = 0
while counter < len(waveList):
    for line in waveList: 
        ## runs the wavlength through the shift equation using the shift offset provided by user upon load
        ## append rounded, shifted values to a final wave list
        ## increase count by 1 to end while loop at end of list
        shiftedWave = ((1 / shiftInput) - (1 / float(line))) * 10**7
        shiftedWave = round(shiftedWave,2)
        finalWaves.append(shiftedWave)
        counter = counter + 1

## reset count value to 0
## while the counter is less than the length of spectra1List - if empty is 0 and = counter
## for each line in spectra1List
## check the value provided is greater than 0
counter = 0
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
## while the counter is less than the length of spectra2List - if empty is 0 and = counter
## for each line in spectra2List
## check the value provided is greater than 0
counter = 0
while counter < len(spectra2List):
    for line in spectra2List: 
        ## run the spectraList1 values through the normalisation formula
        ## append the normalised spectra value to a finalSpectra1 value list
        ## increase the counter by 1 to move to the next value in spectra1List
        normalisedSpectra = (1 / frames * (spectra2List[counter]))
        finalSpectra2.append(normalisedSpectra)
        counter = counter + 1

## reset count value to 0
## while the counter is less than the length of spectra3List - if empty is 0 and = counter
## for each line in spectra3List
## check the value provided is greater than 0
counter = 0
while counter < len(spectra3List):
    for line in spectra3List: 
        ## run the spectraList3 values through the normalisation formula
        ## append the normalised spectra value to a finalSpectra3 value list
        ## increase the counter by 1 to move to the next value in spectra3List
        normalisedSpectra = (1 / frames * (spectra3List[counter]))
        finalSpectra3.append(normalisedSpectra)
        counter = counter + 1        

## save location (plot folder) specified and added to the file name on hand
## create new txt file with filename with _condensed added to end at the file path
## if the final lists hold data
## for each line in finalWaves and finalSpectra1
## write wave length name followed by a "," followed by the spectra value to each line 
savePath = (r'C:\Users\JordanWinter\Documents\GitHub\ICTProject')
saveName = os.path.join(savePath,fileName)
outFile = open(saveName, "w")
## if one spectra value
if finalSpectra1 != [] and finalSpectra2 == []:
    for (waveData,spectra1Data) in zip(finalWaves,finalSpectra1):
        outFile.write(str(waveData))
        outFile.write(",")
        outFile.write(str(spectra1Data))
        outFile.write("\n")
## if two spectra values
if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 == []:
    for (waveData,spectra1Data,spectra2Data) in zip(finalWaves,finalSpectra1,finalSpectra2):
        outFile.write(str(waveData))
        outFile.write(",")
        outFile.write(str(spectra1Data))
        outFile.write(",")
        outFile.write(str(spectra2Data))
        outFile.write("\n") 
## if three spectra values
if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 != []:
    for (waveData,spectra1Data,spectra2Data,spectra3Data) in zip(finalWaves,finalSpectra1,finalSpectra2,finalSpectra3):
        outFile.write(str(waveData))
        outFile.write(",")
        outFile.write(str(spectra1Data))
        outFile.write(",")
        outFile.write(str(spectra2Data))
        outFile.write(",")
        outFile.write(str(spectra3Data))
        outFile.write("\n")          
## if the final lists dont contain data, print out error message - cannot contain a ","
if waveData == []:
    outFile.write("Data is corrupt. Please contact technical support.")
##close the outfile
outFile.close
