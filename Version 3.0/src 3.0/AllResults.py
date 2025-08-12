import pandas as pd
import numpy as np
from typing import List
import pickle
import os.path
import sys

from IPython import display

COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'

class AllResults:

    @staticmethod
    def create_newAllResultsList( pathAllResults : str ):
        if( os.path.isfile(pathAllResults) == False ):
            allResults = list()
            AllResults.saveAsPickle_allResults(allResults, pathAllResults)
        else:
            print( COLORRED + "allResults already exists on given path! Creation of new List aborted. " + COLOREND )



    @staticmethod
    def saveAsPickle_allResults( allResults : List[dict], path : str ):
        with open(path, "wb") as f:
            pickle.dump(allResults, f)



    @staticmethod
    def loadFromPickle_allResults( path : str ) -> List:
        with open(path, "rb") as f:
            allResults = pickle.load(f)
        return allResults



    @staticmethod
    def deleteEntry_atGivenIndex(allResults : List, index : int):
        del allResults[index]
        return allResults
    


    @staticmethod
    def showAllResults( input : str | List[dict] ):
        if(type(input) == str):
            allResults = AllResults.loadFromPickle_allResults( input)
        else:
            allResults = input
        for i in range( len(allResults) ):
            print(COLORYELLOW + f"list index = {i}\n" + COLOREND)
            for key in allResults[i]:
                print(COLORCYAN + f"{key} : {allResults[i][key]}" + COLOREND + "\n")













