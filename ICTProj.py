infile = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")
raman2 = open("//Users/JarradPerusic/Desktop/data/raman_02.txt", "r")
raman3 = open("//Users/JarradPerusic/Desktop/data/raman_03.txt", "r")
raman4 = open("//Users/JarradPerusic/Desktop/data/raman_04.txt", "r")

waves = [" "]

data = infile.readlines()

for line in data:

    waves.append(line[:3])
    waves = list(dict.fromkeys(waves))
    waves = sorted(waves)


print(waves)  

