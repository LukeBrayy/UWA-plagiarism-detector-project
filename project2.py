#Project2 for cits1401 by Luke Bray at the University of Western Australia
#Assumptions:
#
#
#
def clearWhiteSpacePunctuation(inString):
    #project description:
    # "any other punctuation or letters eg:'.' when not at the end of a sentence, should be regarded as white space so serve to end words"
    whiteSpacePunctuation = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', "--", "- ", " -", " '", "' "]
    for punctuation in whiteSpacePunctuation:
        inString.replace(punctuation, " ")

    for x in range(0, len(inString)): #removes all the fullstops in the line that are directly adjacent letters
        if inString[x] == ".":
            if inString[x-1] != " " and inString[x+1] != " ":
                inString = inString[:x] + " " + inString[x+1:]
    return(inString)



def getPunctuationProfile(fileName):
    #punctuation characters tested are ; , " -
    profile = {}
    with open(fileName, "r") as text:
        my_dict[some_key] = my_dict.get(some_key, 0) + 1

        for line in text.readline(): #streams in line by line to avoid loading very large files at once, which make cause performance issues
            profile[','] = profile.get(',', 0) + line.count(",")
            profile[';'] = profile.get(';', 0) + line.count(";")

            line = clearWhiteSpacePunctuation(line)

            profile["-"] = profile.get("-", 0) + line.count("-")
            profile["'"] = profile.get("'", 0) + line.count("'")

    return(profile)

def getConjuctionProfile(fileName):
    conjuctions = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of", "or", "since", "that", "though", "until", "when", "whenever", "whereas", "which", "while", "yet"]
    profile = {}
    with open(fileName, "r") as text:
        for line in text.readline():
            for word in conjuctions:
                profile[word] = profile.get(word, 0) + line.count(word)
    return(profile)

def getUnigramProfile(fileName):
    profile = {}
    with open(fileName, "r") as textfile:
        for line in textfile.readline():
            line = clearWhiteSpacePunctuation(line)
            for word in line.split(" "):
                profile[word] = profile.get(word, 0) + 1
    return(profile)

def getAverage(filename): #returns the average amount of words in the sentences
    #and the avergage amount of sentences in the file
    wordCount = 0
    sentenceCount = 0
    paragraphCount
    with open(filename, "r") as text:
        wordCount = 0
        sentenceCount = 0
        for line in filename.readline():
            line = clearWhiteSpacePunctuation(line)
            for word in line.split(" "):
                wordCount += 1
                if word[0] ==".":
                    sentenceCount += 1
                if word[-1] == ".":
                    sentenceCount += 1
            if line == "" or " ":
                paragraphCount += 1
    averageWordsPerSentence = wordCount / sentenceCount
    averageSentencesPerParagraph = sentenceCount / paragraphCount
    return([averageWordsPerSentence, averageSentencesPerParagraph])




def composite(filename):
    compositeProfile = {}
    punctuationProfile = getPunctuationProfile(filename)
    conjuctionProfile = getConjuctionProfile(filename)
    compositeProfile.update(punctuationProfile)
    compositeProfile.update(conjuctionProfile)

    getAverages(filename)




def main(filePath1, filePath2, feature):)
    if feature not in ["punctuation", "unigrams", "conjuctions", "composite"]:
        print("The feature given was not acceptible")
        raise ValueError("Feature given is not acceptible")
