import pandas as pd


def streamBody_to_CSV_tips(obj):

    return pd.read_csv(obj['Body'], usecols = ['tip_amount'])

def mean_pandas(df):
    return df["tip_amount"].mean()

def rows_number(df):
    return df["tip_amount"].count()