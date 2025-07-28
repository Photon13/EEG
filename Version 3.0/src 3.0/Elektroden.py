class Elektroden:

    #     Position     |  Elektrode    | 
    #__________________|_______________|
    #    leftEar(A1)   |    13 grün    |      
    #    Forehead      |    14 grün    |
    #    rightEar(A2)  |    15 grün    |
    #    vertex(FCz)   |    16 grün ?  |  
    #    vertex(Cz)    |    17 grün ?  | 



    RECORDING_ELECTRODE = "14" #Forehead
    #RECORDING_ELECTRODE = "16" # Vertex FCz
    #RECORDING_ELECTRODE = "17" # Vertex Cz

    REFERENCE_ELECTRODE = "13" # Ohr links
    REFERENCE_ELECTRODE = "15" # Ohr rechts
    #REFERENCE_ELECTRODE = ["13", "15"] # mean(Ohren)


    @staticmethod
    def get_usedElectrodes():
        return ["13", "14", "15", "16", "17"] # NOCH Cz EINFÜGEN !
    



#print( Elektroden.get_usedElectrodes() )