 
from itertools import combinations, chain
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

        # value of gap to be i`i``added to gapCounter
        # gap variuable remains constant
        gapCounter += gap

        # print(df.loc[gapCounter])
        gapItems.append(df.loc[gapCounter])

        # increase whatever value of gapCounter by 1 which then be
        # added to the constant value of gap
        gapCounter += 1
    
    # gap collection df
    df2 = pd.DataFrame(gapItems)

    # get common pairs
    midCommonPairs = get_common_pairs(df2, 1)
    aftCommonPairs = get_common_pairs(df2, 2)
    eveCommonPairs = get_common_pairs(df2, 3)

    if midCommonPairs:
        print(f"MIDDAY PAIRS")
        print(f"gap: {gap}")
        for eachPair in midCommonPairs:
            print(f"pair: {eachPair}")
            print(df2.iloc[::-1])
            print("\n\n")

    if aftCommonPairs:
        print(f"AFTERNOON PAIRS")
        print(f"gap: {gap}")
        for eachPair in aftCommonPairs:
            print(f"pair: {eachPair}")
            print(df2.iloc[::-1])
            print("\n\n")

    if eveCommonPairs:
        print(f"EVENING PAIRS")
        print(f"gap: {gap}")
        for eachPair in eveCommonPairs:
            print(f"pair: {eachPair}")
            print(df2.iloc[::-1])
            print("\n\n")


def get_common_pairs(df, day):

    # process mid day result
    midResultPairs = set()

    # get only the mid day result
    midResult = df.iloc[0, day]

    # create pairs from mid day result
    midPairs = set([''.join(sorted(x)) for x in combinations(midResult, 2)])

    # combine all pairs to a set to remove duplicates
    midResultPairs.update(midPairs)

    # process afternoon result
    aftResultPairs = set()
    aftResult = df.iloc[1, day]
    aftPairs = set([''.join(sorted(x)) for x in combinations(aftResult, 2)])
    aftResultPairs.update(aftPairs)

    # process evening result
    eveResultPairs = set()
    eveResult = df.iloc[2, day]
    evePairs = set([''.join(sorted(x)) for x in combinations(eveResult, 2)])
    eveResultPairs.update(evePairs)

    qualifiedPairs = midResultPairs.intersection(aftResultPairs).intersection(eveResultPairs)
    
    return qualifiedPairs


def main():

    for i in range(2, 100):
        get_gap_results(i)



if __name__ == '__main__':
    main()