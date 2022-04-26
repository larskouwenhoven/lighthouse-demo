import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import pathlib
import os

dir_name = os.path.abspath(os.path.dirname(__file__))
location = os.path.join(dir_name, '../NTA_ACS_2014_2018.gdb')

print(dir_name)
print(location)

nta2 = gpd.read_file(location)
nta = nta2

for index, row in nta.iterrows():  
    neighbors = nta[nta.geometry.touches(row['geometry'])].NTAName.tolist() 
    # neighbors = neighbors.remove(row.NTAName)
    nta.at[index, "my_neighbors"] = ", ".join(neighbors)
    nta.at[index, "my_neighbors"] = neighbors

def generate_scenario(nta_df, size=20, chance=0.5):
    # select the center of impact
    select_nta = nta_df.sample()

    affected_ntas = [select_nta.NTAName.values[0]]

    neighbors = nta[nta.NTAName == affected_ntas[0]].my_neighbors.values[0]

    consider = set(i for i in neighbors)
    # print("Consider", consider)

    # iteratively find neighbors
    while len(affected_ntas) < size:
        # print(len(affected_ntas), "NTAs affected")
        # find neighbors
        if len(consider) == 1:
            draw = 0
        else:
            draw = random.random()

        use = consider.pop()
        
        if draw <= chance:
            affected_ntas.append(use)
            neighbors = nta[nta.NTAName == use].my_neighbors.values[0]
            use_neighbors = [i for i in neighbors if i not in affected_ntas]
            for i in use_neighbors:
                consider.add(i)
    return affected_ntas

affected_ntas = generate_scenario(nta, size=20, chance=0.5)

nta['color_code'] = "#ffffff"
nta['affected'] = "Not affected"

nta.loc[nta.NTAName.isin(affected_ntas), "color_code"] = "#ec0404ff"
nta.loc[nta.NTAName.isin(affected_ntas), "affected"] = "Affected"

affected_ntas_2 = generate_scenario(nta, size=40, chance=0.8)

nta['color_code_2'] = "#ffffff"
nta['affected_2'] = "Not affected"
nta.loc[nta.NTAName.isin(affected_ntas_2), "color_code_2"] = "#ec0404ff"
nta.loc[nta.NTAName.isin(affected_ntas_2), "affected_2"] = "Affected"

affected_ntas_3 = generate_scenario(nta, size=100, chance=0.6)
nta['color_code_3'] = "#ffffff"
nta['affected_3'] = "Not affected"
nta.loc[nta.NTAName.isin(affected_ntas_3), "color_code_3"] = "#ec0404ff"
nta.loc[nta.NTAName.isin(affected_ntas_3), "affected_3"] = "Affected"

# st.set_page_config(layout="wide")

st.title('Lighthouse Technical Demo')

st.write("This interactive technical demonstration" + \
    "allows you to choose one of three scenarios. In each scenario, " +  
    "the severity of the natural disaster increases, and more locations are affected."
)

scenario = st.selectbox("Select a scenario", ['Scenario 1', 'Scenario 2', 'Scenario 3'])


if scenario == 'Scenario 1':
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis("off")
    nta.plot(ax=ax, color=nta['color_code'], legend=True)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0001)
    st.pyplot(fig)
elif scenario == 'Scenario 2':
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis("off")
    nta.plot(ax=ax, color=nta['color_code_2'], legend=True)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0001)
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis("off")
    nta.plot(ax=ax, color=nta['color_code_3'], legend=True)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0001)
    st.pyplot(fig)


