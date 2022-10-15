from ast import IsNot
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd
from typing import Optional

def fetch_data(url: str):
    """
    Fetch data from an API using get method on given URL.

    Parameters
    ----------
    url : string, a API end point to fetch data from.
    """

    return requests.get(url).content

def extract_data(data: str):
    """
    Extract the obsdimension and obsvalue values from the given xml string.

    Parameters
    ----------
    data : string, xml string to extract the data of obsdimension and obsvalue.
    """

    root = ET.fromstring(data)
    soup = BeautifulSoup(data, features="lxml")
    extracted_data=[]
    for item in soup.find_all('generic:obs'):
        extracted_data.append([item.find("generic:obsdimension").get('value'), float(item.find("generic:obsvalue").get('value'))])
    df = pd.DataFrame(data=extracted_data, columns=("TIME_PERIOD", "OBS_VALUE"))
    return df

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    """
    Fetch and return the data for exchange rate based on given source and target currency.

    Parameters
    ----------
    source : string, currency code of source currency, example EUR, GBP etc
    target : string, currency code to convert the currency, example EUR, GBP etc.
    """

    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.' + source + '.' + target + '.SP00.A?detail=dataonly'
    return extract_data(fetch_data(url))

def get_raw_data(identifier: str) -> pd.DataFrame:
    """
    Fetch and return the raw data for based on given identifier.

    Parameters
    ----------
    identifier : string, an identifier to fetch the raw data. 
            example: M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N
    """

    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/BP6/' + identifier + '?detail=dataonly'
    return extract_data(fetch_data(url))

def get_data(identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame:
    """
    Print the data based on provided identifier and target currency.

    If curreny is not given, DataFrame is returned as it is.

    Parameters
    ----------
    identifier : string, an identifier to fetch the raw data. 
            example: M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N
    target : string, currency code to convert the currency, example EUR, GBP etc.
    """

    df1 = get_raw_data(identifier)
    df_result=pd.DataFrame({})
    df_result["TIME_PERIOD"]=df1["TIME_PERIOD"]
    if target_currency is not None:
        df2 = get_exchange_rate(target_currency)
        df_result["OBS_VALUE"]=df1["OBS_VALUE"] * df2["OBS_VALUE"]
    else:
         df_result["OBS_VALUE"] = df1["OBS_VALUE"]

    print(df_result.to_string(index=False))

get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")    

