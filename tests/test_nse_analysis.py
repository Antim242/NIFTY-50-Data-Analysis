import pytest
import pandas as pd
from nse_analysis import fetch_nifty50_data, analyze_data

def test_fetch_nifty50_data_returns_dataframe():
    df = fetch_nifty50_data()
    assert df is not None, "Expected a DataFrame but got None"
    assert isinstance(df, pd.DataFrame), "Expected type DataFrame"
    assert not df.empty, "DataFrame should not be empty"
    assert 'symbol' in df.columns, "'symbol' column should be present"
    assert 'pChange' in df.columns, "'pChange' column should be present"

def test_analyze_data_returns_expected_outputs():
    df = fetch_nifty50_data()
    gainers, losers, below_high, above_low = analyze_data(df)

    assert isinstance(gainers, pd.DataFrame)
    assert isinstance(losers, pd.DataFrame)
    assert isinstance(below_high, pd.DataFrame)
    assert isinstance(above_low, pd.DataFrame)

    assert len(gainers) <= 5
    assert len(losers) <= 5
