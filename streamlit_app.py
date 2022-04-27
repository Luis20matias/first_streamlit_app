import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

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

# New section to display fruityvice api response
streamlit.header('Frutyvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?',
                                        placeholder='fruit name')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information')
    else:
        fruitvyce_response = requests.get('https://fruityvice.com/api/fruit/'+
                                        fruit_choice)
        fruitvyce_normalized = pd.json_normalize(fruitvyce_response.json())
        streamlit.dataframe(fruitvyce_normalized)
except URLError as e:
    streamlit.error()

# Don't run anything past here while we troubleshoot
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add?",
                                    "jackfruit")

streamlit.write('Thanks for adding', add_my_fruit)

# This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")