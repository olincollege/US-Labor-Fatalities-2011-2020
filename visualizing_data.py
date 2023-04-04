"""
    Plot and visualize data from csv
"""
from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd


def load_data(data_file):
    """
    Loads data as df from data_file

    Args:
        data_file: string of file name/path

    Returns:
        dataframe from csv
    """
    data = pd.read_csv(data_file)
    data.columns.values[0] = "State"

    return data


def plot_all_data(data):
    """
    Plots all data

    Args:
        data: dataframe with data to plot
    """
    years = [int(year) for year in data if year != "State"]

    for i in range(len(data)):
        single_state_data = [int(value) for value in data.iloc[i][1:]]
        plt.plot(years, single_state_data, label=data.iloc[i][0])

    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Number of Fatalities")
    plt.title("Fatalities Per Year in Each State")
    plt.show()


def plot_mean_data(data, plot_row, plot_col, plot_num):
    """
    Plots mean of data by year

    Args:
        data: dataframe with data to plot
        plot_row: int num rows in subplot
        plot_col: int num cols in subplot
        plot_num: int which plot
    """
    years = [int(year) for year in data if year != "State"]

    mean_data = [mean(data[str(year)]) for year in years]

    plt.subplot(plot_row, plot_col, plot_num)
    plt.plot(years, mean_data)
    plt.xlabel("Year")
    plt.ylabel("Number of Fatalities")
    plt.title("Average Fatalities Per Year Across States")


def plot_extremes(data, plot_row, plot_col, plot_num):
    """
    Plots max & min data by year

    Args:
        data: dataframe with data to plot
        plot_row: int num rows in subplot
        plot_col: int num cols in subplot
        plot_num: int which plot
    """
    years = [int(year) for year in data if year != "State"]

    max_data = [max(data[str(year)]) for year in years]
    min_data = [min(data[str(year)]) for year in years]

    plt.subplot(plot_row, plot_col, plot_num)
    plt.plot(years, max_data, label="max")
    plt.plot(years, min_data, label="min")
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Number of Fatalities")
    plt.title("Max and Min Fatalities Per Year")


def plot_state(data, state_name, plot_row, plot_col, plot_num):
    """
    Plots data for a single state

    Args:
        data: dataframe with data to plot
        state_name: string with state name
        plot_row: int num rows in subplot
        plot_col: int num cols in subplot
        plot_num: int which plot
    """

    years = [int(year) for year in data if year != "State"]

    for row in csv_data.iterrows():
        if row[1][0] == state_name:
            state_data = row[1][1:]
            break

    plt.subplot(plot_row, plot_col, plot_num)
    plt.plot(years, state_data)
    plt.xlabel("Year")
    plt.ylabel("Number of Fatalities")
    plt.title("Fatalities Per Year in " + state_name)


csv_data = load_data("data.csv")

subplot_rows, subplot_cols = 1, 3
plot_all_data(csv_data)
plot_mean_data(csv_data, subplot_rows, subplot_cols, 1)
plot_extremes(csv_data, subplot_rows, subplot_cols, 2)
plot_state(csv_data, "Massachusetts", subplot_rows, subplot_cols, 3)
plt.show()