from AllResults import AllResults
from BlockParams import BlockParams
from HelpClass_PeakAnalysis import HelpClass_PeakAnalysis
from HelpClass_Auswertung import HelpClass_Auswertung
from Konversion import Konversion
from Statistics import Statistics
from Plots import Plots
from Paths import Paths

import matplotlib.pyplot as plt
from typing import List
import numpy as np
from scipy import stats
import copy
import re

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'


#########################################################################################################################################################################
class Auswertung:

    @staticmethod
    def plot_zeitlVerlaufPeaks( peaksInOrder : dict[List], famsToUseABC : List[str], expType : str, info : str, pNr : int ):
        title_fontSize = 17
        label_fontSize = 15
        tick_fontSize = 13

        ##
        if( expType == "singleSpeaker" ): #X-AXIS: SECONDS (MEAN TIME POINT INTERVAL)
            times = []
            blockStart = 0
            for i in range( 2 ):
                for j in range( 1, 29+1 ):
                    times.append( blockStart + j*5 )
                blockStart += 150

    
        elif( expType == "threeSpeakers" ):
            times = []
            blockStart = 0
            for i in range( 72 ):
                for j in range( 1, 5+1 ):
                    times.append( blockStart + j*5 )
                blockStart += 30

        peakList_famA = peaksInOrder["FAM_A"]
        peakList_famB = peaksInOrder["FAM_B"]
        peakList_famC = peaksInOrder["FAM_C"]

        
        plt.figure(figsize=(10, 5))

        print(times)

        blockStarts = []
        t = (times[0]-5)
        while True:
            blockStarts.append( t )
            if( t >= times[-1]-5 ):
                break
            if( expType == "threeSpeakers"):
                t += 120
            elif( expType == "singleSpeaker"):
                t += 150

        #for t in range( (times[0]-5), (times[-1]-5)+1, (120) ):
        #    blockStarts.append( t )

        if( expType == "threeSpeakers" ): #CONVERT TO MINUTES
            for i in range( len(blockStarts) ):
                blockStarts[i] = int( float(blockStarts[i])/60.0 )
            for k in range( len( times) ):
                times[k] = float(times[k])/60.0 

        plt.plot( times, peakList_famA, label="famA", color = "black" )
        if( expType == "threeSpeakers" ):
            plt.plot( times, peakList_famB, label="famB", color = "blue" )
            plt.plot( times, peakList_famC, label="famC", color = "orange" )

        plt.xticks(blockStarts, fontsize=tick_fontSize) 
        plt.yticks(fontsize=tick_fontSize)

        for blockStart in blockStarts:
            plt.axvline( blockStart, color='grey', linestyle=':', alpha=0.8, linewidth=2.0, zorder=0 )



        if( expType == "threeSpeakers" ):
            title = f"Participant {pNr}"
            plt.xlabel(f"\nt [min]{info}", fontsize=label_fontSize)
        elif( expType == "singleSpeaker" ):
            title = "Evolution of Peak Height (Single Speaker Experiment)"
            plt.xlabel(f"\nt [sec]{info}", fontsize=label_fontSize)


        plt.title(f"\n{title}", fontsize=title_fontSize, fontweight='bold', pad=20)

        plt.ylabel("Relative Peak Height\n", fontsize=label_fontSize) 

        plt.legend(loc="upper left", fontsize=tick_fontSize)



        plt.tight_layout()
        plt.show()
        inp = input("any ")



    #########################################################################################################################################################################
    #########################################################################################################################################################################
    #########################################################################################################################################################################


    @staticmethod #funzt scheinbar
    def famABC_VS_famABC( peakDict : dict, info : str, pNr : int ):
        print( COLORGREEN + f"\nparticipant{pNr}" + COLOREND)
        print( COLORYELLOW + f"Comparison of famA, famB and famC\n" + COLOREND)

        data    = HelpClass_Auswertung.getEmptyDict_data("famsABC")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsABC")

        for freqCombCond in peakDict:
            
            for famNameABC in peakDict[freqCombCond]:

                for peak in peakDict[freqCombCond][famNameABC]:
                    data[famNameABC].append( peak ) 
                    counter[famNameABC] +=1 


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for letter in ["A", "B", "C"]:
            data[f"fam{letter}"] = data[f"FAM_{letter}"]
            del data[f"FAM_{letter}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"Participant {pNr}",        ##
            ylabel        = "Relative Peak Height", 
            xlabel        = f"\n{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")


    #########################################################################################################################################################################


    @staticmethod #funzt scheinbar
    def famLMR_VS_famLMR( peakDict : dict, info : str, famsToUseABC : List[str], pNr : int):
        print( COLORGREEN + f"\nparticipant{pNr}" + COLOREND)
        print( COLORYELLOW + f"famLeft VS famMiddle VS famRight\n" + COLOREND)
        print( COLORCYAN + f"Included fams: {famsToUseABC}" + COLOREND)

        data = HelpClass_Auswertung.getEmptyDict_data("famsLMR")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsLMRABC")

        for freqCombCond in peakDict:

            for famNameLMR in ["FAM_LEFT", "FAM_MIDDLE", "FAM_RIGHT"]:
                famNameABC = Konversion.get_convertedFamName(freqCombCond, famNameLMR)  ##
                if( famNameABC in famsToUseABC ):
                    for peak in peakDict[freqCombCond][famNameABC]:
                        data[famNameLMR].append(peak)
                        counter[famNameLMR][famNameABC] +=1


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for pos in ["left", "middle", "right"]:
            data[f"fam{pos.capitalize()}\n"] = data[f"FAM_{pos.upper()}"]
            del data[f"FAM_{pos.upper()}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"Participant {pNr}",    ##
            ylabel        = "\nRelative Peak Height", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")


#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################

    @staticmethod
    def famLMR_VS_famLMR_perCond( peakDict : dict, info : str, famsToUseABC : List[str], targetPos : str, pNr : int ):
        print( COLORGREEN + f"\nparticipant{pNr}" + COLOREND)
        print( COLORYELLOW + f"target = {targetPos}\n" + COLOREND)
        print( COLORCYAN + f"Included fams: {famsToUseABC}" + COLOREND)

        data    = HelpClass_Auswertung.getEmptyDict_data("famsLMR")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsLMRABC")
        
        for freqCombCond in peakDict:
            cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0])

            for pos in ["left", "middle", "right"]:
                if( cond == targetPos.lower() ):
                    famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{pos.upper()}")
                    if( famNameABC in famsToUseABC ):
                        for peak in peakDict[freqCombCond][famNameABC]:
                            data[f"FAM_{pos.upper()}"].append(peak)
                            counter[f"FAM_{pos.upper()}"][famNameABC] +=1

        
        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )


        #Rename data keys (and thus x-axis labels):
        for pos in ["left", "middle", "right"]:
            if( pos == targetPos.lower() ):
                targetTyp = "target"
            else:
                targetTyp = "nonTarget"

            data[f"fam{pos.capitalize()}\n({targetTyp})"] = data[f"FAM_{pos.upper()}"]
            del data[f"FAM_{pos.upper()}"]

        Plots.boxplot( 
            data          = data, 
            title         = f"Participant {pNr}\ntarget = {targetPos}",    ##
            ylabel        = "Relative Peak Height", 
            xlabel        = f"\nPosition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")

#########################################################################################################################################################################

    @staticmethod
    def cond_VS_cond_perfamLMR( peakDict : dict, info : str, famsToUseABC : List[str], famLMR : str, pNr : int ):
        print( COLORGREEN + f"\nparticipant{pNr}\n" + COLOREND)
        print( COLORYELLOW + f"{famLMR} per Condition\n" + COLOREND)
        print( COLORCYAN + f"Included fams: {famsToUseABC}" + COLOREND)

        data    = HelpClass_Auswertung.getEmptyDict_data("cond")
        counter = HelpClass_Auswertung.getEmptyDict_counter("famsCondABC")

        for freqCombCond in peakDict:
            cond = str( re.findall(r"(left|middle|right|both)", freqCombCond)[0] )
            pos  = str( re.findall(r"(Left|Middle|Right)", famLMR)[0] )

            famNameABC = Konversion.get_convertedFamName(freqCombCond, f"FAM_{pos.upper()}")
            if( famNameABC in famsToUseABC ):
                for peak in peakDict[freqCombCond][famNameABC]:
                        data[cond].append(peak)
                        counter[cond][famNameABC] +=1


        if( info != "" and info != " " ):
            info = HelpClass_Auswertung.addToInfo_counter( counter, info )


        Statistics.test_sigDifference( data )

        Plots.boxplot( 
            data          = data, 
            title         = f"Participant {pNr}",    ##
            ylabel        = "\nRelative Peak Height", 
            xlabel        = f"\nCondition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")