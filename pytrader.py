from yahoo_fin.stock_info import *
from twelvedata import TDClient
import time
from datetime import datetime

#twelvedata.com

with open("ApiKey.txt") as f:
    apiKey = f.readline()

# Test out for best results
overSoldLine = 47
overBoughtLine = 59

# Dynamic Variables
boughtState = False
stocksOwned = 0
bal = 1000
percentageRiskPerTrade = 0.2

while True:

    try:
        #initialize
        td = TDClient(apikey=apiKey)
        ts = td.time_series(
            symbol="CAD/USD",
            interval="1min",
            outputsize=1,
            timezone="America/New_York"
        )
        #Return JSON
        df = ts.with_rsi().as_json()
        print("------------------------------------------------")
        print("                                                ")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)
        print("CAD:USD Live Price: ", get_live_price("CADUSD=X"))
        print("AAPL live price: ", get_live_price("AAPL"))
        print("S&P 500 live price: ", get_live_price("SPY"))
        print("Rsi: ")
        print(df[0]["rsi"])
        
        rsiNumber = float(df[0]["rsi"])
        #Buying Method
        if boughtState is not True:
            if float(rsiNumber) <= overSoldLine:
                boughtState = True

                amountSharesBought = float((bal+0.02) / float(get_live_price("CADUSD=X")))
                bal = float(bal - (amountSharesBought*float(get_live_price("CADUSD=X"))))

        #Selling Method
        if boughtState == True:
            if float(rsiNumber) >= overBoughtLine:
                bal = float(bal + (amountSharesBought * float(get_live_price("CADUSD=X"))))
                amountSharesBought = 0
                boughtState = False
        print("Bal: ")
        print(bal)
        time.sleep(300)
    except:
        print("Request limit reached/Error occured")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)
        break


