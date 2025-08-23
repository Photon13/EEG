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



pathAllResultsPSD  = Paths.get_pathAllResultsPSD(pNr, durchgang, typ )
print(COLORGREEN + "allResultsPSD" + COLOREND)
allResultsPSD = AllResults.loadFromPickle_allResults( pathAllResultsPSD )

AllResults.showAllResults( pathAllResultsPSD )

#print( len(allResultsPSD[0]["psdsDict"]["min_attention"]))
#print( allResultsPSD[0]["psdsDict"]["min_attention"])

#for entry in allResultsPSD[1]["freqsDict"]["min_attention"][0]:
#    if( 35.0 <= entry <= 37.0):
#        print(entry)

