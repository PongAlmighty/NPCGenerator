# Random NPC Gen
# Author: Vernon Kettmann
#
# Layout:
# 8 digit number from 100000000 to 999999994
# Digit1 = Sex
# Digit 2-3 = Age
# Digit 4 = Age Weight
# Digit 5-6 = City of Origin
# Digits 7-8 Digits = Occupation
# Last Digit 9 = Rank
# Digits 5-8 = last name
# ALL digits (halfed until under 50) = first name

#Old and busted circuit Python Stuff
#import board
#import simpleio
#from digitalio import DigitalInOut, Direction, Pull


import time
import random

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.IN)


led = simpleio.DigitalOut(board.D13)

#CP stuff:
#LeftButton = DigitalInOut(board.BUTTON_A)
#LeftButton.direction = Direction.INPUT
#LeftButton.pull = Pull.DOWN

LeftButton = GPIO.input(27)



def Rounder( IntInput, MaxNum):
    if (IntInput > MaxNum):
        #print("number over " + (str(MaxNum)) + "! Lowered " + (str(IntInput))) 
        IntInput /= 2
        IntInput = int(round(IntInput))
        #print(" to:" + (str(IntInput)))
        #print("")
    return(IntInput)
    
def Limiter( IntInput, MaxNum):
    while (IntInput > MaxNum):
        #print("number over " + (str(MaxNum)) + "! Lowered " + (str(IntInput))) 
        IntInput /= 2
        IntInput = int(round(IntInput))
        #print(" to:" + (str(IntInput)))
        #print("")
    return(IntInput)
    
ArrOccupations = ["Armorer", "Jeweler", "Baker", "Blacksmith", "Mapmaker", 
                    "Book Binder", "Mason", "Brewer", "Miner", "Potter", 
                    "Roper", "Carpenter", "Sailor", "Candlemaker", "Ship Builder", 
                    "Barrel Maker", "Tailor", "Coppersmith", "Farmer", "Roofer", 
                    "Fisher", "Woodcutter", "Furrier", "Winemaker", "Glassblower", 
                    "Turd Farmer", "BeadPiercer", "Swordsman", "Tollgate Keeper", 
                    "Customs Officer", "Road Worker", "Shop Worker", "Street Cleaner", 
                    "Cobbler", "Quarryman", "Medic", "Nurse", "Notary", "LampLighter", 
                    "Bell Toller", "Town Security (grunt)", "Town Security (Captian)", 
                    "Town Security (General)", "Machinist", "Hired Man", "Haberdasher", 
                    "Gilder", "Forgeman", "Animal Trainer", "Hunter", "Sandwich Artist", "Professional Sandwich"]

#Stats arranged like: Rank | Description | ICPool | OCPool
ArrQNPCStats = [[1,'Poor',1,2,1],
                [2,'Average',2,4,2],
                [3,'Good',4,6,3],
                [4,'Expert',6,8,4],
                [5,'Master',8,10,5]]

#with open('CityNames.txt', 'r') as f:
#    Cities = f.readlines()


#with open('MaleFirstNames.txt', 'r') as f:
#    MaleFNames = f.readlines()


#with open('FemaleFirstNames.txt', 'r') as f:
#    FemaleFNames = f.readlines()

#with open('ShtLastNames.txt','r') as f:
#    LNames = f.readlines()

   

while True:
        
    if LeftButton.value:
        RndNum = (random.randint(100000000, 999999994))
        RndNumStr = (str(RndNum))
        print(RndNum)
        
        # Sort out the Occupation
        OccNumStr = (RndNumStr[6:8])
        OccNumInt = (int(OccNumStr))
        OccNumInt = Rounder( OccNumInt, 50)
        OccNumStr = str(OccNumInt)
                
        # Sort out Sex
        SexNumStr = (RndNumStr[0])
        SexNumInt = (int(SexNumStr))
        # print(SexNumStr)
        if SexNumInt == 9: 
            SexString = "Non-Descript"
        elif SexNumInt % 2 == 0:
            SexString = "Male"
        else:
            SexString = "Female"
        
        

        # Sort out age
        AgeNumStr = (RndNumStr[1:3])
        AgeNumInt = int(AgeNumStr)
        #print("starting age is: " + AgeNumStr)
        AgeWeightStr = (RndNumStr[3])
        AgeWeightInt = int(AgeWeightStr)
        if AgeNumInt > 40:
            #print("checking for reduction...")
            if AgeWeightInt > 2:
                #print("Reducing Age...")
                AgeNumInt = (Rounder(AgeNumInt, 40))
                
        elif AgeNumInt < 16:
            AgeNumInt += 15
        AgeNumInt = (round(AgeNumInt))
        AgeNumStr = str(AgeNumInt)    
        
        #City of Origin
        CityNumStr = (RndNumStr[4:6])
        CityNumInt = (int(CityNumStr))
        
        with open('CityNames.txt', 'r') as f:
            Cities = f.readlines()
        
        CityName = (Cities[CityNumInt])
        Cities = [] #<-- taking out the trash
        
        #Rank:
        #Stats arranged like: Rank | Description | ICPool | OCPool
        RankStr = (RndNumStr[8])
        #print(RankStr + "-- Starting Rank") 
        RankInt = int(RankStr)
        if RankInt > 4:
            RankInt = Rounder(RankInt,4)
        
        #print(RankInt)
        RankDesc = ArrQNPCStats[RankInt][1]
        EssStr = (str(ArrQNPCStats[RankInt][2]))
        ICPStr = (str(ArrQNPCStats[RankInt][3]))
        OOCStr = (str(ArrQNPCStats[RankInt][4]))
        
        #Last Name
        LNNumString = (RndNumStr[4:8])
        LNNum = int(LNNumString)
        LNNum = Limiter(LNNum, 1000)
        LNNumString = str(LNNum)
        
        fp = open("LastNames.txt")
        for i, line in enumerate(fp):
            if i == LNNum:
                LastNameString = (line)
            elif i > LNNum:
                break
        fp.close()
        
        LastNameString = LastNameString.rstrip()
        
        #First Name:
        FNNumString = (RndNumStr[0:8])
        FNNum = int(FNNumString)
        FNNum = Limiter(FNNum, 50)
        FNNumString = str(FNNum)
        
        #print("FirstName Number: " + FNNumString)
        
        if SexNumInt % 2 == 0: #if it's even, male name
            fp = open("MaleFirstNames.txt")
            for i, line in enumerate(fp):
                if i == FNNum:
                    FirstNameString = (line)
                elif i > FNNum:
                    break
        else:
            fp = open("FemaleFirstNames.txt")
            for i, line in enumerate(fp):
                if i == FNNum:
                    FirstNameString = (line)
                elif i > FNNum:
                    break
            
        fp.close()
        
        FirstNameString = FirstNameString.rstrip()
        
        
        print("A " + AgeNumStr + " Year-old " + (SexString) + " appears before you.")
        print("Their name is: " + FirstNameString + " " + LastNameString +".") 
        print("They are from " + CityName + "and work as a " + RankDesc + " " + (ArrOccupations[OccNumInt]))
        print("Stats:")
        print("Essence: " + EssStr)
        print("In Concept Pool: " + ICPStr)
        print("Out of Concept Pool: " + OOCStr)
        print("")
        time.sleep(.2) #<-ghetto debounce
        
        
        
        
        
        
        
        
        
        
        
        
        