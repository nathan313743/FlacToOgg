import os

foundFileList = []

for root, dirs, files in os.walk("/home/nathan/Eclipse"):
    for file in files:
        if(file.endswith(".flac")):
            foundFileList.append(os.path.join(root, file))
            #print(os.path.join(root, file))


for file in foundFileList:
    print(file)

