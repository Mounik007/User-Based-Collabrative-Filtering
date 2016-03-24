# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:35:28 2015

@author: mounik
"""

import sys
import csv
import collections
import math

def Predict(userID,kSpeificLister, movieName, dictUserIDKey):
    sumNumerator = 0
    sumDenominator = 0
    for elementList in kSpeificLister:
        tempList = []
        tempList = dictUserIDKey[elementList[0]]
        for eleList in tempList:
            if(eleList[0]==movieName):
                sumNumerator += float(eleList[1])*float(elementList[1])
                sumDenominator += float(elementList[1])

    if(sumDenominator!=0 and sumNumerator!=0):
        probabilityValue = sumNumerator/sumDenominator
    else:
        probabilityValue = 0
    print("\n"+str(probabilityValue))
    
def K_NearestNeighbours(userID, dictWeightedSimilarty,desiredNearestNeighbours):
    lstKValueList = []
    for element in dictWeightedSimilarty:
        lstTempList = []
        lstTempList.append(element)
        lstTempList.append(dictWeightedSimilarty[element])
        lstKValueList.append(lstTempList) 
        
    sortedList = sorted(lstKValueList, key= lambda kValuelst:(kValuelst[1],kValuelst[0]), reverse = True)
    kSpecificList = []
    kSpecificFilterList = []
    for index in range(desiredNearestNeighbours+1):
        kSpecificList.append(sortedList[index])
    for ind in range(1,len(kSpecificList)):
        print(kSpecificList[ind][0]+" "+str(kSpecificList[ind][1]))
        kSpecificFilterList.append(kSpecificList[ind])
    return kSpecificFilterList

def Pearson_Corelation(lstUserIDValues,lstCoUserIDValues, avgUserID, avgCoUserID, movieName):
    
    sumNumerator= 0
    sumDenominator1 =0
    sumDenominator2 =0
    for elementList in lstUserIDValues:
        for eleList in lstCoUserIDValues:
            if((not(elementList[0] == movieName)) & (not(eleList[0] == movieName))):
                if(elementList[0] == eleList[0]):
                    sumNumerator += (float(elementList[1])-float(avgUserID))*(float(eleList[1])-float(avgCoUserID))
                    sumDenominator1 += (float(elementList[1])-float(avgUserID))**2
                    sumDenominator2 += (float(eleList[1])-float(avgCoUserID))**2
    
    sumDenominator = (math.sqrt(sumDenominator1))*(math.sqrt(sumDenominator2))
    if(sumDenominator!=0):
        weightedSimilarity = sumNumerator/sumDenominator
    else:
        weightedSimilarity = 0
    return weightedSimilarity
                    

def CalaculatePredictedRating(userID,dictUserIDKey,movieName, desiredNearestNeighbours):
    dictAvgRatingUser = {}
    dictWeightedSimilarty = {}
    
    for item in dictUserIDKey:
        lstAllRatingsForUserOnMovie = []
        for aList in dictUserIDKey[item]:
            lstAllRatingsForUserOnMovie.append(float(aList[1]))
        averageRating = float(sum(lstAllRatingsForUserOnMovie))/float(len(lstAllRatingsForUserOnMovie))
        dictAvgRatingUser[item] = averageRating
    
    for singUser in dictAvgRatingUser:
        weightedSimilarity = Pearson_Corelation(dictUserIDKey[userID],dictUserIDKey[singUser], dictAvgRatingUser[userID], dictAvgRatingUser[singUser],movieName)
        dictWeightedSimilarty[singUser] = weightedSimilarity
    
    kSpecificLister = []
    kSpecificLister = K_NearestNeighbours(userID, dictWeightedSimilarty, desiredNearestNeighbours)
    Predict(userID,kSpecificLister, movieName, dictUserIDKey) 
           

if __name__ == '__main__':
    lstInputData = []
    userID = str(sys.argv[2])
    movieName = str(sys.argv[3])
    desiredNearestNeighbours = int(sys.argv[4])
    dictUserIDKey = collections.defaultdict(list)
    with open(sys.argv[1]) as tsvFile:    
        tsvReader = csv.reader(tsvFile, delimiter ="\t")
        for line in tsvReader:
            lstInputData.append(line)
            lstUserIDValue = []
            lstItemIDValue = []
            lstUserIDValue.append(line[2])
            lstUserIDValue.append(line[1])
            dictUserIDKey[line[0]].append(lstUserIDValue)    
    CalaculatePredictedRating(userID,dictUserIDKey, movieName, desiredNearestNeighbours)