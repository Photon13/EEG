class BlockParams:

    FAM_A = 15.9
    FAM_B = 41.3
    FAM_C = 66.7

    # not(45-55 Hz)  #powerline
    # not(22.5-27.5) #subharmonics of power line # nicht sichtbar?
    # beating freq: 25.4 Hz

    N_BLOCKS = 3*4*6
    BLOCK_LENGTH = 30 # [sec]

    freqCombs = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    freqComb : str

    conditions = ["left", "middle", "right", "both"]
    condition : int

    trials = [1, 2, 3]
    trial : int





@staticmethod
def main_new():

    blockDict = dict()
    for i in range( BlockParams.N_BLOCKS ):
        blockDict[f"block{i}"] = {
            "trial" : None,
            "freqComb" : None,
            "condition" : None
        }

    blockNr = 0
    for trial in BlockParams.trials:
        
        for freqComb in BlockParams.freqCombs:

            for condition in BlockParams.conditions:
  
                blockDict[f"block{blockNr}"]["trial"] = trial
                blockDict[f"block{blockNr}"]["freqComb"] = freqComb
                blockDict[f"block{blockNr}"]["condition"] = condition
                #pushBlockDictToJson()

                #Leds.turnTargetLedOn(conditon)
                #freefield.write()
                #freefield.play
                #time.sleep()
                blockNr += 1
                #time.sleep(2)
            inp = input("Contine? [yes]: ")
            
    print(blockDict)

main_new()