
from ast import Index
from xml.etree.ElementPath import get_parent_map
import pandas as pd


def get_gap_results(gap):
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})
    
    # reverse order and index
    df = df.iloc[::-1].reset_index(drop=True)

    gapCounter = 0
    gapItems = []

    while True:

        # max number of entries to process
        if len(gapItems) >= 2:
            break

        # value of gap to be added to gapCounter
        # gap variuable remains constant
        gapCounter += gap

        # print(df.loc[gapCounter])
        gapItems.append(df.loc[gapCounter])

        # increase whatever value of gapCounter by 1 which then be
        # added to the constant value of gap
        gapCounter += 1
    
    df2 = pd.DataFrame(gapItems)

    return df2



def main():
    allGapItems = []
    for i in range(2, 50):
        allGapItems.append(get_gap_results(i))
    
    print(allGapItems)


if __name__ == '__main__':
    main()