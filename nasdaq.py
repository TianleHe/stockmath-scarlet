# Tianle Tyler He, July 8th 2020

from numpy import genfromtxt
import os
import time

class StockList:

    def __init__(self, path):
        """
        Allows for easy access to the data stored in the CSV files in a number of functions.
        :param path: The file path from the current directory to the directory containing data.
        """
        self.path = path

    def clone_data(self):
        """
        Converts all stock data files into a list of type Stock.
        :return: A list of objects of type Stock.
        """
        clone_time = time.time()

        list_of_stock = []
        list_of_stock_files, num_of_stock = self.listall()
        list_of_stock_names = self.getname()

        for j in range(0, num_of_stock):
            dat = genfromtxt((self.path + list_of_stock_files[j]), delimiter=',', dtype=None)
            res = [[]]
            for i in range(1, len(dat)):  # Using loops instead of map allows me to skip the labels.
                res.append([self.unformat_date(dat[i][0]),
                            self.unformat_accounting(dat[i][1]),
                            self.unformat_volume_int(dat[i][2]),
                            self.unformat_accounting(dat[i][3]),
                            self.unformat_accounting(dat[i][4]),
                            self.unformat_accounting(dat[i][5])])

            temp_stock = Stock(res, list_of_stock_names[j])
            list_of_stock.append(temp_stock)

        print("Database cloned to RAM, reformatted, and loaded in", round(time.time()-clone_time, 2), "seconds.")

        return list_of_stock

    def getname(self):
        """
        Produces a list of all stock ticker names, assumes files are correctly formatted as (TICKER).csv
        :return: a list of strings of all stock tickers of files in the directory.
        """

        listoffile, numfiles = self.listall()
        listofname = []

        for filename in listoffile:
            listofname.append(filename.rpartition('.')[0])

        return listofname

    def listall(self):
        """
        Produces a list of all CSV files found in the provided directory and the number of files.
        :return: a list of all file names in directory and the number of files in directory.
        """

        list_of_stock_name = []
        with os.scandir(self.path) as entries:
            for entry in entries:
                if entry.name.rpartition('.')[-1] == 'csv':
                    list_of_stock_name.append(entry.name.rpartition('<DirEntry ')[2])  # Keeps only 'XXXXX.csv'

        return list_of_stock_name, len(list_of_stock_name)

    def unformat_accounting(self, val):
        """
        Takes an excel accounting value and produces a float.
        :param val: Value of type any, although in this class, generally values in accounting format from MS Excel.
        :return: The value formatted as a float.
        """
        if val == b' N/A':
            return b' N/A'
        else:
            return float(val[2:])

    def unformat_date(self, val):
        """
        Converts an excel date formatted as MM/DD/YYYY to a single integer YYYYMMDD that can be used for easy sorting.
        :param val: Values of type Excel Date.
        :return: An integer equivalent in form YYYYMMDD
        """
        days = int(val[3:][:2])
        months = int(val[:2])
        years = int(val[6:])

        return int(1e4 * years + 1e2 * months + days)

    def unformat_volume_int(self, val):
        """
        Converts an MS Excel Number value to a Python int value.
        :param val: Values of type Excel Number
        :return: The equivalent Python int value.
        """
        if val == b' N/A':
            return b' N/A'
        else:
            return int(val)


class Stock:

    def __init__(self, data, name):
        """
        Information defining a stock.
        :param data: data from csv files reformatted from StockList.clone_data
        :param name: the ticker name of the stock.
        """

        self.name = name

        self.date = [data[i][0] for i in range(1, len(data))]
        self.close = [data[i][1] for i in range(1, len(data))]
        self.volume = [data[i][2] for i in range(1, len(data))]
        self.open = [data[i][3] for i in range(1, len(data))]
        self.high = [data[i][4] for i in range(1, len(data))]
        self.low = [data[i][5] for i in range(1, len(data))]

    def find_date_index(self, date):
        """
        Finds the index in the data where the date occurs.
        :param date: The desired date. (YYYYMMDD)
        :return: int (index) or False if this date is not in the dataset.
        """

        for i in range(0, len(self.date)):
            if self.date[i] == date:
                return i
            else:
                return False

    def on_date_close(self, date):
        """
        The closing share price of the stock on the provided date in USD. Method made separate for convenience.
        :param date: The trading day when the requested information takes place. (YYYYMMDD)
        :return: float (share price) or False if no information is available for the provided date.
        """
        match = self.find_date_index(date)
        return False if match is False else self.close[match]

    def on_date_volume(self, date):
        """
        The transaction volume of the stock on the provided date. Method made separate for convenience.
        :param date: The trading day when the requested information takes place. (YYYYMMDD)
        :return: int (volume) or False if no information is available for the provided date.
        """
        match = self.find_date_index(date)
        return False if match is False else self.volume[match]


    def on_date_open(self, date):
        """
        The share price at market open of the stock on the provided date. Method made separate for convenience.
        :param date: The trading day when the requested information takes place. (YYYYMMDD)
        :return: float (share price) or False if no information is available for the provided date.
        """
        match = self.find_date_index(date)
        return False if match is False else self.open[match]

    def on_date_high(self, date):
        """
        The maximum value the share price reaches on public trading for that day. Method made separate for convenience.
        :param date: The trading day when the requested information takes place. (YYYYMMDD)
        :return: float (share price) or False if no information is available for the provided date.
        """
        match = self.find_date_index(date)
        return False if match is False else self.high[match]

    def on_date_low(self, date):
        """
        The minimum value the share price reaches on public trading for that day. Method made separate for convenience.
        :param date: The trading day when the requested information takes place. (YYYYMMDD)
        :return: float (share price) or False if no information is available for the provided date.
        """
        match = self.find_date_index(date)
        return False if match is False else self.low[match]

