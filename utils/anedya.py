import json
import requests
import time
import uuid
import streamlit as st
import pandas as pd
import pytz  # Add this import for time zone conversion
import random
from datetime import datetime, timedelta

nodeId = ""
apiKey = ""


def anedya_config(NODE_ID, API_KEY) -> bool:
    # Simulate always successful config for testing/demo
    global nodeId, apiKey
    nodeId = NODE_ID or "SIMULATED_NODE_ID"
    apiKey = API_KEY or "SIMULATED_API_KEY"
    return True


def anedya_sendCommand(COMMAND_NAME, COMMAND_DATA):
    # Simulate sending a command
    print(f"Simulated sendCommand: {COMMAND_NAME} with data {COMMAND_DATA}")


def anedya_setValue(KEY, VALUE):
    # Simulate setting a value
    print(f"Simulated setValue: {KEY} = {VALUE}")
    class Response:
        text = '{"success": true}'
    return Response()


def anedya_getValue(KEY):
    # Simulate getting a value
    print(f"Simulated getValue: {KEY}")
    return [True, 1]


@st.cache_data(ttl=15, show_spinner=False)
def anedya_get_latestData(param_variable_identifier: str) -> list:
    # Simulate latest data
    value = round(random.uniform(20, 30), 2)
    timestamp = int(time.time())
    return [value, timestamp]


def anedya_getData(
    param_variable_identifier: str,
    param_from: int,
    param_to: int,
    param_aggregation_interval_in_minutes: float,
) -> list:
    # Simulate aggregated data with different ranges for temperature and humidity
    data = {}
    current = param_from
    if param_variable_identifier == "temperature":
        min_val, max_val = 22, 26
    elif param_variable_identifier == "humidity":
        min_val, max_val = 20, 50
    else:
        min_val, max_val = 20, 30  # default range
    while current <= param_to:
        ts = str(current)
        data[ts] = [
            {
                "timestamp": current,
                "aggregate": round(random.uniform(min_val, max_val), 2)
            }
        ]
        current += int(param_aggregation_interval_in_minutes * 60)
    response_message = json.dumps({"data": data, "success": True})
    res_code = 200
    return [response_message, res_code]


@st.cache_data(ttl=60, show_spinner=False)
def fetchHumidityData(
    param_from, param_to, param_aggregation_interval_in_minutes=10
) -> pd.DataFrame:
    response_message = anedya_getData(
        "humidity",
        param_from=param_from,
        param_to=param_to,
        param_aggregation_interval_in_minutes=param_aggregation_interval_in_minutes,
    )
    if response_message[1] == 200:
        data_list = []
        response_data = json.loads(response_message[0]).get("data")
        for timeStamp, value in reversed(response_data.items()):
            for entry in reversed(value):
                data_list.append(entry)
        if data_list:
            df = pd.DataFrame(data_list)
            df["Datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            local_tz = pytz.timezone("Asia/Kolkata")
            df["Datetime"] = (
                df["Datetime"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
            )
            df.set_index("Datetime", inplace=True)
            df.drop(columns=["timestamp"], inplace=True)
            chart_data = df.reset_index()
        return chart_data
    else:
        print(response_message[0])
        value = pd.DataFrame()
        return value


@st.cache_data(ttl=60, show_spinner=False)
def fetchTemperatureData(
    param_from=0, param_to=0, param_aggregation_interval_in_minutes=10
) -> pd.DataFrame:
    response_message = anedya_getData(
        "temperature",
        param_from=param_from,
        param_to=param_to,
        param_aggregation_interval_in_minutes=param_aggregation_interval_in_minutes,
    )
    if response_message[1] == 200:
        data_list = []
        response_data = json.loads(response_message[0]).get("data")
        for timeStamp, value in reversed(response_data.items()):
            for entry in reversed(value):
                data_list.append(entry)
        if data_list:
            df = pd.DataFrame(data_list)
            df["Datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            local_tz = pytz.timezone("Asia/Kolkata")
            df["Datetime"] = (
                df["Datetime"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
            )
            df.set_index("Datetime", inplace=True)
            df.drop(columns=["timestamp"], inplace=True)
            chart_data = df.reset_index()
        return chart_data
    else:
        print(response_message[0])
        value = pd.DataFrame()
        return value


@st.cache_data(ttl=50, show_spinner=False)
def anedya_getDeviceStatus():
    # Simulate device status
    print("Simulated getDeviceStatus")
    return [True, 1]
