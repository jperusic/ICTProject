# coding: utf-8
import os.path

def process(fp, shiftInput: (int, float) = 1) -> list:
    """
    :param fp: abs path of the data file
    :param shiftInput: shift value, accept float/int
    :return: list of normalised data
    """
    results = []  ## holds function: process result
    inFile = open(fp, "r")  ## open file target (file to be normalised)
    data = [line for line in inFile.readlines() if line.strip()]  ## imported file data and stripped of blank lines
    inFile.close()  ## close the file

    ## Declaration of variables used in function: process
    waveList = []  ## List to hold all wavelength values found in the file (no duplicates in list)
    finalWaves = []  ## List to hold the shifted wavelength values to be plotted

    ## Variables used for the first set of speactra results per wavelength
    spectra1 = []  ## Holds all first set spectra values found in the target file
    spectra1List = []  ## Holds all average values for first set spectra values which are ready to be normalised
    finalSpectra1 = []  ## Holds all first set normalised spectra values which will be displayed as dataset and on plot

    ## Variables used for the second set of speactra results per wavelength (only used if a second spectra set is present)
    spectra2 = []  ## Holds all second set spectra values found in the target file
    spectra2List = []  ## Holds all average values for second set spectra values which are ready to be normalised
    finalSpectra2 = []  ## Holds all second set normalised spectra values which will be displayed as dataset and on plot

    ## Variables used for the third set of speactra results per wavelength (only used if a third spectra set is present)
    spectra3 = []  ## Holds all third set spectra values found in the target file
    spectra3List = []  ## Holds all average values for third set spectra values which are ready to be normalised
    finalSpectra3 = []  ## Holds all third set normalised spectra values which will be displayed as dataset and on plot

    counter = 0  ## Holds value used to determine the number of unique wavelength names
    occurance = 0  ## Holds value used to determine the number of frames in the file

    ## Loop to gather list of unique wavelength values found in the data file
    ## For each line of the imported file that doesnt begin with F (to remove Frame rows)
    ## Split line to identify wavelength (first value in row) add to a waveList if not already present
    while counter < len(data):
        for line in data:
            if not line.startswith("F"):
                thisLine = line.split()
                if thisLine[0] not in waveList:
                    waveList.append(thisLine[0])
            counter = counter + 1  ## increase count by 1 to move to next row

    ## For each line of the imported file split line into wavelength, spectra value(s)
    ## Compare the current row wave to the waveList wave - allocate spectra if there is a match (finds all spectra values for each wavelength)
    ## Take found spectra values and categorize into seperate lists (Supports up to 3 spectra values - list only created if values present)
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
                        spectra3.append(int(thisLine[3]))
                occurance = occurance + 1  ## increase occurance count by 1

        ## If there were spectra values found for the wavelength being analysed, add together all spectra values found to get a total
        ## Find the average value of the identified spectra values by dividing the sum and instances found - result rounded to 1 decimal point
        ## Add the average values to a list with the other average values found - these values are ready for normalisation 
        if occurance > 0:
            spectra1Total = int(sum(spectra1))
            spectra1Average = round(spectra1Total / occurance, 1)
            spectra1List.append(spectra1Average)
            ## If there is a second spectra data set found in the list complete same process for spectra2
            if spectra2 != []:
                spectra2Total = int(sum(spectra2))
                spectra2Average = round(spectra2Total / occurance, 1)
                spectra2List.append(spectra2Average)
                ## If there is a third spectra data set found in the list complete same process for spectra2
                if spectra3 != []:
                    spectra3Total = int(sum(spectra3))
                    spectra3Average = round(spectra3Total / occurance, 1)
                    spectra3List.append(spectra3Average)

        ## Empty the lists used to hold identified spectra values so they can be used for the next value
        spectra1 = []
        spectra2 = []
        spectra3 = []

        occurance = 0  ## Reverts occurance count to zero
        counter = counter + 1  ## Increase counter by one to search for the next wavelength

    ## While the counter is less than the length of the waveList go through the rows in waveList
    counter = 0
    while counter < len(waveList):
        for line in waveList:
            ## Runs the wavelength through the shift equation using the shift offset provided by user upon input
            ## Append the rounded value, shifted values to a final wave list - these waves will be used to plot dataset
            shiftedWave = ((1 / shiftInput) - (1 / float(line))) * 10 ** 7
            shiftedWave = round(shiftedWave, 2)
            finalWaves.append(shiftedWave)
            counter = counter + 1  ## Increase counter by one to search for the next wavelength

    ## Reset the counter value to 0
    ## While the counter is less than the length of spectra1List (if list is empty will be 0 and = counter - skipped if empty)
    ## For each line in spectra1List check the value provided is greater than 0
    ## Append the rounded and normalised spectra value to a finalSpectra1 list - values will be used to plot dataset
    counter = 0
    while counter < len(spectra1List):
        for line in spectra1List:
            if spectra1List[counter] > 0:
                normalisedSpectra = round(spectra1List[counter], 1)
                finalSpectra1.append(normalisedSpectra)
                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## Reset the counter value to 0
    ## While the counter is less than the length of spectra2List (if list is empty will be 0 and = counter - skipped if empty)
    ## For each line in spectra2List check the value provided is greater than 0
    ## Append the rounded and normalised spectra value to a finalSpectra2 list - values will be used to plot dataset
    counter = 0
    while counter < len(spectra2List):
        for line in spectra2List:
            if spectra2List[counter] > 0:
                normalisedSpectra = round(spectra2List[counter], 1)
                finalSpectra2.append(normalisedSpectra)
                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## Reset the counter value to 0
    ## While the counter is less than the length of spectra3List (if list is empty will be 0 and = counter - skipped if empty)
    ## For each line in spectra3List check the value provided is greater than 0
    ## Append the rounded and normalised spectra value to a finalSpectra3 list - values will be used to plot dataset
    counter = 0
    while counter < len(spectra3List):
        for line in spectra3List:
            if spectra3List[counter] > 0:
                normalisedSpectra = round(spectra3List[counter], 1)
                finalSpectra3.append(normalisedSpectra)
                counter = counter + 1  ## Increase the counter by 1 to move to the next spectra value

    ## Append the shifted / normalised data to the function results - no. of spectra values vary. However, wavelengths will always be appended
    ## If there were only a single set of spectra values found in the process, append the single dataset to the function results alongside the wavelengths
    if finalSpectra1 != [] and finalSpectra2 == []:
        for (waveData, spectra1Data) in zip(finalWaves, finalSpectra1):
            results.append([waveData, spectra1Data])

    ## If there were two sets of spectra values found in the process, append the two datasets to the function results alongside the wavelengths
    if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 == []:
        for (waveData, spectra1Data, spectra2Data) in zip(finalWaves, finalSpectra1, finalSpectra2):
            results.append([waveData, spectra1Data, spectra2Data])

    ## If there were three sets of spectra values found in the process, append the three datasets to the function results alongside the wavelengths
    if finalSpectra1 != [] and finalSpectra2 != [] and finalSpectra3 != []:
        for (waveData, spectra1Data, spectra2Data, spectra3Data) in zip(finalWaves, finalSpectra1, finalSpectra2, finalSpectra3):
            results.append([waveData, spectra1Data, spectra2Data, spectra3Data])

    return results

## Function to export the shifted / normalsied data to a new file and avoid alteration of the original file
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

## Function to read normalised data directly from a normalised file - allows for already normalised files to be supported and displayed within the system
def read_normalised_data(fp):
    """read data from a normalised file"""
    data = []
    with open(fp, 'r', encoding='utf-8') as f:
        for line in f:
            if not line:
                continue
            _ = line.split(',')
            if not _:
                continue
            _ = [float(i) for i in _]
            data.append(_)
    return data

## Function to get the reading specs for the file being analysed so it can be displayed in the spec list when the file is selected.
## Requires the importation of a labbook to compare if filename exists in the labbook, no results displayed if no match in labbook  - evolution of display_specs()
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
    import timeit
    fp = 'data/raman_01.txt'
    r = process(fp, 100.0)
    print(r)
    print(timeit.timeit(process, number=100000))



