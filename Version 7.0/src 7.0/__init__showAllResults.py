from AllResults import AllResults
from Paths import Paths

COLORGREEN  = '\033[0;32m'
COLORCYAN   = '\033[36m'
COLORYELLOW = '\033[33m'
COLORPURPLE = '\033[35m'
COLORRED    = '\33[31m'
COLOREND    = '\033[0m'




pNr, durchgang = 2,"2"

#typ = "singleSpeaker"
typ = "threeSpeakers"



pathAllResults  = Paths.get_pathAllResults(pNr, durchgang, typ )
allResults = AllResults.loadFromPickle_allResults( pathAllResults )

AllResults.showAllResults( pathAllResults )

