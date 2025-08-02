class Elektroden:

    #     Position     |  Elektrode    | 
    #__________________|_______________|
    #    leftEar(A1)   |    13 grün    |      
    #    Forehead      |    14 grün    |
    #    rightEar(A2)  |    15 grün    |
    #    vertex(FCz)   |    20 grün    |  
    #    vertex(Cz)    |    25 grün    |
    #    vertex(Cpz)   |    27 grün    | 



    @staticmethod
    def get_usedElectrodes():
        return ["13", "14", "15", "20", "25", "27"]
    



#print( Elektroden.get_usedElectrodes() )