raman1 = open("//Users/JarradPerusic/Desktop/data/raman_01.txt", "r")
raman2 = open("//Users/JarradPerusic/Desktop/data/raman_02.txt", "r")
raman3 = open("//Users/JarradPerusic/Desktop/data/raman_03.txt", "r")
raman4 = open("//Users/JarradPerusic/Desktop/data/raman_04.txt", "r")

#print(raman1.read())

count = 0
for item in raman1:
    wave = int(raman1.read(3))
    if wave=="515":
        count=count+1


print(count)



