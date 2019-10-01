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
    whiteSpacePunctuation = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', "--", "- ", " -", " '", "' "]
    for punctuation in whiteSpacePunctuation:
        inString = inString.replace(punctuation, " ")

    for x in range(0, len(inString)): #removes all the fullstops in the line that are directly adjacent letters
        if inString[x] == ".":
            if x+1 < len(inString):
                if inString[x-1] != " " and inString[x+1] != " ":
                    inString = inString[:x] + " " + inString[x+1:]

    return inString



def getPunctuationProfile(fileName):
    #punctuation characters tested are ; , " -
    profile = {}
    with open(fileName, "r") as text:
        for line in text: #streams in line by line to avoid loading very large files at once, which make cause performance issues
            profile[','] = profile.get(',', 0) + line.count(",")
            profile[';'] = profile.get(';', 0) + line.count(";")

            line = clearWhiteSpacePunctuation(line)

            profile["-"] = profile.get("-", 0) + line.count("-")
            profile["'"] = profile.get("'", 0) + line.count("'")
            if line:
                if line[0] == "'":
                    profile["'"] -= 1
                if len(line) >1:
                    if line[-1] == "'":
                        profile["'"] -= 1

    return(profile)

def getConjuctionProfile(fileName):
    conjuctions = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of", "or", "since", "that", "though", "until", "when", "whenever", "whereas", "which", "while", "yet"]
    profile = {}
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line)
            line = line.replace(".", "")
            line = line.replace(",", "")
            line = line.split(" ")
            for word in conjuctions:
                profile[word] = profile.get(word, 0) + line.count(word)
    return(profile)

def getUnigramProfile(fileName):
    profile = {}
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line)
            line.replace(".", "")
            line.replace(",", "")
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
            line = clearWhiteSpacePunctuation(line)
            for word in line.split(" "):
                if word:
                    wordCount += 1
                    if word[0] == ".":
                        sentenceCount += 1
                    if word[-1] == ".":
                        sentenceCount += 1
            print("|"+line+"|")
            if line == "":
                paragraphCount += 1
    averageWordsPerSentence = wordCount / sentenceCount
    averageSentencesPerParagraph = sentenceCount / paragraphCount
    print(wordCount, sentenceCount, paragraphCount)
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

    testDict2 = {'also': 0, 'although': 0, 'and': 27, 'as': 2, 'because': 0, 'before': 2, 'but': 4, 'for': 2, 'if': 2, 'nor': 0, 'of': 13, 'or': 2, 'since': 0, 'that': 10, 'though': 2, 'until': 0, 'when': 3, 'whenever': 0, 'whereas': 0, 'which': 0, 'while': 0, 'yet': 0, ',': 41, ';': 3, '-': 1, "'": 17, 'words_per_sentence': 25.4286, 'sentences_per_par': 1.75}

    for item in testDict2:
        if testDict2[item] != profile2[item]:
            print(item, "~", testDict2[item], profile2[item])
    input(":")

testBase = "C:/Users/mooki/OneDrive/My Documents/GitHub/cits1401-Project2/project2data/project2data/"
main(testBase+"sample1.txt", testBase+"sample2.txt", "composite")
