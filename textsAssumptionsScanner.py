import os
#use to test the existence of assumed conditions for the text files
def findFiles(directory, extension): #function that returns all filepaths in a given directory, ending in a given string(extension)
    dirCollection = []
    for root, dirs, files in os.walk(directory): #loop through all filepaths, and every directory
        for file in files:
            if file.endswith(extension):
                location = os.path.join(root, file) #get the full current filepath
                dirCollection.append(location) #add the filepath, minus the given directory, as we already know what that is
    return dirCollection

def main(filename):
    with open(filename) as E:
        allLines = E.readlines()
        for x in range(0, len(allLines)):
            line = allLines[x]
            if line[-1] == "-":
                print(line)
                print(allLines[x+1])
for file in findFiles("C:\\Users\\mooki\\OneDrive\\My Documents\\GitHub\\cits1401-Project2\\project2data\\", ".txt"):
    main(file)
    print("donefile")
input("done")
