import Libraries.Stock as st
import Libraries.Transactions as tr

print("Reading data...")
maxDays = -1
[Stocks,Days] = st.readData("Stocks",maxDays)
print("Dataset ready.")


#7763.076499999969 <--For 5 days
money = 1
period = Days[:]
print("Lets make this "+str(money)+" $ to millions!\nCalculating transactions...")
[trns,money,diagram] = tr.becomeRicher(Stocks,Days,money)
print("Transactions calculations completed.")
print("Profits:",money,"$")
#for t in trns:
    #print("Day:",t["day"]," is for stock:",t["stock"],"{",t["type"],",",t["profit"],"$}")
    #print(t)

#WriteResults
base_name = "results_large_"
print("Writing results in file:",base_name+str(maxDays)+".txt")
output = open(base_name+str(maxDays)+".txt","w")
#output.write(str(len(transactions)*2))
output.write(str(len(trns)))
for t in trns:
    output.write("\n")
    output.write(t[0]+" "+t[2]+" "+t[1]+" "+str(t[5]))
output.close()

#Draw Diagram
tr.DrawDiagram(diagram[0],diagram[1],diagram[2])

print("LifeHack fount. GG fellow millioner! Cyia in Malbs!")