import os
import gc

import streamlit as st
from streamlit_option_menu import option_menu

from app.exterior import app as exterior_app
from app.homepage import app as homepage_app
from app.interior import app as interior_app
from backend.inference import ArchIntelligent



st.set_page_config(page_title="ArchIntelligent", page_icon="🏠", initial_sidebar_state='expanded')




@st.cache_resource
def load_model():
    with st.spinner("🔄 Loading base model...", show_time= True):
        gc.enable()
        gc.collect()
        return ArchIntelligent()

pipe = load_model()


# with st.sidebar:
selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "Exterior Design", "Interior Design"],
    icons=["Psychology", "Home", "Bed"],
    orientation= 'horizontal',
    menu_icon="list",
    default_index=0,
    
)
    

if selected == "Home":
    homepage_app()
elif selected == "Exterior Design":
    exterior_app(pipe)
elif selected == "Interior Design":
    interior_app()
