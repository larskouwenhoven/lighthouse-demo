import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import pathlib
import os
from PIL import Image


st.title('Lighthouse Technical Demo')

intro_text = "Lighthouse is an app that helps people get to safety in times of hurricanes and other natural disasters. Lighthouse heavily relies on algorithms that optimize the user journey when evacuating in these events. This page allows the user to understand these algorithms and the techniques behind Lighthouse through an interactive demonstration, focusing on New York City. "
intro_text_2 = "The NYC government has devised 6 different evacuation zones. During a natural disaster,  individuals living in a subset of these evacuation zones may be required to evacuate, or conversely, to stay in place. In this technical demonstration, we will use three different scenarios. In scenario 1, evacuation zones 1 and 2 are asked to evacuate. In scenario 2, this is the case for zones 1 through 4; and finally, in scenario 3, all zones (1 through 6) are asked to evacuate. These three scenarios are displayed in the maps below. "

st.write(intro_text)
st.write(intro_text_2)

scenario = st.selectbox("Select a scenario", ['Scenario 1', 'Scenario 2', 'Scenario 3'])

sc1_image = Image.open("sc1.png")
sc2_image = Image.open("sc2.png")
sc3_image = Image.open("sc3.png")

if scenario == 'Scenario 1':
    st.image(sc1_image, caption="Evacuation zones 1 and 2")
    
elif scenario == 'Scenario 2':
    st.image(sc2_image, caption="Evacuation zones 1 through 4")
    
else:
    st.image(sc3_image, caption="Evacuation zones 1 through 6")
    
challenge_text = "One challenge that Lighthouse intends to overcome is the fact that even in mandatory evacuation areas, few people evacuate. For example, during hurricane Sandy, only 40% of the population in evacuation zones actually evacuated. In zones that were not devised as evacuation zones, still 10% of the population evacuated. Lighthouse has then identified four different groups of users, displayed in the following overview. "
challenge_text_2 = "Lighthouse aims to increase the share of people that are ordered to evacuate, and actually do so, and decrease the number of people that evacuate, even though they are not in an evacuation zone. The behavior of these people can have adverse effects, as they may take up valuable road space, leading to traffic jams and hindering the evacuation process of others. "

st.write(challenge_text)
table_img = Image.open('table.png')

col11, col21, col31= st.columns(3)

with col21:
    st.image(table_img,)

st.write(challenge_text_2)

st.subheader("Vehicle ownership")

veh_text = "One reason people in New York City decide to not evacuate, is the fact that they may not have access to a personal vehicle. One average, some 40% of people own a car, but this number is as low as 8% in some areas in Manhattan and Brooklyn. The map below shows the car ownership rates of different areas in New York City. "
veh_text_2 = "While car ownership is relatively low, many of the people evacuating using their own vehicle have empty seats. There is thus an opportunity to more equitably distribute resources here. One of Lighthouse's key features is to connect people looking for transport, with those who are evacuating with empty seats. "

st.write(veh_text)

# car ownership map
veh_image = Image.open('vehicle_ownership.png')
st.image(veh_image, caption="Vehicle ownership rates in NYC")

st.write(veh_text_2)

st.subheader("Ride-sharing")

rs_text = "This section shows the potential impact that Lighthouse's pairing algorithm may have in the situation of a hurricane. A user can select one of the three scenarios, and explore how many more people are effectively evacuated. All of these scenarios are under the assumption of a conservative adoption rate of 0.5%. In practice, this means some 40,000 people were to use Lighthouse in New York City. One can imagine the optimisation realized under this assumption would be even stronger at higher adoption rates. "
rs_text_2 = "For each of the three scenarios, we will first display (1) the number of people (using Lighthouse) looking for a ride; (2) the number of spare seats available; and (3) the number of people Lighthouse successfully matches, so they now have a means of transportation. "

st.write(rs_text)
st.write(rs_text_2)

scenario_2 = st.selectbox("Select a scenario:", ['Scenario 1', 'Scenario 2', 'Scenario 3'])

col1, col2, col3 = st.columns(3)

if scenario_2 == 'Scenario 1':
    with col1:
        st.write("Number of spare seats:")
        st.write("Number of requested seats:")
        st.write("Share of potential seats matched:")
        st.write("Average time deviation:")
    with col2:
        st.write("**952**")
        st.write("**2,932**")
        st.write("**51%**")
        st.write("**5.1 minutes**")
    with col3:
        st.subheader("")
elif scenario_2 == 'Scenario 2':
    with col1:
        st.write("Number of spare seats:")
        st.write("Number of requested seats:")
        st.write("Share of potential seats matched:")
        st.write("Average time deviation:")
    with col2:
        st.write("**1,756**")
        st.write("**4,127**")
        st.write("**59%**")
        st.write("**1.8 minutes**")
    with col3:
        st.subheader("")
elif scenario_2 == 'Scenario 3':
    with col1:
        st.write("Number of spare seats:")
        st.write("Number of requested seats:")
        st.write("Share of potential seats matched:")
        st.write("Average time deviation:")
    with col2:
        st.write("**3,776**")
        st.write("**9,394**")
        st.write("**68.7%**")
        st.write("**1.2 minutes**")
    with col3:
        st.subheader("")

map_text = "Lighthouse also provides an algorithm to efficiently route users. When matching a car with spare seats to a household looking for transport, we minimize the time traveled. The data above also displays the average minutes driving spent additionally, as a result of picking up another family. As you can see, this number decreases as the severity of the hurricane increases. This fact shows the power of Lighthouse: if more people are impacted, more people will also be available to offer rides. The maps below show the deviations people must make to pick up someone in need of transport. It is now obvious why these deviations are shorter as the severity of the impact increases. "

st.write(map_text)


rs_img_1 = Image.open("routes_merged1_pessimistic.png")
rs_img_2 = Image.open("routes_merged2_pessimistic.png")
rs_img_3 = Image.open("routes_merged3_pessimistic.png")

scenario_3 = st.selectbox("Select a scenario: ", ['Scenario 1', 'Scenario 2', 'Scenario 3'])

if scenario_3 == 'Scenario 1':
    st.image(rs_img_1)
elif scenario_3 == 'Scenario 2':
    st.image(rs_img_2)
elif scenario_3 == 'Scenario 3':
    st.image(rs_img_3)