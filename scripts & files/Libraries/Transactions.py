#Library to host all transsaction logic
import datetime
import time
#Find best stock to trade on date
#for close-open values
def findBestSellOnDay(Stocks,date):
    transaction = ["","",-1,-1]  #Stock Type,Profit,opening
    best_stock = ""
    for s in Stocks:
        [type,profit,opening] = s.getIntraDayWin(date)
        if profit > transaction[2] and type != "":
            transaction[0] = s.stock
            transaction[1] = type
            transaction[2] = profit
            transaction[3] = opening
            best_stock = s
    return [best_stock,[transaction[0],transaction[1],transaction[2],transaction[3]]]

#Find best stock to trade on period of days
#for close-open values
def findBestSellOnPeriod(Stocks,period):
    transactions = []
    #Find for all stocks their profit in designated period
    for s in Stocks:
        #result = s.getProfitPeriod(period) #[buyData,sellData,profit]
        result = s.getProfitPeriodSmart(period) #[buyData,sellData,profit]
        if result != [] :
            transactions.append(
                {
                    "stock": s,
                    "buy": result[0],
                    "sell": result[1],
                    "profit": result[2]
                }
            )
    #Sort them
    #print("Hodlers are:",transactions)
    return sorted(transactions, key=lambda i: i['profit'])


#Returns the Best Stock with best possible profits
#for close-open values
def findBestIncreaseDaily(Stocks):
    max = ["","",-1,"" ]    #Date,Type,Profit,Stock
    for s in Stocks:
        [date,type,profit] = s.getBiggestDayAccimulation()
        if profit > max[2]:
            max[0] = date
            max[1] = type
            max[2] = profit
            max[3] = s.stock
    return max

#Get all best Profits (or loses) for all stocks
#for close-open values
def getAllBestIncreaseDaily(Stocks):
    data = []
    for s in Stocks:
        [day,type,profit] = s.getBiggestDayAccimulation()
        data.append(
            {
                "stockname":s.stock,
                "day": day,
                "type": type,
                "profit": profit
            }
        )
    return sorted(data, key=lambda i: i['profit'])

def becomeRich(Stocks,Days,money):
    transactions = []
    portfolio={}

    for d in Days:
        #print(d,"{",money," $}")
        #For every stock in day d calculate if it can be bought
        availableStocks = []
        for s in Stocks:
            price = s.getOpenPrice(d)
            if price != -1 and price <= money:
                availableStocks.append(s)
        #Find best one out of these
        best_stock,sell = findBestSellOnDay(availableStocks,d)
        #print("Best for day:",d,"is:",best)
        if sell[0] != "":
            #print("Best sell of day ",d,"is:",sell)
            buy = sell.copy()

            #Calculate Buy amount
            available_volume = best_stock.buyAmmount(d,money)
            buyamount = 1
            #MakeBuy command
            buy[1]= "buy-open"
            transactions.append([d]+buy+[buyamount])

            #Add to portfolio
            #print("Buying:",buyamount)
            if best_stock.stock not in portfolio.keys():
                portfolio[best_stock.stock] = buyamount
            else:
                portfolio[best_stock.stock] = portfolio[best_stock.stock]+buyamount
            #Update Money
            money -= buy[3]*buyamount
            #print("Buy: ",buy[3],"x",buyamount," || Money:",money," $")

            #Make Sell command
            sellamount = buyamount

            transactions.append([d]+sell+[sellamount])
            #Update portfolio
            portfolio[best_stock.stock] = portfolio[best_stock.stock]-sellamount
            if portfolio[best_stock.stock] == 0:
                portfolio.pop(best_stock.stock)
            #Update Money
            money += (buy[3]+sell[2])*sellamount
            #print("Sell: ",(buy[3]+sell[2]),"x",sellamount," || Money:",money," $")

    return [transactions,money]

def hodl(Stocks,period,money):
    hodl_stocks = findBestSellOnPeriod(Stocks,period)
    for i in range(len(hodl_stocks)-1,0,-1):
        if hodl_stocks[i]["buy"][2] <= money:
            return hodl_stocks[i]
    return None

def buyStock(stock,buyData,money,available_transactions):
    # Calculate Buy amount
    #print("Buy stock for:",stock.stock,"At buy data:",buyData)
    available_volume = stock.buyAmmount(buyData[0], money)
    buyamount = available_volume
    if buyamount > available_transactions:
        buyamount = available_transactions
    # print("I will buy",buyamount,"from ",best_stock.stock)
    # MakeBuy command
    return [buyData[0]] + [buyData[1]] + [buyamount]


def becomeRicher(Stocks,Days,money):
    transactions = []
    portfolio={}    #"stockname":[ammount,type,sellStats]

    #For diagram
    dates_label = []
    balance_data = []
    portfolio_data = []

    hodl_steps = 1000
    hodl_incr = 3
    hodl_bind = 20/100 #Bind 20% of money
    hodl_perdiod = -1#
    hodl_threshold = 3 #Designates how many times a hodl profit should be better than an intraDay transaction

    for i in range(len(Days)):
        d = Days[i]
        """#ExportYear
        year = d.split('-')
        if year[0] not in dates_label:
            dates_label.append(year[0])
        """
        #Add date for diagram
        dates_label.append(d)
        #print(d,"{",money," $}")
        #For every stock in day d calculate if it can be bought
        #print("Day:",d,"\nProfolio:",portfolio)
        availableStocks = []
        for s in Stocks:
            price = s.getOpenPrice(d)
            #print("Price:",price)
            if price != -1 and price <= money:
                availableStocks.append(s)
        #Find best one out of these for intraDay
        best_stock,sell = findBestSellOnDay(availableStocks,d)

        available_transactions = 0
        for p in portfolio:
            available_transactions += portfolio[p][0]
        available_transactions += 1

        #print("Date:",d,"|Availalbe:",available_transactions)
        #print(portfolio)
        #if d == "1981-08-10":
         #   input("Enter sth:")
        #available_transactions = len(portfolio)+1   #TOCHANGE: I can buy +1 based on total hodlings

        #print("Day:",d,"\tStartDay available traansactions:",available_transactions)
        #Decide if we go for hodl
        hodl_stock = None
        if money*hodl_bind > hodl_steps:
            if hodl_perdiod != -1:
                hodl_stock = hodl(availableStocks,Days[i:i+hodl_perdiod],money*hodl_bind)
            else:
                hodl_stock = hodl(availableStocks,Days[i:],money*hodl_bind)
            if hodl_stock != None and hodl_stock['profit'] <= 0:
                hodl_stock = None



        #Check if daily gives more profit
        if hodl_stock != None:
            #print("Hold is:",hodl_stock["stock"].stock,"with profit:",hodl_stock['profit'])
            #print("Data regarding are:",hodl_stock['profit'] > sell[2]*hodl_threshold)
            #print("Since threshold is:",sell[2]*hodl_threshold)
            #print("Sell is:",sell)
            if sell[0] != "" and hodl_stock['profit'] > sell[2]*hodl_threshold:
                hodl_steps = hodl_steps*hodl_incr   #Increase next goal
                #Buy stock
                transaction = buyStock(hodl_stock["stock"],hodl_stock["buy"],money*hodl_bind,available_transactions)
                #print("Decided to hodl stock:",hodl_stock["stock"].stock," and bought at transaction",transaction)
                #print("Buy transaction data",hodl_stock["buy"])
                #print("Sell transaction data",hodl_stock["sell"])
                available_transactions -= transaction[2]
                #print("New available traansactions:",available_transactions)
                #print("LOLOappending:",[hodl_stock["buy"][0],hodl_stock["stock"].stock,hodl_stock["buy"][1],hodl_stock["profit"],hodl_stock["buy"][2],[transaction[2]]]) #typeProfitOpening
                transactions.append([hodl_stock["buy"][0],hodl_stock["stock"].stock,hodl_stock["buy"][1],hodl_stock["profit"],hodl_stock["buy"][2],transaction[2]])
                # Add to portfolio
                if hodl_stock["stock"].stock not in portfolio.keys():
                    portfolio[hodl_stock["stock"].stock] = [transaction[2],"hodl",hodl_stock["sell"],hodl_stock["profit"],hodl_stock["buy"][2]]
                else:
                    portfolio[hodl_stock["stock"].stock][0] = portfolio[hodl_stock["stock"].stock][0] + transaction[2]
                # Update Money
                money -= hodl_stock["buy"][2] * transaction[2]  # Opening*amount $


        #Perform IntraDay transaction on rest
        #print("Best for day:",d,"is:",best)
        if sell[0] != "" and available_transactions > 0:
            #print("Best sell of day ",d,"is:",sell)
            buy = sell.copy()

            #Calculate Buy amount
            available_volume = best_stock.buyAmmount(d,money)
            buyamount = available_volume
            if buyamount > available_transactions:
                buyamount = available_transactions
                available_transactions -=buyamount
            """
            if buyamount >1:
                print("I CAN BUY MORE:::",buyamount)
                print("Current portfolio:")
                print(portfolio)
            if d == "1981-08-10":
                input("Enter sth:")
            """
            #print("I will buy",buyamount,"from ",best_stock.stock)
            #MakeBuy command
            buy[1]= "buy-open"
            transactions.append([d]+buy+[buyamount])

            #Add to portfolio
            #print("Buying:",buyamount)
            if best_stock.stock not in portfolio.keys():
                portfolio[best_stock.stock] = [buyamount,"intraDay",""]
            else:
                portfolio[best_stock.stock][0] = portfolio[best_stock.stock][0]+buyamount
            #Update Money
            money -= buy[3]*buyamount   #Opening*amount $
            #print("Buy: ",buy[3],"x",buyamount," || Money:",money," $. Bought in total for:",buy[3]*buyamount)

            #Make Sell command
            sellamount = buyamount
            #print("appending:",[d]+sell+[sellamount])
            transactions.append([d]+sell+[sellamount])
            #Update portfolio
            portfolio[best_stock.stock][0] = portfolio[best_stock.stock][0]-sellamount
            if portfolio[best_stock.stock][0] == 0:
                portfolio.pop(best_stock.stock)
                #print("Removing from portfolio")
            #Update Money
            money = money + (buy[3]+sell[2])*sellamount
            #print("Sell: ",(buy[3]+sell[2]),"x",sellamount," || Money:",money," $ and sell for total:",(buy[3]+sell[2])*sellamount)

        #Check if hodlers need to be sold
        if len(portfolio) > 0:
            #print("Porfotlio:",portfolio)
            clone = portfolio.copy()
            for p in clone:
                #print("Cheking",p,"sell on", portfolio[p][2][0],"Current date:",d)
                #print("CHECK2:",portfolio[p][2][0]<=d)
                if p[1] == "hodl" and portfolio[p][2][0]>=d:
                    #print("Must sell",p,"since sell status is",portfolio[p][2][0])
                    #current_date = date_1 + datetime.timedelta(days=hodl_perdiod)
                    transactions.append([portfolio[p][2][0], p, portfolio[p][2][1], portfolio[p][3], portfolio[p][2][2], portfolio[p][0]])
                    portfolio.pop(p)
                    money += ( portfolio[p][4]+portfolio[p][2][2])*portfolio[p][0]
            clone.clear()
        #print("Portfolio is:",portfolio)

        #End of day add to label
        balance_data.append(money)
        portfolio_assets = 0
        for p in portfolio:
            portfolio_assets += portfolio[p][0]
        portfolio_data.append(portfolio_assets)

    #Finally sell all hodlings if any left
    if len(portfolio) > 0:
        clone = portfolio.copy()
        for p in clone:
            #print("Must sell", p)
            #print("Appending:",[portfolio[p][2][0], p, portfolio[p][2][1],portfolio[p][3], portfolio[p][2][2],portfolio[p][0]])
            transactions.append( [portfolio[p][2][0], p, portfolio[p][2][1],portfolio[p][3], portfolio[p][2][2],portfolio[p][0]])
            money += ( portfolio[p][4]+portfolio[p][2][2])*portfolio[p][0]
            portfolio.pop(p)
        clone.clear()

    #print("Portfolio is:", portfolio)
    return [transactions,money,[dates_label,balance_data,portfolio_data]]


#Return 0 if equal
#1 if date1 bigger
#-1 if date2 bigger
def compareDates(date1,date2):
    newdate1 = time.strptime(date1, "%Y-%m-%d")
    newdate2 = time.strptime(date2, "%Y-%m-%d")
    if newdate2 == newdate1:
        return 0
    elif newdate1 > newdate2:
        return 1
    elif newdate1 < newdate2:
        return -1



def DrawDiagram(dates,balance,portfolio):
    import matplotlib.pyplot as plt
    """
    print(dates)
    print(balance)
    print(portfolio)
    print(len(dates))
    print(len(balance))
    print(len(portfolio))
    """
    labels = dates
    bal_means = balance
    port_means = portfolio
    width = 0.99  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, bal_means, width, label='Balance')
    ax.bar(labels, port_means, width, bottom=bal_means,label='Portfolio')

    ax.set_ylabel('Assets')
    ax.set_title('Date')
    ax.legend()

    plt.show()





