import pandas as pd
from itertools import combinations

def previous_result():
    # read results
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})

    # get second to the lastr result
    mid = df["mid"].iloc[-2]
    aft = df["aft"].iloc[-2]
    eve = df["eve"].iloc[-2]

    # return a list of previous result
    return [mid, aft, eve]


def plus_minus_digits(resultList):
    # collect all the sum difference digits that are less than 10
    
    resultCombi = []
    for res in resultList:
        resultCombi.extend(list(combinations(sorted(res), 2)))

    plusMinusResults = []
    for res in resultCombi:
        x = int(res[0])
        y = int(res[1])

        # addition
        addRes = x + y
        if addRes < 10:
            plusMinusResults.append(addRes)
        
        if addRes == 10:
            plusMinusResults.append(0)
        
        # subtraction
        subRes = abs(x - y)
        plusMinusResults.append(subRes)

    return plusMinusResults


def all_results_digits(resultList):
    allDigits = []
    for res in resultList:
        allDigits.extend(list(map(lambda x: int(x), res)))

    return allDigits


def collect_all_digits(allDigits, plusMinusDigits):
    digits = allDigits + plusMinusDigits

    return {i: digits.count(i) for i in digits}


def main():
    resultList = previous_result()
    allDigits = all_results_digits(resultList)
    plusMinusDigits = plus_minus_digits(resultList)

    for k, v in sorted(collect_all_digits(allDigits, plusMinusDigits).items(), key=lambda x: x[1]):
        print(f'digit {k} == {v}')


if __name__ == "__main__":
    main()