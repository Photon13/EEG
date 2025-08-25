
class HelpClass_Auswertung:

    def getEmptyDict_data(typ):
        """ typ = \"famsABC\" | \"famsLMR\" | \"cond\" """
        if( typ == "famsABC" ):
            data = {
                "FAM_A" : [],
                "FAM_B" : [],
                "FAM_C" : []
            }      
        elif( typ == "famsLMR" ):
            data = {
                "FAM_LEFT"   : [],
                "FAM_MIDDLE" : [],
                "FAM_RIGHT"  : []
            }
        elif( typ == "cond"):
            data = {
                "left"   : [],
                "middle" : [],
                "right"  : [],
                "both"   : []
            }
        return data



    def getEmptyDict_counter(famTyp):
        """ famTyp = \"famsABC\" | \"famsLMRABC\" | \"famsCondABC\" """
        if( famTyp == "famsABC" ):
            counter = {
                "FAM_A" : 0,      ##
                "FAM_B" : 0,      ##
                "FAM_C" : 0       ##
            }
        elif( famTyp == "famsLMRABC" ):
            counter = {
                    "FAM_LEFT"   : {
                        "FAM_A" : 0,
                        "FAM_B" : 0,
                        "FAM_C" : 0
                    },
                    "FAM_MIDDLE" : {
                        "FAM_A" : 0,
                        "FAM_B" : 0,
                        "FAM_C" : 0
                    },
                    "FAM_RIGHT"  : {
                        "FAM_A" : 0,
                        "FAM_B" : 0,
                        "FAM_C" : 0
                    }
            }
        elif( famTyp == "famsCondABC"):
            counter = {
                "left"   : {
                    "FAM_A" : 0,
                    "FAM_B" : 0,
                    "FAM_C" : 0,
                },
                "middle"   : {
                    "FAM_A" : 0,
                    "FAM_B" : 0,
                    "FAM_C" : 0,
                },
                "right"   : {
                    "FAM_A" : 0,
                    "FAM_B" : 0,
                    "FAM_C" : 0,
                },
                "both"   : {
                    "FAM_A" : 0,
                    "FAM_B" : 0,
                    "FAM_C" : 0,
                },
            }
        return counter
    

    def addToInfo_counter( counter : dict, info : str ):
        for key in counter:
            if( type( counter[key] ) == dict ):
                info += f"\n\n"
                for key in counter:
                    info += f"{key} : {counter[key]}\n"
            else:
                info += f"\n\n{counter}"
            return info