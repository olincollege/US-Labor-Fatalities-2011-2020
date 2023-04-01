from csv import reader as csv_reader
from keys import BLS_key
import requests
import json
import pandas as pd

# This file is to store all series ID segments and their meanings in
# dictionaries to make the data acquisition more understandable
def make_state_dict(state_dict_url):
    """
    creates a dictionary from a url with state id info

    inputs:
        state_dict_url: str
            url that leads to a list of states and their 2 digit codes

    returns:
        state_dict: dict
            dictionary that maps states to their 2 digit numbers
    """

    # string w states separated from their ids with \t, each separated with \n
    states_string = ((requests.get(state_dict_url)).content).decode()

    # list of each <state id> + "\t" + <state name>
    state_id_list = []
    for string in states_string.split("\n")[1:]:
        state_id_list.append(string.strip("\r"))

    # dict with state names mapping to state ids
    state_id_dict = {}
    for item in state_id_list:
        if item.count("\t") == 1:
            state_id_dict[item.split("\t")[1]] = item.split("\t")[0]
    return state_id_dict


state_dict = make_state_dict("https://download.bls.gov/pub/time.series/sm/sm.state")


def create_all_state_ids(state_idx_dict, sample_series_id):
    """
    creates a dictionary that maps state names to series IDs

    inputs:
        state_dict: dict
            maps str state names to their 2 digit numbers
        sample_series_id: str
            series identifier which will later access the API to a particular dataset

    returns:
        series_ids_dict: dict
            names of states mapped to series IDs within the same series type
            as sample_series_id
    """

    # finds index of first int in the string of chars & ints
    for idx, character in enumerate(sample_series_id):
        if character.isdigit():
            state_int_index = int(idx)
            break

    # creates dict with state names mappig to series id with proper state id
    series_ids_dict = {}
    for key in state_dict:
        this_state_series = (
            sample_series_id[0:state_int_index]
            + str(state_idx_dict[key])
            + sample_series_id[state_int_index + 2 :]
        )
        series_ids_dict[key] = this_state_series
    return series_ids_dict


series_ids_dict = create_all_state_ids(state_dict, "SMU19197802023800001")


def get_series_json(series_ids_dict, start_year, end_year, api_key):
    """
    call BLS API with series ids and return data in specified timeframe

    inputs:
        series_ids_dict: dict
            names of states mapped to series IDs within the same series type
            as sample_series_id
        timeframe: lst
            2 item list: beginning year, end year
        api_key: str
            api key to access BLS database

    returns:
        series_dict: dict
            dictionary with nested dictionaries and lists. includes all
            data values for all timeframes and series called
    """

    # creates list of state names from states.csv file
    with open("states.csv", "r") as states_file:
        state_strings_list = list(csv_reader(states_file, delimiter=","))[0]

    # creates list of series ids only for states in state_strings_list
    active_series_list = []
    for state_string in state_strings_list:
        active_series_list.append(series_ids_dict[state_string])

    headers = {"Content-type": "application/json"}
    data = json.dumps(
        {
            "seriesid": active_series_list,
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": api_key,
        }
    )

    # API CALL: MAX 200 PER DAY
    json_data = requests.post(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/", data=data, headers=headers
    )

    # converts json object to dict and returns
    return json_data.json()


dict_data = get_series_json(series_ids_dict, 2000, 2010, BLS_key)


def dict_to_df(series_dict):
    """
    creates a df object from series_dict with each state as a column of values

    inputs:
        series_dict: dict
            dict object which contains series values for all timeframes

    returns:
        series_df: pandas dataframe
            accessible table which contains data from all states in all times
    """
    df = pd.DataFrame(series_dict)
    return df


data_frame_data = dict_to_df(dict_data["Results"]["series"][14]["data"])


def df_to_csv(series_df):
    """
    creates a csv from a dataframe

    inputs:
        series_df: pandas dataframe
            accessible table which contains data from all states in all times

    returns:
        none (creates a csv file)
    """
    with open("data.csv", "wb") as csv_file:
        series_df.to_csv(csv_file)


df_to_csv(data_frame_data)
