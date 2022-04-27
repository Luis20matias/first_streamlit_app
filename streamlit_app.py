import streamlit
import requests
import pandas as pd

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinake & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick the fruit they want to incluide
fruits_selected = streamlit.multiselect(
    'Pick some fruits:',
    list(my_fruit_list.index),
    ['Avocado', 'Strawberries']
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header('Frutyvice Fruit Advice!')
fruitvyce_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
streamlit.text(fruitvyce_response.json())

# take the json version of the response and normalize it
fruitvyce_normalized = pd.json_normalize(fruitvyce_response.json())
#output it the screen as a table
streamlit.dataframe(fruitvyce_normalized)