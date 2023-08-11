"""
Purpose: Illustrate addition of continuous information. 
"""

import asyncio
from datetime import datetime
from pathlib import Path
import os

import pandas as pd
from collections import deque
from dotenv import load_dotenv

from fetch import fetch_from_url
from util_logger import setup_logger

logger, log_filename = setup_logger(__file__)


def get_API_key():
    load_dotenv()
    key = os.getenv("OPEN_WEATHER_API_KEY")
    return key


def lookup_lat_long(location):
    """Return the latitude and longitude for the given location."""
    locations_dictionary = {
        "Seattle WA": {"latitude": 47.606209, "longitude": -122.332069},
        "Portland OR": {"latitude": 45.512230, "longitude": -122.658722},
        "San Francisco CA": {"latitude": 32.715760, "longitude": -117.163820},
        "San Diego CA": {"latitude": 32.715736, "longitude": -117.161087},
        "Phoenix AZ": {"latitude": 33.448200, "longitude": -111.072578},
    }
    answer_dict = locations_dictionary[location]
    lat = answer_dict["latitude"]
    long = answer_dict["longitude"]
    return lat, long


async def get_temperature_from_openweathermap(lat, long):
    logger.info("Calling get_temperature_from_openweathermap for {lat}, {long}}")
    api_key = get_API_key()
    open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=imperial"
    logger.info(f"Calling fetch_from_url for {open_weather_url}")
    result = await fetch_from_url(open_weather_url, "json")
    logger.info(f"Data from openweathermap: {result}")
    temp_F = result.data["main"]["temp"]
    return temp_F


def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Location", "Latitude", "Longitude", "Time", "Temp_F"]
    )
    df_empty.to_csv(file_path, index=False)


async def update_csv_location():
    """Update the CSV file with the latest location information."""
    logger.info("Calling update_csv_location")
    try:
        locations = ["Seattle WA", "Portland OR", "San Francisco CA", "San Diego CA", "Phoenix AZ"]
        update_interval = 60
        total_runtime = 15 * 60
        num_updates = 20
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("reactive_location.csv")

        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  
            for location in locations:
                lat, long = lookup_lat_long(location)
                new_temp = await get_temperature_from_openweathermap(lat, long)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                new_record = {
                    "Location": location,
                    "Latitude": lat,
                    "Longitude": long,
                    "Time": time_now,
                    "Temp_F": new_temp,
                }
                records_deque.append(new_record)

                df = pd.DataFrame(records_deque)

            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving temperatures to {fp}")

            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_location: {e}")