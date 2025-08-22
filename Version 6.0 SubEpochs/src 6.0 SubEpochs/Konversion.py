import re
import copy


COLORRED    = '\33[31m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORGREEN  = "\033[0;32m"
COLORPURPLE = '\033[35m'
COLOREND    = '\033[0m'



class Konversion:

    @staticmethod #works
    def get_convertedFamName(freqCombCond : str, output : str): #-> ["FAM_A"]
        """ output = \"FAM_LEFT\" | \"FAM_MIDDLE\" | \"FAM_RIGHT\" 
            -> returns \"FAM_A\" | \"FAM_B\" | \"FAM_C\"
            
            output = \"FAM_TARGET\" | \"FAM_NONTARGET\"
            -> returns list of \"FAM_A\" | \"FAM_B\" | \"FAM_C\" """

        cond = str(re.findall(r"(left|middle|right|both)", freqCombCond)[0])
        freqComb = str( re.findall(r"[A-C]{3}", freqCombCond)[0])

        letterLeft   = str(re.findall(r"[A-Z]", freqComb)[0])
        letterMiddle = str(re.findall(r"[A-Z]", freqComb)[1])
        letterRight  = str(re.findall(r"[A-Z]", freqComb)[2])

        lmr_to_abc = {
            "FAM_LEFT"   : f"FAM_{letterLeft}",
            "FAM_MIDDLE" : f"FAM_{letterMiddle}",
            "FAM_RIGHT"  : f"FAM_{letterRight}"
        }


        if( cond == "left"):
            fam_targetLMR = ["FAM_LEFT"]

        elif( cond == "middle"):
            fam_targetLMR = ["FAM_MIDDLE"]

        elif( cond == "right"):
            fam_targetLMR = ["FAM_RIGHT"]

        elif( cond == "both"):
            fam_targetLMR = ["FAM_LEFT", "FAM_BOTH"]

        famsLMR = ["FAM_LEFT", "FAM_MIDDLE", "FAM_RIGHT"]
        fam_nonTargetLMR = copy.deepcopy( famsLMR )
        for famLMR in fam_targetLMR:
            fam_nonTargetLMR.remove(famLMR)

        fam_targetABC = []
        for famLMR in fam_targetLMR:
            fam_targetABC.append( lmr_to_abc[famLMR] )

        fam_nonTargetABC = []
        for famLMR in fam_nonTargetLMR:
            fam_nonTargetABC.append( lmr_to_abc[famLMR] )

        if( output == "FAM_TARGET" ):
            return fam_targetABC
        if( output == "FAM_NONTARGET" ):
            return fam_nonTargetABC
        
        if( output == "FAM_LEFT" ):
            return lmr_to_abc["FAM_LEFT"] 
        if( output == "FAM_MIDDLE" ):
            return lmr_to_abc["FAM_MIDDLE"]
        if( output == "FAM_RIGHT" ):
            return lmr_to_abc["FAM_RIGHT"]
        
        print( COLORRED + "Invalid output chosen. Valid outputs are: " 
            + COLORGREEN + "\"FAM_TARGET\", \"FAM_NONTARGET\", \"FAM_LEFT\", \"FAM_MIDDLE\", \"FAM_RIGHT\" " + COLOREND)
        