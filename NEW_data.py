# coding: utf-8

import os.path


def process(fp, shiftInput: (int, float) = 1) -> list:
    """
    :param fp: abs path of the data file
    :param shiftInput: shift value, accept float/int
    :return: list of normalised data
    """

    # todo: please paste your code here
    # ===========================================
    # the following code as an example
    # do not hesitate to delete these and replace them with yours.


    results = []
    ## Open  file target
    ## specify file name to be used when writing out new data
    ## imported file titled data
    ## close the in file
    inFile = open(fp, "r")
    data = inFile.readlines()
    inFile.close()

    ## Declaration of variables used in the process
    waves = [] ## Holds the wavelength name values
    finalWaves = [] ## Holds shifted wavelength name values

    spectra1 = [] ## Empty list to hold spectra values
    spectra1List = [] ## Empty list to hold all average values for spectra 
    spectra1Total = 0 ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra1 = [] ## Holds normalised spectra1 values

    spectra2 = [] ## Empty list to hold spectra values
    spectra2List = [] ## Empty list to hold all average values for spectra 
    spectra2Total = 0 ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra2 = [] ## Holds normalised spectra values

    spectra3 = [] ## Empty list to hold spectra values
    spectra3List = [] ## Empty list to hold all average values for spectra
    spectra3Total = 0 ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra3 = [] ## Holds normalised spectra values

    counter = 0 ## Holds value used to determine the number of unique wavelength names
    occurance = 0 ## Holds value used to determine the number of frames in the file
    frames = 0 ## Holds value used to store number of frames from the file

    ## prompt user to enter an offset used to shift the wavelength - warns of the need to be numeric
    # shiftInput = input(
    #     "Enter the offset used to shift wavelength. Please note: Needs to be a numeric value. Please enter your selection here: ")
    ## if the user enters a valid number
    ## use this entry as a float as the shift offset
    # if shiftInput.isnumeric():
    #     shiftInput = float(shiftInput)
    # ## if the user doesnt enter a valid number
    # ## have them re enter the value - warn another error will result in use of default offset of 1
    # else:
    #     shiftInput = input(
    #         "You did not enter a numeric value, another incorrect entry will result in default offset of 1 being used. Please enter a numeric offset to shift wavelength: ")
    #     ## if the user enters a valid number
    #     ## use this entry as a float as the shift offset
    #     if shiftInput.isnumeric():
    #         shiftInput = float(shiftInput)
    #     ## if the user doesnt enter a valid number
    #     ## used the default offset of 1 as the shift offset
    #     else:
    #         shiftInput = float(1)

    ## For each line of the imported file
    ## Split line into wavelength, spectra values
    ## Take the wavelengths and place them in a new waves list
    ## Add the waves list items to a waveList and remove duplicate values
    while counter < len(data):
        for line in data: 
            thisLine = data[counter].split()
            waves.append(thisLine[0])
            waveList = list(dict.fromkeys(waves))
            counter = counter + 1

    ## For each line of the imported file
    ## Split line into wavelength, spectra values
    ## Take found spectra values and categorize into seperate lists (Supports up to 3 spectra values)
    counter=0
    while counter < len(waveList):
        for line in data: 
            thisLine = data[counter].split()
            if thisLine[0]==waveList[counter]:
                spectra1.append(int(thisLine[1])) 
                ## if 2 spectra values found
                if len(thisLine) > 2:
                    spectra2.append(int(thisLine[2])) 
                ## if 3 spectra values found
                if len(thisLine) > 3:
                    spectra2.append(int(thisLine[3]))  
                occurance = occurance + 1 

        ## If there was a match found during the if loop
        ## Add together all the values that were found to get the total
        ## Find the average value of all instances found and round to 1 decimal point
        ## Add the average values to a list with the other average values found
        if occurance > 0:
            spectra1Total=int(sum(spectra1))
            spectra1Average=round(spectra1Total/occurance, 1)
            spectra1List.append(spectra1Average)

            ## If there is a second spectra value found
            if spectra2Total > 0:
                spectra2Total=int(sum(spectra2))
                spectra2Average=round(spectra2Total/occurance, 1)
                spectra2List.append(spectra2Average)

            ## If there is a third spectra value found
            if spectra3Total > 0:
                spectra3Total=int(sum(spectra3))
                spectra3Average=round(spectra3Total/occurance, 1)
                spectra3List.append(spectra3Average)

        ## Empty the lists used to hold found values so they can be used for the next value
        spectra1 = []
        spectra2 = []
        spectra3 = []

        ## If the frames haven't been recorded yet, take the occurance value and move to frames
        if frames == 0:
            frames = occurance

        occurance = 0 ## Reverts occurance count to zero
        counter = counter + 1 ## Increase counter by one to search for the next wavelength

    ## Reset the counter value to 0
    ## While the counter is less than the length of the waveList
    ## For each line in the waveList
    counter = 0
    while counter < len(waveList):
        for line in waveList: 
            ## Runs the wavelength through the shift equation using the shift offset provided by user upon input
            ## Append the rounded value, shifted values to a final wave list
            ## Increase the counter by 1 to end the while loop at end of the list
            shiftedWave = ((1 / shiftInput) - (1 / float(line))) * 10**7
            shiftedWave = round(shiftedWave,2)
            finalWaves.append(shiftedWave)
            counter = counter + 1

        
    ## Reset the counter value to 0
    ## While the counter is less than the length of spectra1List - if empty is 0 and = counter
    ## For each line in spectra1List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra1List):
        for line in spectra1List: 
            if spectra1List[counter] > 0:
                ## Run the spectraList1 values through the normalisation formula
                ## Append the rounded and normalised spectra value to a finalSpectra1 list
                ## Increase the counter by 1 to move to the next value in spectra1List
                normalisedSpectra = round(spectra1List[counter],1)
                finalSpectra1.append(normalisedSpectra)
                counter = counter + 1

    ## Reset count value to 0
    ## While the counter is less than the length of spectra2List - if empty is 0 and = counter
    ## For each line in spectra2List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra2List):
        for line in spectra2List: 
            ## Run the spectraList1 values through the normalisation formula
            ## Append the normalised spectra value to a finalSpectra1 value list
            ## Increase the counter by 1 to move to the next value in spectra1List
            normalisedSpectra = round(spectra2List[counter],1)
            finalSpectra2.append(normalisedSpectra)
            counter = counter + 1

    ## Reset counter value to 0
    ## While the counter is less than the length of spectra3List - if empty is 0 and = counter
    ## For each line in spectra3List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra3List):
        for line in spectra3List: 
            ## Run the spectraList3 values through the normalisation formula
            ## Append the normalised spectra value to a finalSpectra3 value list
            ## Increase the counter by 1 to move to the next value in spectra3List
            normalisedSpectra = round(spectra3List[counter],1)
            finalSpectra3.append(normalisedSpectra)
            counter = counter + 1    

    # ------------------------------------------------- #
    if finalSpectra1 != [] and finalSpectra2 == []:
        for (waveData, spectra1Data) in zip(finalWaves, finalSpectra1):
            results.append([waveData, spectra1Data])
    # if two spectra values
    if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 == []:
        for (waveData, spectra1Data, spectra2Data) in zip(finalWaves, finalSpectra1, finalSpectra2):
            results.append([waveData, spectra1Data, spectra2Data])

    # if the final lists dont contain data, print out error message - cannot contain a ","
    if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 != []:
        for (waveData, spectra1Data, spectra2Data, spectra3Data) in zip(finalWaves, finalSpectra1, finalSpectra2,
                                                                        finalSpectra3):
            results.append([waveData, spectra1Data, spectra2Data, spectra3Data])

    return results


def export_data(data: list, output_path: str):
    """
    save normalised data to a file
    :param data: normalised data
    :param output_path: abs path of output file
    :return:
    """

    # todo: please paste your code here
    # ===========================================
    # the following code as an example
    # do not hesitate to delete these and replace them with yours.


    with open(output_path, 'w', encoding='utf-8') as f:
        for line in data:
            line = [str(i) for i in line]
            f.write('{}\n'.format(','.join(line)))


if __name__ == '__main__':
    fp = 'data/raman_01.txt'
    r = process(fp, 100.0)
    print(r)
