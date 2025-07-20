from typing import List
import numpy as np  

class HelpMethods:

    @staticmethod # Helpmethod
    def berechneMean_Eintraege( arr : np.ndarray | List ):
        sum = 0.0
        for e in arr:
            sum += e
        mean = sum / float( len(arr) )
        return mean