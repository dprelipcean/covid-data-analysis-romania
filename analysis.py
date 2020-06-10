"""Analysis plots for COVID data in Romania."""

import json
import pandas as pd

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def read_data(file_name="data/date_09_iunie_la_18_52.json"):
    """Read data file."""
    with open(file_name, encoding="latin-1") as f:
        data = json.load(f)
    return data


def main():
    """Perform reading, analysis, curating and plotting."""
    data = read_data()

    # Initialize Lists
    days_list = list()
    cases_list_suceava = list()

    number_infected = list()
    number_cured = list()
    number_deceased = list()

    daily_infected = list()
    daily_cured = list()
    daily_deceased = list()

    old_value_infected = 0
    old_value_cured = 0
    old_value_deceased = 0

    for value, key in data["historicalData"].items():
        try:
            cases_list_suceava.append(data["historicalData"][value]["countyInfectionsNumbers"]["SV"])
            days_list.append(value)

            number_infected.append(data["historicalData"][value]['numberInfected'])
            number_cured.append(data["historicalData"][value]['numberCured'])
            number_deceased.append(data["historicalData"][value]['numberDeceased'])

            new_value_infected = data["historicalData"][value]['numberInfected']
            daily_infected.append(abs(new_value_infected - old_value_infected))
            old_value_infected = data["historicalData"][value]['numberInfected']

            new_value_cured = data["historicalData"][value]['numberCured']
            daily_cured.append(abs(new_value_cured - old_value_cured))
            old_value_cured = data["historicalData"][value]['numberCured']

            new_value_deceased = data["historicalData"][value]['numberDeceased']
            daily_deceased.append(abs(new_value_deceased - old_value_deceased))
            old_value_deceased = data["historicalData"][value]['numberDeceased']

        except KeyError:
            continue

    # Curate data
    days_list.reverse()
    cases_list_suceava.reverse()
    cases_list_suceava_filtered = savgol_filter(cases_list_suceava, 11, 2)

    number_infected.reverse()
    number_cured.reverse()
    number_deceased.reverse()

    daily_infected.append(daily_infected[-1])
    daily_infected.reverse()
    daily_infected.pop(-1)

    daily_cured.append(daily_cured[-1])
    daily_cured.reverse()
    daily_cured.pop(-1)

    daily_deceased.append(daily_deceased[-1])
    daily_deceased.reverse()
    daily_deceased.pop(-1)

    # Plot data
    df = pd.DataFrame({'data1': daily_infected, 'data2': daily_cured, 'data3': daily_deceased}, index=days_list)
    df.plot(kind='bar', stacked=True)
    plt.legend(['Infectati', 'Recupertati', 'Decedati'])
    plt.show()

    plt.plot(days_list, cases_list_suceava)
    plt.plot(days_list, cases_list_suceava_filtered)
    plt.show()

    plt.plot(days_list, number_infected)
    plt.plot(days_list, number_cured)
    plt.plot(days_list, number_deceased)
    plt.show()

    plt.plot(days_list, daily_infected)
    plt.plot(days_list, daily_cured)
    plt.plot(days_list, daily_deceased)
    plt.show()


if __name__ == "__main__":
    main()
