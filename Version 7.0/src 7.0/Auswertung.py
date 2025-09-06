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
        print( COLORGREEN + f"\nparticipant{pNr}\n" + COLOREND)
        title_fontSize = 17
        label_fontSize = 15
        tick_fontSize = 13

        ##
        if( expType == "singleSpeaker" ): #X-AXIS: SECONDS (MEAN TIME POINT INTERVAL)
            peakList = peaksInOrder["FAM_A"]
            n_intervals_perBlock = int( (150 - 5 )/ 5 ) #last interval missing bec it would be only 5 secs long
            
            timesList = []
            t = 5 # 1st interval mean timepoint at 5 sec recording
            interval = 1 #intervalNr
            for i in range( 2*n_intervals_perBlock ):
                timesList.append( t )
                if( interval == n_intervals_perBlock ):
                    t += 10  #jump to next block
                    interval = 1 #reset interval nr
                elif( interval < n_intervals_perBlock ):
                    t += 5   #jump to next interval
                    interval += 1
                else:
                    print(COLORRED + "Invalid interval! " + COLOREND + "Message from plot_zeitlVerlaufPeaks().")

            plt.figure(figsize=(10, 5))
            plt.plot( timesList, peakList, label="", color = "black" )
            
            title = "Evolution of peak hight (singleSpeaker)"
            plt.legend(loc="upper left")

            for markerPosition in [ (150 - 5), (150 + 5) ]: #boundary between att and nonAtt
                    plt.axvline( markerPosition, color='grey', linestyle=':', alpha=0.8, linewidth=3.0, zorder=0 )
            
       
        
        ##
        elif( expType == "threeSpeakers" ): #X-AXIS: BLOCK NR
            blockList = [] # block X: X.0, X.2 ... X.8
            n_intervals_perBlock = 5
            t = 0.0 + 1.0/6.0 # Mitte vom ersten Intervall ist bei 1/6 vom Block
            interval = 1 #intervalNr
            for i in range( 72*n_intervals_perBlock ):
                print(t)
                blockList.append( t )
                if( interval == n_intervals_perBlock ):
                    t += 2.0/6.0  #jump to next block
                    interval = 1 #reset interval nr
                elif( interval < n_intervals_perBlock ):
                    t += 1.0/6.0   #jump to next interval
                    interval += 1
                else:
                    print(COLORRED + "Invalid interval! " + COLOREND + "Message from plot_zeitlVerlaufPeaks().")
                
     
            peakList_famA = peaksInOrder["FAM_A"]
            peakList_famB = peaksInOrder["FAM_B"]
            peakList_famC = peaksInOrder["FAM_C"]

            plt.figure(figsize=(10, 5))
            plt.plot( blockList, peakList_famA, label="famA", color = "blue" )
            plt.plot( blockList, peakList_famB, label="famB", color = "black" )
            plt.plot( blockList, peakList_famC, label="famC", color = "orange" )

            title = "Evolution of peak hight (threeSpeakers)"
            plt.legend(loc="upper left")

            for markerPosition in [ 23.0, 47.0 ]: #sHOW TRIAL BOUNDARIES
                plt.axvline( markerPosition, color='grey', linestyle=':', alpha=0.8, linewidth=4.0, zorder=0 ) #linewidt must set 2x the actal value! e.g. 10 sec toal width -> linewidth=20.0
            for markerPosition in range(0, 71+4, 4):
                plt.axvline( float(markerPosition), color='grey', linestyle=':', alpha=0.8, linewidth=2.0, zorder=0 )

            plt.xticks(range(0, 71+4, 4), fontsize=tick_fontSize)

            #plt.xlim( 22, 29 ) ## close-up

        #ax = plt.gca() # Access the current Axes object
        #ax.yaxis.get_offset_text().set_fontsize(tick_fontSize) # Change font size of the offset text (scale factor)
        plt.title(f"\n{title}", fontsize=title_fontSize, fontweight='bold', pad=20)
        plt.xlabel(f"Start of block nr.{info}", fontsize=label_fontSize)
        plt.ylabel("Relative Peak Height", fontsize=label_fontSize) 
        
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
            ylabel        = "Relative Peak Height", 
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

    def cond_VS_cond_perfamLMR( peakDict : dict, info : str, famsToUseABC : List[str], famLMR : str, pNr : int ):
        print( COLORGREEN + f"\nparticipant{pNr}\n" + COLOREND)
        print( COLORYELLOW + f"{famLMR} per Condition\n" + COLOREND)

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
            ylabel        = "Relative Peak Height", 
            xlabel        = f"\nCondition{info}", 
            axhline       = None
        )
        print("\n\n\n\n\n")