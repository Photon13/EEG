from typing import List
import numpy as np  

class HelpMethods:

    @staticmethod # Helpmethod
    def berechne_meanEintraege( arr : np.ndarray | List ):
        sum = 0.0
        for e in arr:
            sum += e
        mean = sum / float( len(arr) )
        return mean