import pandas as pd
import numpy as np
import timeit

class SebLoad:
    def __init__(self, db_path, fund_names, min_days):
        self._fund_names = fund_names
        self._path = db_path
        self._min_days = min_days

    def _read_file(self, path, fund_name):
        filename = "{0}/{1}.csv".format(path, fund_name)
        df = pd.read_csv(filename)
        return df

    def _set_index_date(self, df):
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index("date")
        return df

    def _remove_duplicates(self, df):
        df = df[~df.index.duplicated()]
        return df

    def _remove_strange_values(self, df):
        df = df.dropna()
        df = df[df.quote != 0]
        return df

    def _add_fund(self, funds, df, fund_name):
        df.name = fund_name   
        funds[fund_name] = df

    def _add_change(self, df):
        df['change'] = df.quote.pct_change()
        df['since_start'] = df.quote / df.quote.iloc[0]

    def _adjust_fund_remake(self, df):
        contains_id_nbr = df.id.apply(lambda x: np.isreal(x)).all()
        if not contains_id_nbr:
            return
        diff = df.id.diff()
        diff = diff.dropna()

        change = df.quote.pct_change()
        fund_remakes = diff[diff != 0]
        for index, row in fund_remakes.iteritems():
            #print(index, change[index])
            updated_rows = df[index:].quote / (1 + change[index])
            df.update(updated_rows)

    def _adjust_fund_abnormal(self, df):
        change = df.quote.pct_change()
        abnormal_change = change[change < -0.1]
        for date_index, percent_change in abnormal_change.iteritems():
            #print(index, row)
            updated_rows = df[date_index:].quote / (1 + percent_change)
            df.update(updated_rows)
    
    def _add_sma_10(self, df):
        ten_month = 10 * 30
        rolling = df.quote.rolling(ten_month)
        df['sma10'] = rolling.mean()

    def _do_operations_on_dataset(self, df):
        df = self._set_index_date(df)
        df = self._remove_duplicates(df)
        df = self._remove_strange_values(df)
        self._adjust_fund_remake(df)
        self._adjust_fund_abnormal(df)
        self._add_change(df)
        self._add_sma_10(df)
        return df

    def _load_single_fund(self, fund_name):
        df = self._read_file(self._path, fund_name)
            
        height, _ = df.shape
        if height < self._min_days:
            return None
        
        df = self._do_operations_on_dataset(df)
        return df

    def execute(self):
        funds = {}
        for fund_name in self._fund_names:
            df = self._load_single_fund(fund_name)
            if df is None:
                # if fund contains less than minimum days skip it
                continue
            
            self._add_fund(funds, df, fund_name)
        
        return funds