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

st.write("Even in mandatory evacuation areas; during hurricane Sandy, only 40% of the population evacuated. In the case of area where there was no evacuation order, this number was just over 10%. For now, we will assume **15% of people in affected areas evacuate**. We will also devise different scenarios for Lighthouse adoption rates. In a pessimistic scenario, 0.1% of citizens will use Lighthouse. In a realistic scenario, we will find an adoption rate of 5%. In a optimistic scenario, 15% of NYC residents will adopt Lighthouse. ")

st.header("Vehicle ownership")

st.write("One point that renders New York City unique within an American context, is the low vehicle ownership rate. On average, some 40% of the population own a car, but this number is as low as 8% is some areas in Manhattan. The lack of car ownership often makes evacuations more challenging. At the same time, many of those who **do** evacuate using their own vehicle have many empty seats. There is thus an opportunity to more equitably distribute resources here. The map below shows the car ownership rates of different areas in New York City. ")

vehicle_path = os.path.join(dir_name, "../ACSDP5Y2020.DP04_2022-04-22T145843/ACSDP5Y2020.DP04_data_with_overlays_2022-04-22T145824.csv")

vehicle_df = pd.read_csv(vehicle_path, header=1)
veh_available_cols = [
    'Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!1 vehicle available',
    'Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!2 vehicles available',
    'Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!3 or more vehicles available'
]
vehicle_df['total_households_vehicle'] = vehicle_df[veh_available_cols].sum(axis=1)
vehicle_df['ZIP'] = vehicle_df['Geographic Area Name'].str.strip("ZCTA5 ")

zcta_path = os.path.join(dir_name, "../Modified Zip Code Tabulation Areas (MODZCTA)")

zcta_gdf = gpd.read_file(zcta_path)
zcta_gdf['total_vehicles'] = 0
zcta_gdf = zcta_gdf.merge(vehicle_df[['total_households_vehicle', 'ZIP']], left_on='modzcta', right_on='ZIP', how='left')
zcta_gdf.loc[zcta_gdf.total_households_vehicle.isna(), 'total_households_vehicle'] = zcta_gdf.total_households_vehicle.mean()
zcta_gdf['vehicle_own_rate'] = zcta_gdf.total_households_vehicle / zcta_gdf.pop_est
zcta_gdf = zcta_gdf[:177]

fig, ax = plt.subplots(figsize=(10,10))

ax.axis("off")

zcta_gdf[zcta_gdf.vehicle_own_rate < 0.5].plot(column='vehicle_own_rate', ax=ax, legend=False, cmap='OrRd')

fig.patch.set_facecolor('white')
fig.patch.set_alpha(0.0001)

# legend = ax.legend()
# ax.setp(legend.get_texts(), color='w')

st.pyplot(fig)

st.header("Simulating users")

nta['population'] = nta.pop_2E
total_population = round(nta['population'].sum())

st.write("The total population of NYC is 8,443,713. In our pessimistic scenario, we would have 8,444 users. In our realistic scenario, we would have 422,186. Finally, in our optimistic scenario, we would have 1,266,557 users. We will now examine how these different scenarios affect the effectiveness of Lighthouse-guided evacuations. ")
