#Project2 for cits1401 by Luke Bray at the University of Western Australia
#Assumptions:
#   -no words are split across two lines with a hyphen

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
        testWords = []
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
                            testWords.append(word)
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters

                    try:
                        if word[characterIndex] == "-" and word[characterIndex-1] in letters and word[characterIndex+1] in letters:
                            profile["-"] = profile.get("-", 0) + 1
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters
    print("\n\n\n\n",
    testWords)
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

def equalizeProfiles(profile1, profile2): #makes sure both profiles have every item from the other profile in it
    for item in profile1:
        if item not in profile2:
            profile2[item] = 0
    for item in profile2:
        if item not in profile1:
            profile1[item] = 0
    return([profile1, profile2])


def main(filePath1, filePath2, feature):
    if feature == "punctuation":
        profile1 = getPunctuationProfile(filePath1)
        profile2 = getPunctuationProfile(filePath2)
    elif feature == "unigrams":
        profile1 = getUnigramProfile(filePath1)
        profile2 = getUnigramProfile(filePath2)
        equalProfiles = equalizeProfiles(profile1, profile2)
        profile1, profile2 = equalProfiles[0], equalProfiles[1]
    elif feature == "conjunctions":
        profile1 = getConjuctionProfile(filePath1)
        profile2 = getConjuctionProfile(filePath2)
    elif feature == "composite":
        profile1 = getCompositeProfile(filePath1)
        profile2 = getCompositeProfile(filePath2)
    else:
        print("The feature given was not acceptible")
        raise ValueError("Feature given is not acceptible")

    score = round(compareProfiles(profile1, profile2),4)
    print(score)
    print(profile1)
    print(profile2)

    """
    print("\n Differences:")

    test1 = {'also': 6, 'although': 1, 'and': 1282, 'as': 240, 'because': 17, 'before': 33, 'but': 188, 'for': 278, 'if': 117, 'nor': 7, 'of': 820, 'or': 113, 'since': 0, 'that': 340, 'though': 11, 'until': 9, 'when': 106, 'whenever': 0, 'whereas': 0, 'which': 47, 'while': 54, 'yet': 5, ',': 2334, "'": 551, '-': 411, ';': 226, 'words_per_sentence': 19.5435, 'sentences_per_par': 2.6288}
    test2 = {'also': 4, 'although': 0, 'and': 6422, 'as': 552, 'because': 223, 'before': 163, 'but': 1040, 'for': 873, 'if': 424, 'nor': 61, 'of': 1768, 'or': 393, 'since': 14, 'that': 1081, 'though': 36, 'until': 3, 'when': 430, 'whenever': 11, 'whereas': 1, 'which': 117, 'while': 52, 'yet': 59, ',': 8190, "'": 4454, ';': 1562, '-': 1019, 'words_per_sentence': 18.9841, 'sentences_per_par': 2.5213}

    for item in profile1:
        if profile1[item] != test1[item]:
            print(item, "| Mine:", profile1[item], "Yours:", test1[item])

    """
testBase = "C:/Users/mooki/OneDrive/My Documents/GitHub/cits1401-Project2/project2data/project2data/"
#main(testBase+"Banjo_Paterson.txt", testBase+"Hucklebery_Finn.txt","composite")
#main(testBase +"Lawrence_Kangaroo.txt", testBase + "Lawrence_Sea_Sardinia.txt","composite")
#main(testBase +"Lawrence_Unconsiousness.txt", testBase + "Lawrence_Sea_Sardinia.txt","composite")

main(testBase+"Lawson_Children_of_the_Bush.txt",testBase+"lifeOnMississippi.txt","composite")
#main(testBase+"Hucklebery_Finn.txt", testBase+"lifeOnMississippi.txt", "unigrams")
#Banjo_Paterson.txt
