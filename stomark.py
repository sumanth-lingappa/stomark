import pandas as pd
from yahoofinancials import YahooFinancials
# import json
from datetime import datetime, timedelta

# Input
assets = [  # these IDs are as per YahooFinance website
    "INFY.BO",
    "INFY.NS",
    "TCS.NS",
    "TCS.BO",
]
DMA_DAYS = "50"  # last 50 days


# -------------------------------------------
yahoo_financials = YahooFinancials(assets)

today = datetime.today()
end = today.strftime("%Y-%m-%d")
start = (today - timedelta(days=int(DMA_DAYS))).strftime("%Y-%m-%d")

stockdata = yahoo_financials.get_historical_price_data(start_date=start, end_date=end, time_interval="daily")


custom_data = {}
for company, cdata in stockdata.items():
    custom_data[company] = {}
    tmp = []
    for daily_stock_data in cdata["prices"]:
        tmp.append(daily_stock_data["close"])
    custom_data[company]["mean"] = round(sum(tmp) / len(tmp), 2)
    custom_data[company]["Days>DMA" + DMA_DAYS] = len(
        [above_avg for above_avg in tmp if above_avg > custom_data[company]["mean"]]
    )
    custom_data[company]["Last10days>DMA" + DMA_DAYS] = len(
        [above_avg for above_avg in tmp[-10:] if above_avg > custom_data[company]["mean"]]
    )

# with open('sto.json', 'w') as f:
#     json.dump(stockdata, f)

pd_dict = {}
pd_dict["Company"] = custom_data.keys()
pd_dict["DMA" + DMA_DAYS] = []
pd_dict["Days>DMA" + DMA_DAYS] = []
pd_dict["Last10days>DMA" + DMA_DAYS] = []
for k, v in custom_data.items():
    pd_dict["DMA" + DMA_DAYS].append(v["mean"])
    pd_dict["Days>DMA" + DMA_DAYS].append(v["Days>DMA" + DMA_DAYS])
    pd_dict["Last10days>DMA" + DMA_DAYS].append(v["Last10days>DMA" + DMA_DAYS])

df = pd.DataFrame(pd_dict)
print(df)

input("Enter any key to exit! ")
