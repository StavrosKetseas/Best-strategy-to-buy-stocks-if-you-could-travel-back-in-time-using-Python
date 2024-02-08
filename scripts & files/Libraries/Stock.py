import os
from datetime import datetime
import time

#Stocks Class
class Stock:
    # Date,Open,High,Low,Close,Volume,OpenInt
    def __init__(self,stock):
        self.stock = stock
        self.data =[]
        self.bestTransaction= ["","",-1] #Date,Type,Profit

    #Add data to the stock
    def addData(self ,date ,open ,high ,low ,close ,volume ,openInt):
        self.data.append(
            {
                "date": date,
                "open": float(open),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": float(volume),
                "openInt": int(openInt)
            }
        )

    #Returns IntraDayTransaction upon open and close
    #Returns [Type,Profit,OpenPrice]
    #If not fount returns ["",0,0]
    def getIntraDayWin(self, date):
        for d in self.data:
            #if self.compareDates(d["date"],date) == 0:
            if d["date"]== date:
                #Remove for no searching allover
                #self.data.remove(d)
                #Check if we can buy
                if d["volume"] == 0 or d["volume"]<10:
                    return ["",0,0]
                #Check if high > close
                if d["high"] > d["close"]:
                    return ["sell-high",d["high"] - d["open"],d["open"]]
                else:
                    return ["sell-close",d["close"] - d["open"],d["open"]]
            elif d["date"] > date:
                break
        return ["",0,0]

        # Returns IntraDayTransaction upon open and close
        # Returns [Type,Profit,OpenPrice]
        # If not fount returns ["",0,0]
    def getIntraDayWinNEWNOTWORK(self, date):
        if len(self.data) == 0:
            return ["", 0, 0]
        d = self.data[0]
        if d["date"]==date:
            # Remove for no searching allover
            #self.data.remove(self.data[0])

            if d["volume"] == 0 or d["volume"] < 10:
                return ["", 0, 0]
            # Check if high > close
            if d["high"] > d["close"]:
                return ["sell-high", d["high"] - d["open"], d["open"]]
            else:
                return ["sell-close", d["close"] - d["open"], d["open"]]
        return ["", 0, 0]

    #Returns the difference between high and low in period
    #Return [[date,buy_type,buy_price],[date,sell_type,sell_price],profit]
    #Returns >0 if win
    #Returns <0 if lose
    #Returns 0 if not fount
    def getProfitPeriod(self, period):
        startDate = period[0]
        start_value = ["","",-1]
        endDate = period[len(period)-1]
        end_value = ["","",-1]
        for d in self.data:
            if startDate <= d["date"]  and start_value[0] == "":
                if d["open"] < d["low"]:
                    start_value[0] = d["date"]
                    start_value[1] = "buy-open"
                    start_value[2] = d["open"]
                else:
                    start_value[0] = d["date"]
                    start_value[1] = "buy-low"
                    start_value[2] = d["low"]
            if (d["date"]>endDate and end_value[0] == "") or (d==self.data[len(self.data)-1] and end_value==""):
                if d["close"] < d["high"]:
                    end_value[0] = d["date"]
                    end_value[1] = "sell-high"
                    end_value[2] = d["high"]
                else:
                    end_value[0] = d["date"]
                    end_value[0] = "sell-close"
                    end_value[1] = d["close"]
                break

        reply = [start_value,end_value,end_value[2]-start_value[2]]
        if start_value[0] == "":
            reply = []
        #print("Buy Reply:",start_value)
        #print("Sell Reply:",end_value)
        return reply

    # Returns the difference between high and low in period
    # Find lowest point and next highest Point
    # Return [[date,buy_type,buy_price],[date,sell_type,sell_price],profit]
    # Returns >0 if win
    # Returns <0 if lose
    # Returns 0 if not fount
    #Need further adjustmet to be bind in period. This now will go until the end of data
    def getProfitPeriodSmart(self, period):
        #Find Minimum Value of starting period
        min_tr = ["","",-1]
        for d in self.data:
            if d["date"] < period[0]:
                continue
            if d["date"] == period[0]:
                values = [d["low"],d["open"],d["close"]]
                values.sort()
                min_tr[0] = d["date"]
                min_tr[2] = values[0]
                if values[0] == d["low"]:
                    min_tr[1] = "buy-low"
                elif values[0] == d["open"]:
                    min_tr[1] = "buy-open"
                elif values[0] == d["close"]:
                    min_tr[1] = "buy-close"
                break
            if d["date"] > period[0]:
                break
        if min_tr[2] == -1:
            return []
        #Find next peak
        max_tr = ["", "", -1]
        for d in self.data:
            if d["date"] < min_tr[0]:
                continue
            if d["date"] > period[0]:
                values = [d["high"],d["open"],d["close"]]
                values.sort()
                if values[len(values)-1] > max_tr[2]:
                    max_tr[0] = d["date"]
                    max_tr[2] = values[len(values)-1]
                    if values[len(values)-1] == d["high"]:
                        max_tr[1] = "sell-high"
                    elif values[len(values)-1] == d["open"]:
                        max_tr[1] = "sell-open"
                    elif values[len(values)-1] == d["close"]:
                        max_tr[1] = "sell-close"
            reply = [min_tr, max_tr, max_tr[2] - min_tr[2]]
            #print("~~~")
            #print(reply)
            #print(max_tr[2] - min_tr[2])
            if max_tr[2] - min_tr[2] <= 0:
                reply = []
            #print("Buy Reply:",reply)
            return reply

    #Returns the best Profit for daily results
    def getBiggestDayAccimulation(self):
        if self.bestTransaction[2] != -1:
            return self.bestTransaction
        maxTransaction = ["",-1,0]    #Type,Profit,Opening
        maxDay = ""
        for d in self.data:
            transaction = self.getIntraDayWin(d["date"])
            if transaction[1] > maxTransaction[1]:
                maxTransaction = transaction
                maxDay = d["date"]

        self.bestTransaction = [maxDay,maxTransaction[0],maxTransaction[1],maxTransaction[2]]
        return self.bestTransaction

    #Returns the openning price of a date
    def getOpenPrice(self,date):
        for d in self.data:
            if d["date"]==date:
                return d["open"]
            elif d["date"]>date:
                break
        return -1
    #Returns the volume of a price
    def getVolume(self,date):
        for d in self.data:
            if d["date"]==date:
                return d["volume"]
            elif d["date"]>date:
                break
        return -1

    #Returns the ammount of stocks that can be bought at a date
    def buyAmmount(self,date,money):
        amount = 0
        for d in self.data:
            if d["date"]==date:
                amount = int(money // d["open"])
                canbuy = int(d["volume"] * 10/100)
                if amount > canbuy:
                    amount = canbuy
            elif d["date"]>date :
                break
        return amount

    #Printning
    def __str__(self):
        datastr = ">>" + self.stock + ":\n"
        datastr += "Date\t\tOpen\tHigh\tLow\t\tClose\tVolume\topenInt\n"
        for d in self.data:
            datastr += d["date"] + "\t" + str(d["open"]) + "\t" + str(d["high"]) + "\t" + str(d["low"]) + "\t" + str(d["close"]) + "\t" + str(d["volume"]) + "\t" + str(d["openInt"]) + "\n"
        return datastr

    #Return 0 if equal
    #1 if date1 bigger
    #-1 if date2 bigger
    def compareDates(self,date1,date2):
        newdate1 = time.strptime(date1, "%Y-%m-%d")
        newdate2 = time.strptime(date2, "%Y-%m-%d")
        if newdate2 == newdate1:
            return 0
        elif newdate1 > newdate2:
            return 1
        elif newdate1 < newdate2:
            return -1

#Read all files
#Folder is the path of where the stocks data are saved
#Stockes is the table to Fill
#MaxDays designate how many days to read
def readData(folder,maxDays):
    Stocks=[]
    days = []
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f:
            name = filename.split('.')
            st = Stock(name[0].upper())
            count = 0
            for l in f:
                ls = l.split(",")
                if ls[0] == '\n' or ls[0] == "Date":  # Skip headers
                    continue
                st.addData(ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6])
                count += 1
                if maxDays!= -1 and count >= maxDays:
                    break
                if ls[0] not in days:
                    days.append(ls[0])
            Stocks.append(st)
            f.close()
    days.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    return [Stocks,days]


