from bs4 import BeautifulSoup
import requests
import cloudscraper
scraper = cloudscraper.create_scraper()
import math

URLBASE = "https://results.bajasae.net/"
ENDURANCEGRIDPAGE = "https://results.bajasae.net/EnduranceGrid.aspx"
TEAMURLBASE = "https://results.bajasae.net/MyResults.aspx?carnum="
STATICSEXTENTION = "&tab=statics"
DYNAMICSEXTENTION = "&tab=dynamics"
ENDURANCEDYNAMICS = "&tab=endurance"




class team:
    def __init__(self, name=0, carnumber=0, cost=0,design=0,sales=0,accel=999,manuv=999,sus=999,hill=[999,999],end=0):
        self.name = name # this is actually car number
        self.carnumber = carnumber # this is actually name
        self.cost = cost
        self.design = design
        self.sales = sales
        self.accel = accel
        self.manuv = manuv
        self.sus = sus
        self.hill = hill
        self.end = end
    


if __name__ == "__main__":
    listofteams = []
    page = scraper.get(ENDURANCEGRIDPAGE)
    soup = BeautifulSoup(page.content, "html.parser")
    allteams = soup.find_all('td')
    
    # for i in range(1, len(allteams), 5):
    for i in range(1, 50, 5):
        listofteams.append(team(allteams[i].text))
        listofteams[len(listofteams)-1].carnumber = allteams[i+1].text
    # all existing teams on the endurance grid.
    for i in listofteams:
        print(i.name)
        print(i.carnumber)
    # start collecting each teams statics score
    for i in listofteams:
        # ALL OF COST 
        print(TEAMURLBASE + i.name + STATICSEXTENTION)
        page = scraper.get(TEAMURLBASE + i.name + STATICSEXTENTION)
        soup = BeautifulSoup(page.content, "html.parser")
        costreport = soup.find('span', id='MainContent_lblCostReportScore')
        costreport = float(costreport.text)
        costprototype = soup.find('span', id='MainContent_lblCostEvalScore')
        costprototype = float(costprototype.text)
        listofteams[listofteams.index(i)].cost = costreport + costprototype
        print(listofteams[listofteams.index(i)].cost)
        # END OF COST
        # DESIGN START
        designPenalty = soup.find('span', id='MainContent_lblDesignReportPenalty')
        #print(designPenalty)
        if (designPenalty.text == "Not Yet Available"):
            designPenalty = "0.00"
            designPenalty = float(designPenalty)
        else:
            designPenalty = float(designPenalty.text)
            designScore = soup.find('span', id='MainContent_lblDesignEvalScore')
            designScore = float(designScore.text)
            listofteams[listofteams.index(i)].design = designScore - designPenalty
            print(listofteams[listofteams.index(i)].design)
        # END OF DESIGN
        #SALES START
        salesPenalty = soup.find('span', id='MainContent_lblPresentationPenalty')
        print(salesPenalty.text)
        if (salesPenalty.text == "Not Yet Available"):
            print("AHHHH")
            salesPenalty = "0.00"
            print(salesPenalty)
            salesPenalty = float(salesPenalty)
        else:
            salesPenalty = float(salesPenalty.text)
        salesScore = soup.find('span', id='MainContent_lblPresentationEvalScore')
        if (salesScore.text == "Not Yet Available"):
            salesScore = "0.00"
            salesScore = float(salesScore)
        else:
            salesScore = float(salesScore.text)
        listofteams[listofteams.index(i)].sales = salesScore - salesPenalty
        print(listofteams[listofteams.index(i)].sales)
        #END OF SALES
        #END OF STATICS
        #DYNAMICS START
        
        accel = 0
        manuv = 0
        sus = 0
        hill = 0


        print(TEAMURLBASE + i.name + DYNAMICSEXTENTION)
        page = scraper.get(TEAMURLBASE + i.name + DYNAMICSEXTENTION)
        soup = BeautifulSoup(page.content, "html.parser")
        #ACCEL START
        allData = soup.find_all('tr') # all rows.
        # find highest accel score
        for row in allData:
            if "Acceleration" in row.text:
                print("ACCEL")
                accel = row.find_all('td')
                accel = float(accel[3].text)
                print(accel)
                if accel < listofteams[listofteams.index(i)].accel:
                    listofteams[listofteams.index(i)].accel = accel
                print(listofteams[listofteams.index(i)].accel)
            #END OF ACCEL

            #MANUV START
            if "Maneuverability" in row.text:
                print("MANUV")
                manuvdata = row.find_all('td')
                manuv = float(manuvdata[3].text)
                if (manuv < listofteams[listofteams.index(i)].manuv) & (manuvdata[1].text != "DQ"):
                    listofteams[listofteams.index(i)].manuv = manuv
                print(listofteams[listofteams.index(i)].manuv)
            #END OF MANUV
            
            #SUS START
            if "Suspension" in row.text:
                print("SUS")
                sus = row.find_all('td')
                sus = float(sus[3].text)
                if (sus < listofteams[listofteams.index(i)].sus) & (sus != 0):
                    listofteams[listofteams.index(i)].sus = sus
                print(listofteams[listofteams.index(i)].sus)
            #END OF SUS

            #HILL START
            if "Hill Climb" in row.text:
                print("HILL")
                hill = row.find_all('td')
                print(hill)
                # GROUP ONE HILL CLIMB PEOPLE
                if (int(math.floor(float(hill[3].text))) != 0 ):
                    hill = [float(hill[3].text),1]
                    if hill < listofteams[listofteams.index(i)].hill:
                        listofteams[listofteams.index(i)].hill = hill
                    print(listofteams[listofteams.index(i)].hill)
                # GROUP TWO CLIMB PEOPLE
                else:
                    hill = [float(hill[7].text.split()[0]), 2]
                    #hill = [float(hill[7].text),2]
                    if hill < listofteams[listofteams.index(i)].hill:
                        listofteams[listofteams.index(i)].hill = hill
                    print(listofteams[listofteams.index(i)].hill)
            #END OF HILL

            #END OF DYNAMICS
    
        #START OF ENDURANCE
        # page = scraper.get(TEAMURLBASE + i.name + ENDURANCEDYNAMICS)
        # soup = BeautifulSoup(page.content, "html.parser")
        # endurance = soup.find('span', id="MainContent_lblEndLapCount")
        # endurance = int(endurance.text)
        # listofteams[listofteams.index(i)].end = endurance
        # print(listofteams[listofteams.index(i)].end)
        #END OF ENDURANCE
# END OF DATA COLLECTION.



# DATA MANIPULATION.

# ACCEL
tmin = 9999 # fastest
tmax = 0 # slowest
for i in listofteams:
    if i.accel < tmin:
        tmin = i.accel
    if i.accel > tmax:
        tmax = i.accel
print("ACCEL THINGS MAX")
print(tmax) # slowest score
print(tmin) # fastest score

for i in listofteams:
    if i.accel == 999:
        i.accel = 0
    else:
        trun = i.accel
        print(tmax-trun)
        print(tmax-tmin)
        if (i.accel) == tmin:
            i.accel = 70
        else:
            i.accel = 70 * ( (tmax - trun) / (tmax - tmin) )
        print(i.accel)
# END OF ACCEL

# MANUV


manuvtmax = 0 # slowest time
manuvtmin = 0 # fastest time

for i in listofteams:
    print("MANUV TIME")
    print(i.manuv)
    if i.manuv < manuvtmin:
        manuvtmin = i.manuv
    if i.manuv > manuvtmax:
        manuvtmax = i.manuv

print("MANUV STUFF")
print("MAX" + str(manuvtmax))
print("MIN" + str(manuvtmin))


for i in listofteams:
    if i.manuv == 999:
        i.manuv = 0
    else:
        trun = i.manuv
        if (manuvtmax - trun) == 0:
            i.manuv = 70
        else:
            i.manuv = 70 * ( (manuvtmax - trun) / (manuvtmax - manuvtmin) )
    print(i.manuv)




# END OF MANUV

# SUS
tmin = 0
tmax = 0

for i in listofteams:
    if i.sus < tmin:
        tmin = i.sus
    elif i.sus > tmax:
        tmax = i.sus
for i in listofteams:
    if i.sus == 999:
        i.sus = 0
    else:
        trun = i.sus
        if (tmax - trun) == 0:
            i.sus = 70
        else:
            i.sus = 70 * ( (tmax - trun) / (tmax - tmin) )
        print(i.sus)
# END OF SUS

# HILL
tmin = 10000
trun = 0
mingroup1 = 10000
dcourse = 459.00

# GROUP ONE SCORING | GETTING MIN TIME
for i in listofteams:
    if i.hill[1] == 1:
        if(tmin > i.hill[0]):
            tmin = i.hill[0]

print("TMIN" + str(tmin))

# GROUP ONE CALCULATING SCORES
for i in listofteams:
    if i.hill[1] == 1:
        i.hill[0] = 70 * (tmin/i.hill[0])
        print("HELP ME PELASE")
        print(i.hill[0])
    if (i.hill[0] < mingroup1):
        print("THE THING THAT FUCKS STUFF UP" + i.name)
        mingroup1 = i.hill[0]
        print("GROUP 1 MIN SCORE")
        print(mingroup1)
# END GROUP ONE SCORES

print ("MIN GROUP ONE" + str(mingroup1))

# GROUP TWO SCORES
for i in listofteams:
    if i.hill[1] == 2:
        i.hill[0] = mingroup1 * (i.hill[0]/dcourse)
        print("GROUP 2 HILL CLIMB" + str(i.hill[0]))
    if i.hill[1] == 999:
        i.hill[0] = 0
# GROUP TWO END 

# HILL CLIMB END



# ENDURANCE
lowmax = 0
lowend = 0
for i in listofteams:
    if i.end < lowend:
        lowend = i.end
    if i.end > lowmax:
        lowmax = i.end
for i in listofteams:
    if i.end == 0:
        i.end = 0
    else:
        i.end = 400 * ( (i.end - lowend) / (lowmax - lowend) )
        print(i.end)
# END OF ENDURANCE

import pandas as pd
columns = ["Car Number", "Name", "Cost", "Design", "Sales", "Acceleration", "Maneuverability", "Suspension", "Hill Climb", "Endurance"]
data = pd.DataFrame(columns=columns)
for i in listofteams:
    data = data._append({"Car Number": i.name, "Name": i.carnumber, "Cost": i.cost, "Design": i.design, "Sales": i.sales, "Acceleration": i.accel, "Maneuverability": i.manuv, "Suspension": i.sus, "Hill Climb": i.hill[0], "Endurance": i.end}, ignore_index=True)
data.to_excel("bajasae.xlsx")



