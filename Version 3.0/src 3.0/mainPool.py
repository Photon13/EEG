from Main_singleBlock import Main_singleBlock



# Loop über alle Blöcke !
psds_normiert, freqs, P_fABC_normiert, P_fLMR_normiert, P_fTarget_normiert, P_fNonTarget_normiert = Main_singleBlock.main_singleBlock()


# Gleichartige Blöcke müssen noch zusammengepoolt werden
# Export P_fABC's etc. als pd.dataframe?


# FALLS freqs identisch sein sollten für alle BLöcke, dann kann man psds_normiert über Blöcke gleicher Art mitteln
# und dann im Diagramm gegen freqs abbilden

