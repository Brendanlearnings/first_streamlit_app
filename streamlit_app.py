import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)


def get_fruityvice_datat(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruit_normal = pandas.json_normalize(fruityvice_response.json())
  return fruit_normal

# New section to display fruitvice reponse 
  streamlit.header('Fruityvice Fruit Advise')
  try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
    else:
      back_from_function = get_fruityvice_datat(fruit_choice)      
      streamlit.dataframe(fruit_normal)
      
  except URLError as e:
    streamlit.error()


# Dont run anything past here while we troubleshoot
streamlit.stop()

# Query our account metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("My fruit list contains:")
streamlit.dataframe(my_data_row)

# Allow end user to add a fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add?")
streamlit.write("Thanks for adding ", add_my_fruit)

# This wont work - for showcasing purposes. 
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
