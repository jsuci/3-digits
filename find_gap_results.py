
from itertools import combinations, chain
from sunau import AUDIO_FILE_ENCODING_FLOAT
import pandas as pd


def get_gap_results(gap):
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})
    
    # reverse order and index
    df = df.iloc[::-1].reset_index(drop=True)

    gapCounter = 0
    gapItems = []

    while True:

        # max number of entries to process
        if len(gapItems) >= 3:
            break

        # value of gap to be added to gapCounter
        # gap variuable remains constant
        gapCounter += gap

        # print(df.loc[gapCounter])
        gapItems.append(df.loc[gapCounter])

        # increase whatever value of gapCounter by 1 which then be
        # added to the constant value of gap
        gapCounter += 1
    
    # gap collection df
    df2 = pd.DataFrame(gapItems)

    commonPairs = get_common_pairs(df2)

    if commonPairs:
        print(f"gap: {gap}")
        for eachPair in commonPairs:
            print(f"pair: {eachPair}")
            print(df2.iloc[::-1])
            print("\n")




def get_common_pairs(df):

    # collect all pairs from all rows
    allPairsRow = []

    # collect all pairs from first row
    firstRowPairs = set()
    for eachResult in df.iloc[0, 1:]:
        # create pairs for each result
        pairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])

        # combine all pairs to a set
        # to remove duplicates
        firstRowPairs = set().union(pairs)

    secondRowPairs = set()
    for eachResult in df.iloc[1, 1:]:
        pairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])
        secondRowPairs = set().union(pairs)

    thirdRowPairs = set()
    for eachResult in df.iloc[2, 1:]:
        pairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])
        thirdRowPairs = set().union(pairs)

    # combine all pairs from 3 rows
    allPairsRow.extend(chain(firstRowPairs, secondRowPairs, thirdRowPairs))




    # collect pair that repeat 3x
    qualifiedPairs = []
    for e in allPairsRow:
        if allPairsRow.count(e) == 3:
            if e not in qualifiedPairs:
                qualifiedPairs.append(e)
    
    return qualifiedPairs


def main():
    allGapItems = []
    for i in range(2, 100):
        allGapItems.append(get_gap_results(i))



if __name__ == '__main__':
    main()