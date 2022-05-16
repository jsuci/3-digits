
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

    commonResults = get_repeat_results(df2)
    if commonResults:
        # print(f"gap: {gap}")
        # for eachResult in commonResults:
        #     print(f"common: {eachResult}")
        #     print(df2.iloc[::-1])
        #     print("\n")

        commonPairs = get_common_pairs(df2)
        if commonPairs:
            print(f"gap: {gap}")
            print(f"common: {commonResults}")
            for eachPair in commonPairs:
                print(f"pair: {eachPair}")
                print(df2.iloc[::-1])
                print("\n")


def get_repeat_results(df):
    # process first row results
    firstRowResults = set()
    for eachResult in df.iloc[0, 1:]:
        # sort each results and collect
        sortedVal1 = ''.join(sorted(eachResult))
        firstRowResults.add(sortedVal1)

    thirdRowResults = set()
    for eachResult in df.iloc[2, 1:]:
        # sort each results
        sortedVal2 = ''.join(sorted(eachResult))
        thirdRowResults.add(sortedVal2)


    commonResults = firstRowResults.intersection(thirdRowResults)

    return commonResults



def get_common_pairs(df):

    # process first row
    firstRowPairs = set()
    for eachResult in df.iloc[0, 1:]:
        # create pairs for each result in this row
        firstPairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])

        # combine all pairs to a set to remove duplicates
        firstRowPairs.update(firstPairs)

    # process second row
    secondRowPairs = set()
    for eachResult in df.iloc[1, 1:]:
        secondPairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])
        secondRowPairs.update(secondPairs)

    # process third row
    thirdRowPairs = set()
    for eachResult in df.iloc[2, 1:]:
        thirdPairs = set([''.join(sorted(x)) for x in combinations(eachResult, 2)])
        thirdRowPairs.update(thirdPairs)

    qualifiedPairs = firstRowPairs.intersection(secondRowPairs).intersection(thirdRowPairs)
    
    return qualifiedPairs


def main():

    for i in range(2, 100):
        get_gap_results(i)



if __name__ == '__main__':
    main()