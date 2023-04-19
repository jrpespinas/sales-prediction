import pandas as pd
from sklearn.preprocessing import StandardScaler

from ..domain.store import StoreSchema


class StorePreprocessor:
    def __init__(self):
        self.store_df = self.__get_store_details()
        self.scaler = self.__initialize_scaler()

    def __get_store_details(self):
        """Read store details into a DataFrame"""
        df = pd.read_csv("data_store/store.csv")
        return df

    def __get_unscaled_training_data(self):
        """Read store details into a DataFrame"""
        df = pd.read_csv("data_store/x_train_unscaled.csv")
        df = df.drop(df.columns[0], axis=1)
        return df

    def __initialize_scaler(self):
        """initialize standard scaler"""
        x_train_unscaled = self.__get_unscaled_training_data()

        scaler = StandardScaler()
        scaler.fit_transform(x_train_unscaled)
        return scaler

    def __merge_data(self, store: StoreSchema):
        """Merge input data to store details"""
        input_data = pd.DataFrame([store.dict()], index=[0])
        df = input_data.merge(self.store_df, how="inner", on="Store")
        return df

    def __impute_promo_2_data(self, df: pd.DataFrame):
        """Remove NaN values from Promo2 data"""
        values = {
            'Promo2SinceWeek': 0,
            'Promo2SinceYear': 0,
            'PromoInterval': 0
        }
        df = df.fillna(value=values)
        return df

    def __impute_competition_distance(self, df):
        """Remove NaN values from Competition data"""
        df.loc[
            df.CompetitionDistance.isna(),
            'CompetitionOpenSinceMonth'
        ] = df.CompetitionOpenSinceMonth.fillna(0)

        df.loc[
            df.CompetitionDistance.isna(),
            'CompetitionOpenSinceYear'
        ] = df.CompetitionOpenSinceYear.fillna(0)

        df['CompetitionDistance'] = df.CompetitionDistance.fillna(0)
        return df

    def __handle_competition_since_open(self, df):
        """Assign competition open date to earliest open date of the Store"""
        df['Date'] = pd.to_datetime(df['Date'])
        df['SalesMonth'] = df['Date'].dt.month
        df['SalesYear'] = df['Date'].dt.year

        # Get earliest open of the store, then remove Date column
        # NOTE: coincidentally all the stores opened on the same date
        # hence 'Store' == 1
        open_year = df[(df['Store'] == 1) & df['Open'] == 1].Date.min().year
        open_month = df[(df['Store'] == 1) & df['Open'] == 1].Date.min().month
        df.drop(columns=['Date'], inplace=True)

        values = {
            'CompetitionOpenSinceMonth': open_month,
            'CompetitionOpenSinceYear': open_year
        }
        df = df.fillna(value=values)
        return df

    def __categorical_encoding(self, df):
        """Enforce one hot encoding on non-ordinal data,
        use ordinal-encoding on Assortment"""
        # Store type are a, b, c, an d
        df["StoreType_a"] = 1 if df["StoreType"][0] == 'a' else 0
        df["StoreType_b"] = 1 if df["StoreType"][0] == 'b' else 0
        df["StoreType_c"] = 1 if df["StoreType"][0] == 'c' else 0
        df["StoreType_d"] = 1 if df["StoreType"][0] == 'd' else 0

        # Categories are 0, a, b, and c
        df["StateHoliday_0"] = 1 if df["StateHoliday"][0] == '0' else 0
        df["StateHoliday_a"] = 1 if df["StateHoliday"][0] == 'a' else 0
        df["StateHoliday_b"] = 1 if df["StateHoliday"][0] == 'b' else 0
        df["StateHoliday_c"] = 1 if df["StateHoliday"][0] == 'c' else 0

        df['Assortment'].replace({'a': 1, 'b': 2, 'c': 3}, inplace=True)

        df.drop(columns=['StateHoliday', 'StoreType'], inplace=True)
        return df

    def __handle_promo_interval(self, df):
        """Convert interval to number of promos"""
        df['NumberOfPromosPerYear'] = df.PromoInterval.str.count(',') + 1
        df["NumberOfPromosPerYear"].fillna(0, inplace=True)
        df.drop(columns=['PromoInterval'], inplace=True)
        return df

    def __convert_data_types(self, df):
        """Convert all floats into integers, except competition distance"""
        m = df.select_dtypes('float64')
        df[m.columns[1:]] = df[m.columns[1:]].astype(int)
        return df

    def __reindex_df(self, df):
        """Sort column by names"""
        df = df.reindex(sorted(df.columns), axis=1)
        return df

    def __scale_input(self, df):
        """Scale input based on training data"""
        df = pd.DataFrame(self.scaler.transform(df), columns=df.columns)
        return df

    async def convert(self, store: StoreSchema):
        df = self.__merge_data(store)
        df = self.__impute_promo_2_data(df)
        df = self.__impute_competition_distance(df)
        df = self.__handle_competition_since_open(df)
        df = self.__categorical_encoding(df)
        df = self.__handle_promo_interval(df)
        df = self.__convert_data_types(df)
        df = self.__reindex_df(df)
        X = self.__scale_input(df)
        return X
