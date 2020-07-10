import nasdaq as nas

hist = nas.StockList('historical_data/')
x = hist.clone_data()
print(x[0].name, x[0].on_date_close(20200707))