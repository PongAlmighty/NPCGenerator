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

import board
import time
import simpleio
import random
from digitalio import DigitalInOut, Direction, Pull
import busio
import digitalio
from adafruit_rgb_display import ili9341, color565
import bitmapfont



spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# For the Metro
cs = digitalio.DigitalInOut(board.D10)
dc = digitalio.DigitalInOut(board.D9)


display = ili9341.ILI9341(spi, cs=cs, dc=dc, width=320, height=240)
display.write(0x36, b'\x3E')

bf = bitmapfont.BitmapFont(320, 240, display.pixel)  # (240, 320, display.pixel)
bf.init()
 
led = simpleio.DigitalOut(board.D13)
GoButton = DigitalInOut(board.D4)  # pin 4 gets 3.3v to start the party.
GoButton.direction = Direction.INPUT
GoButton.pull = Pull.UP
  
def Rounder(IntInput, MaxNum):
    if (IntInput > MaxNum):
        # print("number over " + (str(MaxNum)) + "! Lowered " + (str(IntInput))) 
        IntInput /= 2
        IntInput = int(round(IntInput))
        # print(" to:" + (str(IntInput)))
        # print("")
    return(IntInput)
    
def Limiter(IntInput, MaxNum):
    while (IntInput > MaxNum):
        # print("number over " + (str(MaxNum)) + "! Lowered " + (str(IntInput))) 
        IntInput /= 2
        IntInput = int(round(IntInput))
        # print(" to:" + (str(IntInput)))
        # print("")
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

# Stats arranged like: Rank | Description | ICPool | OCPool
ArrQNPCStats = [[1, 'Poor', 1, 2, 1],
                [2, 'Average', 2, 4, 2],
                [3, 'Good', 4, 6, 3],
                [4, 'Expert', 6, 8, 4],
                [5, 'Master', 8, 10, 5]]

# with open('CityNames.txt', 'r') as f:
#    Cities = f.readlines()


# with open('MaleFirstNames.txt', 'r') as f:
#    MaleFNames = f.readlines()


# with open('FemaleFirstNames.txt', 'r') as f:
#    FemaleFNames = f.readlines()

# with open('ShtLastNames.txt','r') as f:
#    LNames = f.readlines()

display.fill(0)
bf.text('Ready?!', 0, 0, color565(255, 255, 255))

while True:
    
    if not GoButton.value:
        display.fill(color565(255, 0, 0))
        RndNum = (random.randint(100000000, 999999994))
        RndNumStr = (str(RndNum))
        print(RndNum)
        
        # Sort out the Occupation
        OccNumStr = (RndNumStr[6:8])
        OccNumInt = (int(OccNumStr))
        OccNumInt = Rounder(OccNumInt, 50)
        OccNumStr = str(OccNumInt)
                
        # Sort out Sex
        SexNumStr = (RndNumStr[0])
        SexNumInt = (int(SexNumStr))
        # print(SexNumStr)
        if SexNumInt == 9 and RndNumStr[1] == 4: 
            SexString = "Non-Binary"
        elif SexNumInt % 2 == 0:
            SexString = "Man"
        else:
            SexString = "Woman"
        
        # Sort out age
        AgeNumStr = (RndNumStr[1:3])
        AgeNumInt = int(AgeNumStr)
        # print("starting age is: " + AgeNumStr)
        AgeWeightStr = (RndNumStr[3])
        AgeWeightInt = int(AgeWeightStr)
        if AgeNumInt > 40:
            # print("checking for reduction...")
            if AgeWeightInt > 2:
                # print("Reducing Age...")
                AgeNumInt = (Rounder(AgeNumInt, 40))
                
        elif AgeNumInt < 16:
            AgeNumInt += 15
        AgeNumInt = (round(AgeNumInt))
        AgeNumStr = str(AgeNumInt)    
        
        # City of Origin
        CityNumStr = (RndNumStr[4:6])
        CityNumInt = (int(CityNumStr))
        
        # with open('CityNames2.txt', 'r') as f:
        #     Cities = f.readlines()
        #    result = []
        #    CityName = result.append(CityNumInt.split('|')[1])
        #    f.close
            
        fp = open("CityNames2.txt")
        for i, line in enumerate(fp):
            if i == CityNumInt:
                LocString = (line)
            elif i > CityNumInt:
                break
        fp.close()
        LocArray = LocString.split('|')
        CityName = LocArray[0]
        ZoneName = LocArray[1]
     
        # CityName = (Cities[CityNumInt])
        Cities = []  # <-- taking out the trash
        
        # Rank:
        # Stats arranged like: Rank | Description | ICPool | OCPool
        RankStr = (RndNumStr[8])
        # print(RankStr + "-- Starting Rank") 
        RankInt = int(RankStr)
        if RankInt > 4:
            RankInt = Rounder(RankInt, 4)
        
        # print(RankInt)
        RankDesc = ArrQNPCStats[RankInt][1]
        EssStr = (str(ArrQNPCStats[RankInt][2]))
        ICPStr = (str(ArrQNPCStats[RankInt][3]))
        OOCStr = (str(ArrQNPCStats[RankInt][4]))
        
        # Last Name
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
        
        # First Name:
        FNNumString = (RndNumStr[0:8])
        FNNum = int(FNNumString)
        FNNum = Limiter(FNNum, 50)
        FNNumString = str(FNNum)
        
        # print("FirstName Number: " + FNNumString)
        
        if SexNumInt % 2 == 0:  # if it's even, male name
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
       
        print("Name: " + FirstNameString + " " + LastNameString + ".") 
        FinalNameString01 = ("Name: " + FirstNameString + " " + LastNameString)
                
        bf.text((FinalNameString01), 0, 0, color565(255, 255, 255))
        
        
        FinalAgeSexString = ("Age: " + AgeNumStr + "  Gender: " + SexString)
        bf.text((FinalAgeSexString), 0, 10, color565(255, 255, 255))
        
        FinalCityString01 = ("Hometown in the " + ZoneName)
        FinalCityString02 = (CityName)
        bf.text((FinalCityString01), 0, 20, color565(255, 255, 255))
        bf.text((FinalCityString02), 10, 30, color565(255, 255, 255))
        
        FinalOccString01 = ("Occupation: " + (ArrOccupations[OccNumInt]))
        FinalOccString02 = ("Quality of Work: " + RankDesc)
        print("They are from " + CityName + "and are known as a " + RankDesc + " " + (ArrOccupations[OccNumInt]))
        bf.text((FinalOccString01), 0, 40, color565(255, 255, 255))
        bf.text((FinalOccString02), 10, 50, color565(255, 255, 255))
        bf.text(("Stats: "), 0, 65, color565(255, 255, 255))
        bf.text(("Essence: " + EssStr), 10, 75, color565(255, 255, 255))
        bf.text(("In Concept Pool: " + ICPStr), 10, 85, color565(255, 255, 255))
        bf.text(("Out of Concept Pool: " + OOCStr), 10, 95, color565(255, 255, 255))
        
        
        print("Stats:")
        print("Essence: " + EssStr)
        print("In Concept Pool: " + ICPStr)
        print("Out of Concept Pool: " + OOCStr)
        print("")
        
        while GoButton.value:
            time.sleep(.2)
        #  time.sleep(2)  # <-ghetto debounce
        display.fill(0)
        
        
        
        
        
        
        
        
        
        
        
        
        