"""
imports
"""

import matplotlib.pyplot as plt
import pandas as pd

"""
files - inputs and outputs
Data source: https://data.nasa.gov/resource/eva.json
"""
input_dir = "./eva-data.json"
output_dir = "./eva-data.csv"
graph_file = "./cumulative_eva_graph.png"

"""
read and prune with pandas
"""
eva_df = pd.read_json(input_dir, convert_dates=["date"], encoding="ascii")
eva_df["eva"] = eva_df["eva"].astype(float)
eva_df.dropna(axis=0, subset=["duration", "date"], inplace=True)

eva_df.to_csv(output_dir, index=False, encoding="utf-8")

eva_df.sort_values("date", inplace=True)

"""
summation and plotting
"""
eva_df["duration_hours"] = (
    eva_df["duration"].str.split(":").apply(lambda x: int(x[0]) + int(x[1]) / 60)
)
eva_df["cumulative_time"] = eva_df["duration_hours"].cumsum()
plt.plot(eva_df["date"], eva_df["cumulative_time"], "ko-")
plt.xlabel("Year")
plt.ylabel("Total time spent in space to date (hours)")
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
