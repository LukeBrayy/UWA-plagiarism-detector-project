#Project2 for cits1401 by Luke Bray at the University of Western Australia
#Assumptions:
#
#
#
import math
def clearWhiteSpacePunctuation(inString):
    #project description:
    # "any other punctuation or letters eg:'.' when not at the end of a sentence, should be regarded as white space so serve to end words"
    inString = inString.lower().rstrip()
    whiteSpacePunctuation = ['#', '$', '%', '&', '(', ')', '*', '+', '/', ':', '<', '=', '>', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', "--", "- ", " -", " '", "' ", " ."]
    for punctuation in whiteSpacePunctuation:
        inString = inString.replace(punctuation, " ")

    for x in range(0, len(inString)): #removes all the fullstops in the line that are directly adjacent letters
        if inString[x] == ".":

            if x+1 < len(inString):
                if inString[x-1] in " " and inString[x+1] != " ":
                    inString = inString[:x] + " " + inString[x+1:]

    return inString



def getPunctuationProfile(fileName):
    #punctuation characters tested are ; , " -
    profile = {}
    with open(fileName, "r") as text:
        letters = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        for line in text: #streams in line by line to avoid loading very large files at once, which make cause performance issues
            profile[','] = profile.get(',', 0) + line.count(",")
            profile[';'] = profile.get(';', 0) + line.count(";")

            line = clearWhiteSpacePunctuation(line)
            for item in [".", ",", "?", "!"]:
                line = line.replace(item, " ")


            for word in line.split(" "):
                for characterIndex in range(0, len(word)):
                    try:
                        if word[characterIndex] == "'" and word[characterIndex-1] in letters and characterIndex>0 and word[characterIndex+1] in letters:
                            profile["'"] = profile.get("'", 0) + 1
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters

                    try:
                        if word[characterIndex] == "-" and word[characterIndex-1] in letters and word[characterIndex+1] in letters:
                            profile["-"] = profile.get("-", 0) + 1
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters

    return(profile)

def getConjuctionProfile(fileName):
    conjuctions = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of", "or", "since", "that", "though", "until", "when", "whenever", "whereas", "which", "while", "yet"]
    profile = {}
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line)
            for item in [".", ",", "?", "!", '"']:
                line = line.replace(item, " ")
            line = line.split(" ")
            for word in conjuctions:
                profile[word] = profile.get(word, 0) + line.count(word)
    return(profile)

def getUnigramProfile(fileName):
    profile = {}
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line)
            for item in [".", ",", "?", "!", '"']:
                line = line.replace(item, " ")
            for word in line.split(" "):
                profile[word] = profile.get(word, 0) + 1
    return(profile)

def getAverages(filename): #returns the average amount of words in the sentences
    #and the avergage amount of sentences in the file
    wordCount = 0
    sentenceCount = 0
    paragraphCount = 1
    with open(filename, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line).rstrip()

            sentenceEndChars = ['.', '?', '!']
            for word in line.split(" "):
                if word:
                    wordCount += 1
                    if word[-1] in sentenceEndChars:
                        sentenceCount += 1
                    if len(word) > 1:
                        if word[-2] in sentenceEndChars:
                            if word[-1] == "'" or word[-1] == '"':
                                sentenceCount += 1

            if line == "":
                paragraphCount += 1
    averageWordsPerSentence = round((wordCount / sentenceCount), 4)
    averageSentencesPerParagraph = round((sentenceCount / paragraphCount), 4)
    return([averageWordsPerSentence, averageSentencesPerParagraph])

def getCompositeProfile(filename):
    compositeProfile = {}
    punctuationProfile = getPunctuationProfile(filename)
    conjuctionProfile = getConjuctionProfile(filename)
    compositeProfile.update(punctuationProfile)
    compositeProfile.update(conjuctionProfile)

    averages = getAverages(filename)
    compositeProfile['words_per_sentence'] = averages[0]
    compositeProfile['sentences_per_par'] = averages[1]
    return(compositeProfile)

def compareProfiles(profile1, profile2):
    sumOfDifferences = 0
    for item in profile1:
        sumOfDifferences += (profile1[item] - profile2[item])**2
    score = sumOfDifferences**0.5
    return(score)



def main(filePath1, filePath2, feature):
    if feature == "punctuation":
        profile1 = getPunctuationProfile(filePath1)
        profile2 = getPunctuationProfile(filePath2)
    elif feature == "unigrams":
        profile1 = getUnigramProfile(filePath1)
        profile2 = getUnigramProfile(filePath2)
    elif feature == "conjunctions":
        profile1 = getConjuctionProfile(filePath1)
        profile2 = getConjuctionProfile(filePath2)
    elif feature == "composite":
        profile1 = getCompositeProfile(filePath1)
        profile2 = getCompositeProfile(filePath2)
    else:
        print("The feature given was not acceptible")
        raise ValueError("Feature given is not acceptible")

    score = compareProfiles(profile1, profile2)
    testDict1 = {'also': 1, 'although': 0, 'and': 13, 'as': 8, 'because': 0, 'before': 0, 'but': 2, 'for': 0, 'if': 0, 'nor': 0, 'of': 8, 'or': 0, 'since': 1, 'that': 6, 'though': 0, 'until': 1, 'when': 0, 'whenever': 0, 'whereas': 0, 'which': 0, 'while': 0, 'yet': 0, ',': 27, ';': 5, '-': 10, "'": 1, 'words_per_sentence': 26.75, 'sentences_per_par': 6.0}
    testDict2 = {'also': 0, 'although': 0, 'and': 27, 'as': 2, 'because': 0, 'before': 2, 'but': 4, 'for': 2, 'if': 2, 'nor': 0, 'of': 13, 'or': 2, 'since': 0, 'that': 10, 'though': 2, 'until': 0, 'when': 3, 'whenever': 0, 'whereas': 0, 'which': 0, 'while': 0, 'yet': 0, ',': 41, ';': 3, '-': 1, "'": 17, 'words_per_sentence': 25.4286, 'sentences_per_par': 1.75}


    for item in testDict2:
        if testDict2[item] != profile2[item]:
            print("sample2:", item, "~", testDict2[item], profile2[item])

    for item in testDict1:
        if testDict1[item] != profile1[item]:
            print("sample1:", item, "~", testDict1[item], profile1[item])
    print(round(score,4))
    input(":")

testBase = "C:/Users/mooki/OneDrive/My Documents/GitHub/cits1401-Project2/project2data/project2data/"
main(testBase+"sample1.txt", testBase+"sample2.txt", "composite")
