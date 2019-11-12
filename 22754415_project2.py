#Project2 for cits1401 by Luke Bray at the University of Western Australia
#Assumptions:
#   -no words are split across two lines with a hyphen
#   -Commas in the middle of words shouldn't be split into two words eg. 3,14 != 3 14

import os
def clearWhiteSpacePunctuation(inString):
    #project description:
    # "any other punctuation or letters eg:'.' when not at the end of a sentence, should be regarded as white space so serve to end words"
    #this function clears unneeded punctuation
    #Note- it doesn't clean ".", ",", "?", "!" due to them being needed in other functions
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

def getPunctuationProfile(fileName): #returns a profile made of punctuation counts given a text file
    #punctuation characters tested are ; , " -
    profile = {} #fresh dictionary to be returned at the end
    with open(fileName, "r") as text:
        for line in text: #streams in line by line to avoid loading very large files at once, which make cause performance issues
            profile[','] = profile.get(',', 0) + line.count(",") #adds the commas to the profile
            profile[';'] = profile.get(';', 0) + line.count(";") #adds the semicolons to the profile

            line = clearWhiteSpacePunctuation(line) #cleans the line of unneeded punctuation
            for item in [".", ",", "?", "!"]: #extra punction that isn't cleaned by the previous line
                line = line.replace(item, " ")


            for word in line.split(" "): #split into words
                for characterIndex in range(0, len(word)): #loop through each character
                    try: #only count apostrophes if surrounded by letters
                        if word[characterIndex] == "'" and word[characterIndex-1].isalpha() and characterIndex>0 and word[characterIndex+1].isalpha():
                            profile["'"] = profile.get("'", 0) + 1
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters

                    try: #only count the dashes if it is surrounded by letters
                        if word[characterIndex] == "-" and word[characterIndex-1].isalpha() and word[characterIndex+1].isalpha():
                            profile["-"] = profile.get("-", 0) + 1
                    except IndexError:
                        pass #character isn't relevant anyway as it can't be surrounded by letters
    return(profile)

def getConjuctionProfile(fileName): #makes a profile of conjunction counts, given a textfile
    conjuctions = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of", "or", "since", "that", "though", "until", "when", "whenever", "whereas", "which", "while", "yet"]
    profile = {}
    x = 0
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line) #remove unneeded punctuation
            for item in [".", ",", "?", "!", '"']: #clear any other punctuation
                line = line.replace(item, " ")
            line = line.split(" ") #split into words
            for word in conjuctions:
                profile[word] = profile.get(word, 0) + line.count(word)
    return(profile)

def getUnigramProfile(fileName): #returns a profile with the count of every word given a text file
    profile = {}
    with open(fileName, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line) #remove unnneeded punctuation
            for item in [".", ",", "?", "!", '"']: #remove extra punctuation
                line = line.replace(item, "")
            for word in line.split(" "):
                if word: #check it is a valid string (removes empty counts)
                    profile[word] = profile.get(word, 0) + 1
    return(profile)

def getAverages(filename): #returns the average amount of words in the sentences
    #and the avergage amount of sentences in the file
    wordCount = 0
    sentenceCount = 0
    paragraphCount = 1 #asssume it starts with one paragraph
    with open(filename, "r") as text:
        for line in text:
            line = clearWhiteSpacePunctuation(line) #clear unneeded punctuation

            sentenceEndChars = ['.', '?', '!']
            for word in line.split(" "): #split line into words
                if word:
                    wordCount += 1
                    if word[-1] in sentenceEndChars: #check if the last character in word ends a sentence
                        sentenceCount += 1
                    if len(word) > 1: #check if the second last character in a word ends the sentence, with last being other punctuation
                        if word[-2] in sentenceEndChars:
                            if word[-1] == "'" or word[-1] == '"':
                                sentenceCount += 1

            if line == "": #if there's an empty line, increment the paragraph count
                paragraphCount += 1
    averageWordsPerSentence = round((wordCount / sentenceCount), 4) #round to 4 d.p
    averageSentencesPerParagraph = round((sentenceCount / paragraphCount), 4) #round to 4 d.p
    return(averageWordsPerSentence, averageSentencesPerParagraph)

def getCompositeProfile(filename): #creates a profile by combining the punctuation and conjunction profiles
    #also adds the count of sentences per paragraph and words per sentnce
    compositeProfile = {}
    punctuationProfile = getPunctuationProfile(filename)
    conjuctionProfile = getConjuctionProfile(filename)

    compositeProfile.update(conjuctionProfile) #adds conjunctionprofile to composite
    compositeProfile.update(punctuationProfile) #adds punctuationprofile to composite

    averageWordsPerSentence, averageSentencesPerParagraph = getAverages(filename)
    compositeProfile['words_per_sentence'] = averageWordsPerSentence
    compositeProfile['sentences_per_par'] = averageSentencesPerParagraph
    return(compositeProfile)

def compareProfiles(profile1, profile2): #calculates a score given two profiles
    sumOfDifferences = 0
    for item in profile1:
        sumOfDifferences += (profile1[item] - profile2[item])**2
    score = sumOfDifferences**0.5  #sqrt
    return(score)

def compareUnigramProfiles(profile1, profile2):
    #similar to compare profiles, but checks if the item is in the other profile
    sumOfDifferences = 0
    for item in profile1:
        if item in profile2:
            sumOfDifferences += (profile1[item] - profile2[item])**2
        else:
            sumOfDifferences += (profile1[item] - 0)**2

    for item in profile2:
        if item not in profile1:
            sumOfDifferences += (0 - profile2[item])**2

    score = sumOfDifferences**0.5
    return(score)

def main(filePath1, filePath2, feature):
    if not os.path.exists(filePath1): #checks if the file exists
        print("file1 does not exist")
        raise ValueError("Text file 1 does not exist") #throw an error that can be caught if calling main
    elif not os.path.exists(filePath2):#checks if file2 exists
        print("file2 does not exist")
        raise ValueError("Text file 2 does not exist") #throw an error that can be caught if calling main
    else: #both files exist, so can continue
        if feature == "punctuation":
            profile1 = getPunctuationProfile(filePath1)
            profile2 = getPunctuationProfile(filePath2)
        elif feature == "unigrams":
            profile1 = getUnigramProfile(filePath1)
            profile2 = getUnigramProfile(filePath2)
            score = compareUnigramProfiles(profile1, profile2)
            return(score, profile1, profile2)
        elif feature == "conjunctions":
            profile1 = getConjuctionProfile(filePath1)
            profile2 = getConjuctionProfile(filePath2)
        elif feature == "composite":
            profile1 = getCompositeProfile(filePath1)
            profile2 = getCompositeProfile(filePath2)
        else:
            print("The entered feature was not recognised")
            raise ValueError("Feature given is not acceptible") #throw an error that can be caught if calling main

    score = round(compareProfiles(profile1, profile2),4) #round to 4 d.p
    return(score, profile1, profile2) #final return yay
