import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu


with st.sidebar:
  selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Data visulization","Disease prediction"],
    icons = ["house","book","envelope"],
    menu_icon = "cast",
    default_index = 0,
  )
