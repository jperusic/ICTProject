# coding: utf-8

import os.path


def process(fp, shiftInput: (int, float) = 1) -> list:
    """
    :param fp: abs path of the data file
    :param shiftInput: shift value, accept float/int
    :return: list of normalised data
    """

    results = []  ## holds function result
    inFile = open(fp, "r")  ## open file target
    data = [line for line in inFile.readlines() if
            line.strip()]  ## imported file titled data and stripped of blank lines
    inFile.close()  ## close the in file

    ## Declaration of variables used in the process
    waves = []  ## Holds the wavelength name values
    waveList = []  ## Holds the values of waves with duplicate values removed
    finalWaves = []  ## Holds shifted wavelength name values

    spectra1 = []  ## Empty list to hold spectra values
    spectra1List = []  ## Empty list to hold all average values for spectra
    spectra1Total = 0  ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra1 = []  ## Holds normalised spectra1 values

    spectra2 = []  ## Empty list to hold spectra values
    spectra2List = []  ## Empty list to hold all average values for spectra
    spectra2Total = 0  ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra2 = []  ## Holds normalised spectra values

    spectra3 = []  ## Empty list to hold spectra values
    spectra3List = []  ## Empty list to hold all average values for spectra
    spectra3Total = 0  ## Total of the spectra value - needs to be declared as 0 for the sake of if statement
    finalSpectra3 = []  ## Holds normalised spectra values

    counter = 0  ## Holds value used to determine the number of unique wavelength names
    occurance = 0  ## Holds value used to determine the number of frames in the file
    frames = 0  ## Holds value used to store number of frames from the file

    ## ** DEBUGGING TOOLS **
    debug = 0
    totalToBug = (len(data))

    ## For each line of the imported file that dont begin with F (to remove Frame rows)
    ## Split line to identify wavelength (first value in row) add to a waveList and remove duplicate values
    while counter < len(data):
        for line in data:
            if not line.startswith("F"):
                thisLine = line.split()
                waves.append(thisLine[0])
                waveList = list(dict.fromkeys(waves))
                ## ** DEBUG TOOLS **
            ## print system progress to user in percent via terminal
            debug = debug + 1
            print("PROCESS 1 / 4: ", round((debug / totalToBug) * 100), "% ", debug, "/", totalToBug)
            counter = counter + 1  ## increase count by 1 to move to next row

    ## ** RESET DEBUG TOOLS **
    debug = 0
    totalToBug = (len(waveList))

    ## For each line of the imported file split line into wavelength, spectra values
    ## Compare the current row wave to the waveList wave to allocate spectra
    ## Take found spectra values and categorize into seperate lists (Supports up to 3 spectra values)
    counter = 0
    while counter < len(waveList):
        for line in data:
            thisLine = line.split()
            if thisLine[0] == waveList[counter]:
                spectra1.append(int(thisLine[1]))
                ## if 2 spectra values found
                if len(thisLine) > 2:
                    spectra2.append(int(thisLine[2]))
                    ## if 3 spectra values found
                if len(thisLine) > 3:
                    spectra2.append(int(thisLine[3]))
                occurance = occurance + 1  ## increase occurance count by 1

        ## If there was a match found during the if loop
        ## Add together all the values that were found to get the total
        ## Find the average value of all instances found and round to 1 decimal point
        ## Add the average values to a list with the other average values found
        if occurance > 0:
            spectra1Total = int(sum(spectra1))
            spectra1Average = round(spectra1Total / occurance, 1)
            spectra1List.append(spectra1Average)

            ## If there is a second spectra value found
            if spectra2Total > 0:
                spectra2Total = int(sum(spectra2))
                spectra2Average = round(spectra2Total / occurance, 1)
                spectra2List.append(spectra2Average)

            ## If there is a third spectra value found
            if spectra3Total > 0:
                spectra3Total = int(sum(spectra3))
                spectra3Average = round(spectra3Total / occurance, 1)
                spectra3List.append(spectra3Average)

        ## Empty the lists used to hold found values so they can be used for the next value
        spectra1 = []
        spectra2 = []
        spectra3 = []

        ## If the frames haven't been recorded yet, take the occurance value and move to frames
        if frames == 0:
            frames = occurance
        occurance = 0  ## Reverts occurance count to zero

        ## ** DEBUG TOOLS **
        ## print system progress to user in percent via terminal
        debug = debug + 1
        print("PROCESS 2 / 4: ", round((debug / totalToBug) * 100), "% ", debug, "/", totalToBug)

        counter = counter + 1  ## Increase counter by one to search for the next wavelength

    ## ** RESET DEBUG TOOLS **
    debug = 0
    totalToBug = (len(waveList))

    ## While the counter is less than the length of the waveList go through the rows in waveList
    counter = 0
    while counter < len(waveList):
        for line in waveList:
            ## Runs the wavelength through the shift equation using the shift offset provided by user upon input
            ## Append the rounded value, shifted values to a final wave list
            shiftedWave = ((1 / shiftInput) - (1 / float(line))) * 10 ** 7
            shiftedWave = round(shiftedWave, 2)
            finalWaves.append(shiftedWave)

            ## ** DEBUG TOOLS **
            ## print system progress to user in percent via terminal
            debug = debug + 1
            print("PROCESS 3 / 4: ", round((debug / totalToBug) * 100), "% ", debug, "/", totalToBug)

            counter = counter + 1  ## Increase counter by one to search for the next wavelength

    ## ** RESET DEBUG TOOLS **
    debug = 0
    totalToBug = (len(waveList))

    ## Reset the counter value to 0
    ## While the counter is less than the length of spectra1List - if empty is 0 and = counter
    ## For each line in spectra1List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra1List):
        for line in spectra1List:
            if spectra1List[counter] > 0:
                ## Append the rounded and normalised spectra value to a finalSpectra1 list
                normalisedSpectra = round(spectra1List[counter], 1)
                finalSpectra1.append(normalisedSpectra)

                ## ** DEBUG TOOLS **
                ## print system progress to user in percent via terminal
                debug = debug + 1
                print("PROCESS 4 / 4: ", round((debug / totalToBug) * 100), "% ", debug, "/", totalToBug)

                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## ** RESET DEBUG TOOLS **
    debug = 0
    totalToBug = (len(waveList))

    ## While the counter is less than the length of spectra2List - if empty is 0 and = counter
    ## For each line in spectra2List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra2List):
        for line in spectra2List:
            if spectra2List[counter] > 0:
                ## Append the normalised spectra value to a finalSpectra1 value list
                normalisedSpectra = round(spectra2List[counter], 1)
                finalSpectra2.append(normalisedSpectra)

                ## ** DEBUG TOOLS **
                ## print system progress to user in percent via terminal
                debug = debug + 1
                print("PROCESSING EXTRA SPECTRA: ", round((debug / totalToBug) * 100, 1), "% ", debug, "/", totalToBug)

                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## ** RESET DEBUG TOOLS **
    debug = 0
    totalToBug = (len(waveList))

    ## While the counter is less than the length of spectra3List - if empty is 0 and = counter
    ## For each line in spectra3List
    ## Check the value provided is greater than 0
    counter = 0
    while counter < len(spectra3List):
        for line in spectra3List:
            if spectra3List[counter] > 0:
                ## Append the normalised spectra value to a finalSpectra3 value list
                normalisedSpectra = round(spectra3List[counter], 1)
                finalSpectra3.append(normalisedSpectra)

                ## ** DEBUG TOOLS **
                ## print system progress to user in percent via terminal
                debug = debug + 1
                print("PROCESSING EXTRA SPECTRA: ", round((debug / totalToBug) * 100, 1), "% ", debug, "/", totalToBug)

                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## ** DEBUG TOOLS **
    ## print system status to user via terminal
    print("MAPPING DATA")

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

    with open(output_path, 'w', encoding='utf-8') as f:
        for line in data:
            line = [str(i) for i in line]
            f.write('{}\n'.format(','.join(line)))


def read_normalised_data(fp):
    """read data from a normalised file"""
    data = []  # create an empty container
    with open(fp, 'r', encoding='utf-8') as f:  # open a file handle using "with"
        for line in f:  # each line/row
            if not line:
                continue
            _ = line.split(',')
            if not _:
                continue
            _ = [float(i) for i in _]
            data.append(_)
    return data


def display_specs():
    """function to pull labbook details for current raman file"""

    ## NEED TO PASS FROM FP - NEEDS TO BE FOR THE FILE WHICH IS DISPLAYED CURRENTLY ON TYHE NORMALISED TAB
    dataFile = open("C:/Users/End User/iCloudDrive/Desktop/ICTCode/data/raman_12.txt", "r")
    thisFile = dataFile.name

    ## NEED TO HAVE LIUYU CREATE NEW IMPORT SECTION FOR THIS FILE IMPORT - LABBOOK WITH READING SPECS
    inFile = open("C:/Users/End User/iCloudDrive/Desktop/ICTCode/data/labbook-2018-10-30.txt", "r")
    labbook = [line for line in inFile.readlines() if line.strip()]
    inFile.close()

    ## declare variables for function to allow for loop entry
    fileSpecs = []
    name = 'null'
    counter = 0

    ## while counter less than the number of lines in the labbook go through the lines in labbook
    ## if the line is deemed a reading entry, split the data at the spaces, strip the punctuation.
    ## check the first value from the split and check if it matched the inFile name, if a match allocate data to individual variables
    while counter < len(labbook):
        for line in labbook:
            if len(line) > 25:
                thisLine = line.split()
                name = thisLine[0]
                name = name[:-1]
                if name in thisFile:
                    fileSpecName = 'File: ' + name
                    time = thisLine[1]
                    fileSpecTime = 'Time: ' + time[:-1]
                    P = thisLine[2]
                    fileSpecP = 'P: ' + P[2:-1]
                    E = thisLine[5] + thisLine[6]
                    fileSpecE = 'E: ' + E[:-1]
                    g = thisLine[7]
                    fileSpecG = 'g: ' + g[:-1]
                    c = thisLine[8]
                    fileSpecC = 'c: ' + c[2:-1]
                    temp = thisLine[9]
                    fileSpecTemp = 'Temp: ' + temp
            counter = counter + 1  ## increase count by 1 to move to next line

    ## check if a match was found between the inFile and the labbook
    ## if yes, update the name to matching format and assign the data from the matched row as the return data
    if name != 'null':
        fileSpecName = fileSpecName
        fileSpecs.append(fileSpecName)
        fileSpecs.append(fileSpecTime)
        fileSpecs.append(fileSpecP)
        fileSpecs.append(fileSpecE)
        fileSpecs.append(fileSpecG)
        fileSpecs.append(fileSpecC)
        fileSpecs.append(fileSpecTemp)
    ## if no, provide message to inform user
    else:
        fileSpecName = ' No File Specs Found'
        fileSpecs.append(fileSpecName)

    ## close the data file and return the results
    dataFile.close()
    return fileSpecs


def parse_lab_book(fp):
    data = {}
    # todo: parse lab book data
    with open(fp, 'r', encoding='ISO-8859-1') as f:  # This File encoded not in utf-8
        for line in f:
            if line.count(',') != 5:
                continue
            _, p, e, g, c, temp = line.split(',')
            name, time = _.split(':')
            name = name.strip()
            time = time.strip()
            _, p = p.split('=')
            _, e = e.split('=')
            _, c = c.split('=')
            data[name] = {
                'name': name,
                'time': time,
                'p': p.strip(),
                'e': e.strip(),
                'g': g.strip(),
                'c': c.strip(),
                'temp': temp.strip(),
            }
    return data


if __name__ == '__main__':
    fp = 'data/raman_01.txt'
    r = process(fp, 100.0)
    print(r)
