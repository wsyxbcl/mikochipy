import os
from pathlib import Path
from collections import OrderedDict

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

class FilelogicError(Exception):
    pass

# class Battery:
#     def __init__(self, )

class CDCtest:
    """
    Charge-Discharge Cycle

    """
    def __init__(self, df):
        self.data = df
    def plot_SC_V(self, cycles):
        cmap = get_cmap('tab10') #TODO find a more proper color solution
        for i, cycle in enumerate(cycles):
            cyc_c_idx = (self.data["Cycle"] == cycle) & (self.data["State"] == "C_CC")
            cyc_d_idx = (self.data["Cycle"] == cycle) & (self.data["State"] == "D_CC")
            plt.plot(self.data[cyc_c_idx]["Specific capacity (mAh/g)"], 
                     self.data[cyc_c_idx]["Voltage (V)"], 
                     label='cycle {}'.format(cycle),
                     color=cmap.colors[i]
                     )
            plt.plot(self.data[cyc_d_idx]["Specific capacity (mAh/g)"], 
                     self.data[cyc_d_idx]["Voltage (V)"], 
                     label='cycle {}'.format(cycle),
                     color=cmap.colors[i]
                     )
        plt.xlabel("Specific capacity (mAh/g)")
        plt.ylabel("Voltage (V)")
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()


def land_to_cdc(filename, mass_am, save_csv=False):
    """
    filename: Path of the LANDdt output file (.xls)
    mass_am: Mass of the active material, unit: g
    Return: CDCtest object
    """
    df = pd.read_excel(filename, usecols=list(range(1, 7)))
    df.columns = ["Time (s)", "Voltage (V)", "Current (A)", "Capacity (mAh)", "State"]
    df["Current (A)"] = df["Current (A)"] / 1000
    df["Specific capacity (mAh/g)"] = df["Capacity (mAh)"] / mass_am
    # Seperate cycles
    # Notice that cycle == 0 refers to the initial state "R"
    cyc_sep = (df["State"] != (df["State"].shift())) & (df["State"] != "R")
    if list(df[cyc_sep == 1]["State"])[0] == "C_CC":
        # A charging-first process
        cyc_sep = cyc_sep & (df["State"] != "D_CC")
    elif list(df[cyc_sep == 1]["State"])[0] == "D_CC":
        # A discharging-first process
        cyc_sep = cyc_sep & (df["State"] != "C_CC")
    else:
        print(list(df[cyc_sep == 1]["Time (s)"])[0])
        print(list(df[cyc_sep == 1]["State"])[0])
        raise FilelogicError("Unexpected process, please check")

    df["Cycle"] = cyc_sep.cumsum()
    if save_csv:
        print("Saving converted dataframe...")
        df.to_csv(filename.with_suffix(".csv"))
        print(filename.with_suffix(".csv"))
    return df

if __name__ == "__main__":
    lro_df = land_to_cdc(Path("./test/LRO.xls"), mass_am = 1)
    lro_cdctest = CDCtest(lro_df)
    lro_cdctest.plot_SC_V([1, 2, 3])