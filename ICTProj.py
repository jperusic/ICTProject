infile = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")

waves = []
count = 0
n1 = []
n2 = []
n1Total = 0
n1Average=0
n1List = []
n2Total = 0
n2Average=0
n2List = []
occurance = 0

data = infile.readlines()

for line in data: 
    
    waves.append(line[:3])
    waveList = list(dict.fromkeys(waves))

while count < len(waveList):
    
    for line in data: 
        
        if line[:3]==waveList[count]:
            n1.append(int(line[4:7]))
            n2.append(int(line[8:11]))
            occurance = occurance + 1  
    
    if occurance > 0:

        n1Total=int(sum(n1))
        n1Average=round(n1Total/occurance, 1)
        n1List.append(n1Average)

        n2Total=int(sum(n2))
        n2Average=round(n2Total/occurance, 1)
        n2List.append(n2Average)

    n1 = []
    n1Total = []
    n1Average = []

    n2 = []
    n2Total = []
    n2Average = []

    occurance = 0
    count = count + 1

print(waveList, n1List, n2List) 
