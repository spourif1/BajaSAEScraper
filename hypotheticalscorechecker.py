UMBCCOST = 6577.63
HYPOTHETICALHOPKINSCOST = 7201.98
UMBCSCORE = 66.63
HOPKINSSCORE = 58.99
MAXITERATIONS = 50000

def costscorecalculator(maxcost,mincost,teamcost):
    score = 0
    numerator = (maxcost - teamcost)
    denominator = (maxcost - mincost)
    divideshit = (numerator/denominator)
    score = divideshit * 80
    roundedscore = round(score,2)
    return roundedscore



if __name__ == "__main__":
    iterations = 0
    whileFlag = 0
    maxCost = 17000
    minCost = 4000
    while(whileFlag == 0):

        print("HELP ME UMBC SCORE")
        print(costscorecalculator(maxCost,minCost,UMBCCOST))
        print("HELP ME HOPKINS SCORE")
        print(costscorecalculator(maxCost,minCost,HYPOTHETICALHOPKINSCOST))

        if( ( costscorecalculator(maxCost,minCost,UMBCCOST) == UMBCSCORE) and (costscorecalculator(maxCost,minCost,HYPOTHETICALHOPKINSCOST) == HOPKINSSCORE)):
            print("MAX COST ", maxCost, "\nMIN COST ", minCost)
            whileFlag=1


        
        elif (iterations == MAXITERATIONS):
            print(MAXITERATIONS)
            whileFlag = 1
            print("DEAD")


        else:
            maxCost = round(maxCost-.01,2)
            print("maxcost ", maxCost)
            minCost = round(minCost+.01,2)
            print("mincost ", minCost)
            iterations+=1