import os
import subprocess

import time
from PIL import Image
import pandas as pd
import numpy as np

import streamlit as st 
from streamlit_image_comparison import image_comparison


def app():
    # st.set_page_config(page_title="ArchIntelligent", page_icon="🏠", initial_sidebar_state='expanded')

    # with st.sidebar:
    st.title(":red[Arch]Intelligent", anchor="anchor_example")
    st.caption('*Made by* :blue[**[*Long Thien Hoang Chu (Harry)*](https://www.facebook.com/harryedits3007)**] - Industrial University of Ho Chi Minh City', 
                unsafe_allow_html=True)


    image_comparison(img1=r".\app\asset\images\homepage\image_1.jpg",
                    img2=r".\app\asset\images\homepage\image_2.jpg",
                    label1= "Before",
                    label2= "After",
                    )

    st.write(
        """
                **Render or redesign your exterior designs in seconds. Just upload a photo or sketch and see the magic in action.**
                \n1. Upload an image of your design.
                \n2. Image can be a sketch, snapshot from 3d model or a real photo.
                \n3. Write a good prompt to describe your design.
                \n4. Choose your render mode.
    \n← Start generating from side panel
        """
            )
