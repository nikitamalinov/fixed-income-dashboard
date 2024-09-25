from multiprocessing import process
import streamlit as st
import pandas as pd
import yfinance as yf

import matplotlib.pyplot as plt
from typing import List
import requests
import os
from components.Bonds import yield_calculation


# @st.cache_data
def get_asset_prices() -> List[str]:
    tickers = [
        "IRX",
        "ZN=F",
        "US10Y",
        None,  # Not easily accessible via yfinance
        None,  # Need a specialized API for this
        None,  # Need a specialized API
        None,  # Requires a specialized API
        None,  # Requires a specialized API
        "PFF",  # Example ETF for preferred stock
        "HYG",  # Example ETF
        "EMB",  # Example ETF
    ]
    asset_price_list: List[str] = []
    for i, ticker in enumerate(tickers):
        if ticker is not None:
            try:
                hist = yf.download(ticker, period="1d", interval="1m")
                current_price = hist["Close"].iloc[-1]
                asset_price_list.append(current_price)
            except Exception as e:
                print(e)
                asset_price_list.append("")
        else:
            asset_price_list.append("")
    return asset_price_list


# asset_price_list = get_asset_prices()
st.title("Fixed-income investment calculator")
st.write("The following is based on a California resident")


yield_calculation.show()

st.write("TODO - Add historical prices and selection for each bond type")


data = {
    "Type": [
        "Treasury bills",
        "Treasury notes",
        "Treasury bonds",
        "Savings Bonds",
        "CDs",
        "Money-market funds",
        "Mortgage debt",
        "Municipal bonds",
        "Preferred stock",
        'High-yield ("junk") bonds',
        "Emerging-markets debt",
    ],
    # "Price": ["3.78", "101.09"],
    # "Yield": ["3.93", "3.74"]
    # total return
    # return after taxes
    "Maturity": [
        "Less than 1 year",
        "1 to 10 years",
        "10 to 30 years",
        "Up to 30 years",
        "One month to 5 years",
        "397 days or less",
        "1 to 30 yrs",
        "1 to 30 yrs or more",
        "Indefinite",
        "Seven to 20 yrs",
        "Up to 30 yrs",
    ],
    "Risk of default": [
        "Extremely Low",
        "Extremely Low",
        "Extremely Low",
        "Extremely Low",
        "Very Low, insured up to $100,000",
        "Very Low",
        "Generally moderate but can be high",
        "Generally moderate but can be high",
        "High",
        "High",
        "High",
    ],
    "Risk if interest rates rise": [
        "very low",
        "Moderate",
        "High",
        "Very low",
        "Low",
        "Low",
        "Moderate to High",
        "Moderate To High",
        "High",
        "Moderate",
        "Moderate",
    ],
    "Exempt from most state income taxes": [
        "Yes",
        "Yes",
        "Yes",
        "Yes",
        "No",
        "No",
        "No",
        "No",
        "No",
        "No",
        "No",
    ],
    "Exempt from Federal income taxes": [
        "No",
        "No",
        "No",
        "No",
        "No",
        "No",
        "No",
        "Yes",
        "No",
        "No",
        "No",
    ],
    "Benchmark": [
        "90-day",
        "5-year and 10-year",
        "30-year",
        "EE bond Series bought after May 1995",
        "1-year national average",
        "Taxable money market average",
        "Lehman Bros. MBS Index",
        "National Long-Term Mutual Fund avgerage",
        "None",
        "Merill Lynch High Yield Index",
        "Emerg. Markets Bond Fund",
    ],
}

df = pd.DataFrame(data)
df.index = df.index + 1


st.write(
    'Inspired by Jason Zweig "The Wide World of Bonds" table from The Intelligent Investor pg 108-109'
)
st.dataframe(df, use_container_width=True)
