"""
Store the last 15 minutes of stock values for several companies

Information is updated once per minute.
"""

import asyncio
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from collections import deque

from util_logger import setup_logger
from fetch import fetch_from_url

logger, log_filename = setup_logger(__file__)

def lookup_ticker(company):
    stocks_dictionary = {
        "Nordstrom Inc": "JWN",
        "Lululemon Athletica Inc": "LULU",
        "Starbucks Corporation": "SBUX",
        "NIKE Inc": "NKE",
        "Amazon.com Inc": "AMZN",
    }
    ticker = stocks_dictionary[company]
    return ticker


async def get_stock_price(ticker):
    logger.info(f"Calling get_stock_price for {ticker}")
    stock_api_url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
    logger.info(f"Calling fetch_from_url for {stock_api_url}")
    result = await fetch_from_url(stock_api_url, "json")
    logger.info(f"Data from yahoo finance: {result}")
    price = result.data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
    return price


def init_stock_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Company", "Ticker", "Time", "Price"]
        )
    df_empty.to_csv(file_path, index=False)


async def update_csv_stock():
    logger.info("Calling update_csv_stock")
    try:
        companies = [
        "Nordstrom Inc",
        "Lululemon Athletica Inc",
        "Starbucks Corporation",
        "NIKE Inc",
        "Amazon.com Inc",
        ]
        update_interval = 60
        total_runtime = 15 * 60
        num_updates = 50
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("reactive_stock.csv")

        if not os.path.exists(fp):
            init_stock_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):
            for company in companies:
                ticker = lookup_ticker(company)
                new_price = await get_stock_price(ticker)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Company": company,
                    "Ticker": ticker,
                    "Time": time_now,
                    "Price": new_price,
                }
                records_deque.append(new_record)

            df = pd.DataFrame(records_deque)

            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving prices to {fp}")

            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_stock: {e}")