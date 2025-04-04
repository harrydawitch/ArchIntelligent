import os
import subprocess
import time

from PIL import Image
from io import BytesIO

import pandas as pd
import numpy as np

from streamlit_image_select import image_select
from streamlit_image_comparison import image_comparison
import streamlit as st 


#______________________________Add image________________________________________________________________________________________________________________________________________
def app(pipeline):
        
    # Initialize session states if they don't exist
    if 'lock_settings' not in st.session_state:
        st.session_state['lock_settings'] = False
    if 'generating_process' not in st.session_state:
        st.session_state['generating_process'] = False
    if 'generation_complete' not in st.session_state:
        st.session_state['generation_complete'] = False
    if 'generated_image' not in st.session_state:
        st.session_state['generated_image'] = None


    
    with st.container(border= True):   
        st.header("1. Upload your image", )
        uploaded_image = st.file_uploader(
                label= "# **Upload you image**",
                type= ['png', 'jpg', 'jpeg'],
                disabled= st.session_state['lock_settings'],
                label_visibility = 'collapsed',
                )
        if uploaded_image:
            st.image(uploaded_image)
            pil_img = Image.open(uploaded_image).convert("RGB")
        
            
            
        
#_____________________________Add Design Style and Building Type________________________________________________________________________________________________________________________________________

        
    style_choices = ["Modern", "Minimalism","Art Deco", 
                    "Art Nouveau","Baroque", "Brutalist", "Classical", "Neo-Classical", 
                    "Cyberpunk", "Deconstructivism", "Futurism", "Sustainable",
                    "Gothic",  "Neo-Futurism", "Victorian"
                    ]
    
    functionality_choices = [
                            "Residential", "Villa", "Office", "Skyscraper", 
                            "Hotel", "School Campus", "Farmhouse", "Playground", "Park", "Apartment",
                            "Hospital", "Kindergarten", "Church", "Container", "Bridge",
                            "Resort", "Airport", "Factory", "Stadium", "Temple", "Tree House"
                            ]
    
    with st.container(border= True):
        st.header("Choose style and functionality", divider= 'blue')
        style_col, function_col = st.columns([0.91, 1], border= False)
        with style_col:
            st.write("**Design Style**")
            styles= st.selectbox(label='Style choice',
                            options= style_choices,
                            placeholder= "Design style",
                            label_visibility= 'collapsed',
                            disabled= st.session_state['lock_settings']
                            )
        with function_col:
            st.write("**Functionality**")
            functional= st.selectbox(   
                        label='Functionality choice',
                        options= functionality_choices,        
                        placeholder= "Functionality",
                        label_visibility= 'collapsed',
                        disabled= st.session_state['lock_settings']
                        )
        
            
#______________________________________Add Detail________________________________________________________________________________________________________________________________________
    
    def idx2cls(mode:list):
        return {i: j for i, j in enumerate(mode)}                    
            
    if "season" not in st.session_state:
        st.session_state['season'] = ""
    if "weather" not in st.session_state:
        st.session_state['weather'] = ""
    if "day" not in st.session_state:
        st.session_state['day'] = ""
    if "landscape" not in st.session_state:
        st.session_state['landscape'] = ""
        
    with st.container(border= True):
        
        st.header("Add Details")
        @st.dialog("Choose Season")
        def add_season():
            season_photos = [r".\app\asset\images\season\Spring.jpg",  
                            r".\app\asset\images\season\Summer.jpg", 
                            r".\app\asset\images\season\Autumn.jpg", 
                            r".\app\asset\images\season\Winter.jpg"]
            
            season_caps = ["Spring", "Summer", "Autumn", "Winter"]
            
            season_selection = image_select(label= "", 
                            images = season_photos,
                            captions= season_caps, return_value= 'index',
                            )
            
            season_button = st.button("**Select**", 
                                    use_container_width= True, 
                                    type='primary')  
            
            idx2class = idx2cls(season_caps)
                
            if season_button:
                st.session_state['season'] = idx2class[season_selection]
                st.rerun()
        
        
        @st.dialog("Choose Weather")        
        def add_weather():
            weather_photos = [r".\app\asset\images\weather\Sunny.jpg", r".\app\asset\images\weather\Rainy.jpg",
                            r".\app\asset\images\weather\Cloudy.jpg", r"E:.\app\asset\images\weather\Foggy.jpg",
                            r".\app\asset\images\weather\Snowy.jpg", r"E:.\app\asset\images\weather\Storm.jpg"]
            weather_caps = ['Sunny', "Rainy", "Cloudy", "Foggy", "Snowy", "Storm"]
            weather_selection = image_select(label='', 
                                            images= weather_photos, 
                                            captions= weather_caps,
                                            return_value= 'index')
            weather_button = st.button("**Select**", 
                        use_container_width= True, 
                        type='primary')
            
            idx2class = idx2cls(weather_caps)
            if weather_button:
                st.session_state['weather'] = idx2class[weather_selection]
                st.rerun()
                
        @st.dialog("Time of Day")        
        def add_day():
            day_photos = [
                        r".\app\asset\images\time of day\sunrise.jpg",
                        r".\app\asset\images\time of day\mid_day.jpg",
                        r".\app\asset\images\time of day\sunset.jpg",
                        r".\app\asset\images\time of day\night.jpg"
                        ]
            
            day_caps = ["Sunrise", "Mid day", "Sunset", "Night"] 
            day_selection = image_select(label='', 
                                        images= day_photos, 
                                        captions= day_caps,
                                        return_value= 'index')    
            day_button = st.button("**Select**", 
                        use_container_width= True, 
                        type='primary')
            
            idx2class = idx2cls(day_caps)
            if day_button:
                st.session_state['day'] = idx2class[day_selection]
                st.rerun()


        @st.dialog("Landscape")        
        def add_landscape():
            landscape_photos = [r".\app\asset\images\landscape\urban.jpg", r".\app\asset\images\landscape\surburban.jpg",
                                r".\app\asset\images\landscape\coastal.jpg", r".\app\asset\images\landscape\grassland.jpg",
                                r".\app\asset\images\landscape\forest.jpg", r".\app\asset\images\landscape\tropical.jpg",
                                r".\app\asset\images\landscape\desert.jpg", r".\app\asset\images\landscape\mountain.jpg",
                                r".\app\asset\images\landscape\swamp.jpg", r".\app\asset\images\landscape\polar.jpg"]
            
            landscape_caps = ["Urban", "Suburban", "Coastal", "Grassland", 'Forest',
                            'Tropical', "Desert", "Mountain", "Swamp", "Polar"] 
            
            landscape_selection = image_select(label='', 
                                        images= landscape_photos, 
                                        captions= landscape_caps,
                                        return_value= 'index')    
            landscape_button = st.button("**Select**", 
                        use_container_width= True, 
                        type='primary')
            
            idx2class = idx2cls(landscape_caps)
            if landscape_button:
                st.session_state['landscape'] = idx2class[landscape_selection]
                st.rerun()

            
        with st.popover(label= "Add Detail", 
                        use_container_width= True, 
                        disabled= st.session_state['lock_settings']):
            
            first_col, second_col = st.columns([0.5, 0.5], vertical_alignment='center')
            with first_col:   
                if st.button("**Season**", use_container_width= True):
                    add_season()
                if st.button("**Weather**", use_container_width= True):
                    add_weather()
            with second_col:
                if st.button("**Time**", use_container_width= True):
                    add_day()
                if st.button("**Landscape**", use_container_width= True):
                    add_landscape()
                    
        col1, col2 = st.columns([0.5, 0.8], vertical_alignment= "bottom")
        col3, col4 = st.columns([0.5, 0.8], vertical_alignment= "bottom")
        col5, col6 = st.columns([0.5, 0.8], vertical_alignment= "bottom")
        col7, col8 = st.columns([0.5, 0.8], vertical_alignment= "bottom")
        
        col1.markdown('<p style="font-size:18px; font-weight:bold;">Season:</p>', unsafe_allow_html=True)
        col2.markdown(f'<p style="font-size:16px; font-weight:normal;">{st.session_state["season"]}</p>', unsafe_allow_html=True)
        
        col3.markdown('<p style="font-size:18px; font-weight:bold;">Time:</p>', unsafe_allow_html=True)
        col4.markdown(f'<p style="font-size:16px; font-weight:normal;">{st.session_state["day"]}</p>', unsafe_allow_html=True)
        
        col5.markdown('<p style="font-size:18px; font-weight:bold;">Weather:</p>', unsafe_allow_html=True)
        col6.markdown(f'<p style="font-size:16px; font-weight:normal;">{st.session_state["weather"]}</p>', unsafe_allow_html=True)

        col7.markdown('<p style="font-size:18px; font-weight:bold;">Landscape:</p>', unsafe_allow_html=True)
        col8.markdown(f'<p style="font-size:16px; font-weight:normal;">{st.session_state["landscape"]}</p>', unsafe_allow_html=True)


#________________________________Add Prompt and Negative Prompt________________________________________________________________________________________________________________________________________


    with st.container(border=True):
        st.header("Add Prompts")
        @st.dialog("Keywords")
        def add_keywords():
            
            with st.container(border= True, height= 270):
                st.subheader(body= "View Direction")
                views = st.pills(
                                label= "Choose view",
                                options= ['Elevation Frontal View', 'Aerial View', 'Close-Up Shot',
                                        'Street-level View', 'Wide Shot', 'Cropped View'],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'
                                )
                views = [i.lower() for i in views]
                
                st.subheader(body= "Space Type")
                spaces = st.pills(
                                label= "Choose spaces",
                                options= ['Residential building', 'Countryside villa', "Office building", 
                                        "Office Tower", "Skyscraper", "Stadium Building", "School Building",
                                        "Hotel Building", "Factory Building", "Commercial Building"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                spaces = [i.lower() for i in spaces]
                
                st.subheader(body= "Design style")
                design = st.pills(
                                label= "Design style",
                                options= ["Modern", "Minimalism","Art Deco", 
                                        "Art Nouveau","Baroque", "Brutalist", "Classical", "Neo-Classical", 
                                        "Cyberpunk", "Deconstructivism", "Futurism", 
                                        "Gothic",  "Neo-Futurism", "Victorian"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                design = [i.lower() for i in design]

                st.subheader(body= "Materials")
                material = st.pills(
                                label= "Materials",
                                options= ['Glass', 'Stone', "Metal", "Steel", "Wood", "Brick", "Plastic", "Gypsum",
                                        "Concrete", "Polished Concrete", "Paint", "Stucco", "Marble", "Terracotta"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                material = [i.lower() for i in material]

                st.subheader(body= "Landscape")
                landscape = st.pills(
                                label= "Landscape",
                                options= ['Cityscape', 'Countryside', "Forest", "Desert", "Mountain", "Coastal", 
                                        "Tropical", "Grassland", "Tundra", "Wetland"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                landscape = [i.lower() for i in landscape]
                
                st.subheader(body= "Weather")
                weather = st.pills(
                                label= "Weather",
                                options= ['Sunny', 'Night', "Rainy", "Snowy", "Cloudy Sky", "Foggy", 
                                        "Dusk", "Sunset", "Sunrise"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                weather = [i.lower() for i in weather]

                st.subheader(body= "Lighting")
                lighting = st.pills(
                                label= "lighting",
                                options= ['Soft Lights', 'Golden Hour', "Morning Lights", "Sunbeams", "High Contrast"],
                                selection_mode= 'multi',
                                label_visibility= 'collapsed'              
                                )
                lighting = [i.lower() for i in lighting]
                
            if st.button(label= "# **Add Keywords**", type= "primary"):
                combined = views + spaces + design + material + landscape + weather + lighting
                
                if not combined:
                    st.error(":red[**You haven't selected any keywords**]", icon="🚨")
                else:
                    st.session_state['add_kw'] = f"{prompt} {", ".join(combined)}"
                    st.rerun()
            
        
        if st.button("**+ Add Keywords**", 
                    type= 'secondary', 
                    disabled= st.session_state['lock_settings']):
            add_keywords()

        if "add_kw" not in st.session_state:
            st.session_state['add_kw'] = str("")

    
        prompt = st.text_area(
                                label= "# **Prompt**", 
                                placeholder= "Describe your image",
                                value = st.session_state['add_kw'],
                                max_chars= 600,
                                disabled= st.session_state['lock_settings']
                            )

        neg_prompt= st.text_area(
                                label= "# **Negative prompt (optinal)**",
                                placeholder= "Remove unwanted element",
                                value= '',
                                max_chars= 200,
                                disabled= st.session_state['lock_settings'],
                                )

#___________________________________Creative mode________________________________________________________________________________________________________________________________________
    
    if 'guidance' not in st.session_state:
        st.session_state['guidance'] = 7.50


    with st.container(border= True):
        
        st.header(body= "Creative")

        # Function to update guidance value
        def change_guidance():
            if st.session_state['guidance'] != st.session_state['guidance_numeric']:
                st.session_state['guidance'] = float(st.session_state['guidance_numeric'])
                
            elif st.session_state['guidance'] != st.session_state['guidance_slider']:
                st.session_state['guidance'] = float(st.session_state['guidance_slider'])
            
        num_col, slider_col = st.columns([1, 3])
        # Number input synced with  slider input
        with num_col:
            guidance_numeric = st.number_input("Guidance Scale", min_value=1.0, max_value=15.0, 
                                                value=float(st.session_state['guidance']),
                                                placeholder="Input guidance scale",
                                                key="guidance_numeric",  
                                                on_change=change_guidance,
                                                label_visibility='collapsed',
                                                disabled= st.session_state['lock_settings']
                                            )  
        with slider_col:
            # Slider input synced with number input
            guidance_slider = st.slider("Guidance Scale", min_value=1.0, max_value=15.0,
                                        value=st.session_state['guidance'],
                                        step=0.1,
                                        key= 'guidance_slider',
                                        on_change= change_guidance,
                                        label_visibility='collapsed',
                                        disabled= st.session_state['lock_settings']
                                        )
        with st.expander("How it works?", expanded= True):
            st.write("""
            - Less guidance from the prompt. Flexible with the prompt. Great for redesign.
            - Follow extracly with the prompt, minor change to the prompt.
            """)
            
#___________________________________________Geometry mode________________________________________________________________________________________________________________________________________    

    if 'geometry_scale' not in st.session_state:
        st.session_state['geometry_scale'] = 0.5
        
    with st.container(border= True):
        st.header(body= "Geometry")
        
        def change_geometry():
    
            if st.session_state['geometry_scale'] != st.session_state['geo_col1']:
                st.session_state['geometry_scale'] = float(st.session_state['geo_col1'])
                
            elif st.session_state['geometry_scale'] != st.session_state['geo_col2']:
                st.session_state['geometry_scale'] = float(st.session_state['geo_col2'])

        # Slider with dynamic value display to the left
        col1, col2 = st.columns([1, 3], vertical_alignment= 'top')
        with col1:
            value = st.number_input("Geometry", 0.0, 1.0, 
                                    value= float(st.session_state['geometry_scale']), 
                                    label_visibility="hidden", 
                                    key= "geo_col1", 
                                    on_change= change_geometry,
                                    disabled = st.session_state['lock_settings']
                                    )
            
        with col2:
            value = st.slider("Geometry", 0.0, 1.0, 
                            value= float(st.session_state['geometry_scale']), 
                            label_visibility="hidden", 
                            key= "geo_col2", 
                            on_change= change_geometry,
                            disabled= st.session_state['lock_settings'])


        # Clickable link with detailed description
        with st.expander("How it works?", expanded= True):
            st.write("""
            - **Flexible:** Less guidance from input image. Great for redesign.
            - **Balanced:** Mix of creativity and precision.
            - **Precise:** Accurate, minor change to original input geometry. Good for rendering.
            """)

#____________________________________________________Render mode________________________________________________________________________________________________________________________________________
    
    if "render_mode" not in st.session_state:
        st.session_state["render_mode"] = "Fast"  
        
    with st.container(border= True):

        # Function to switch mode
        def set_render_mode():
            mode_mapping = {"⚡**Fast Render**": True,
                            "🌟 **Best Render**": False}
            st.session_state["render_mode"] = mode_mapping[render_mode]


        st.subheader("**Render Speed**")
        # Two buttons side by side
        render_mode = st.radio("Render Mode", 
                                options= ["⚡**Fast Render**", "🌟 **Best Render**"],
                                label_visibility= 'collapsed',
                                captions= ["**Fast Render:** Quicker, Lower quality",
                                            "**Best Render:** Slower, Best quality"],
                                on_change= set_render_mode,
                                disabled= st.session_state['lock_settings'])

    if 'lock_settings' not in st.session_state:
        st.session_state['lock_settings'] = False
    
    if 'start_generate' not in st.session_state:
        st.session_state['start_generate'] = 'secondary'
        
    
    def store_config():
        config = {}
        
        config['style_names'] = styles
        config['functional_names'] = functional
        
        
        config['posprompt_1'] = prompt
        config['negprompt_1'] = neg_prompt
        
        config['season'] = st.session_state['season']
        config['landscape'] = st.session_state['landscape']
        config['weather'] = st.session_state['weather']
        config['time_of_day'] = st.session_state['day']
        
        config['guidance'] = st.session_state['guidance']
        config['condition_scale'] = st.session_state['geometry_scale']
        config['render_speed'] = st.session_state["render_mode"]
        
        config['image'] = pil_img
        
        return config

    def lock_and_unlock():
        
        if not st.session_state['lock_settings']: 
            st.session_state['lock_settings'] = True
            
        elif st.session_state['lock_settings']:
            st.session_state['lock_settings'] = False
    
    if 'lock_generate_bttn' not in st.session_state:
        st.session_state['lock_generate_bttn'] = False
        
    def reset_generation():
        st.session_state['generating_process'] = False
        st.session_state['generation_complete'] = False
        st.session_state['generated_image'] = None

    def download_image(generated_img):
        buffer = BytesIO()
        
        generated_img.save(buffer, format="PNG")
        
        img_bytes = buffer.getvalue()

        st.download_button(
                        label= "DOWNLOAD",
                        data= img_bytes,
                        file_name= "archintelligent_generated.png",
                        mime= "image/png",
                        type= "primary",
                        use_container_width= True,
                        on_click= 'ignore'
                        )


    def generate_image():
        with st.spinner("Generating your image...", show_time= True):
            config =  store_config()
            pipeline.process_config(config)
            image = pipeline.generate()
            
            # Compare the input image and the result image
            st.session_state['generated_image'] = image
            
        st.session_state['generation_complete'] = True
        st.session_state['generating_process'] = False
            

        # download_image(image)
        if st.button("**Go back**"):
            st.session_state['generating_process'] = False
            st.rerun()

    lock_toggle = "**LOCK SETTINGS**" if not st.session_state['lock_settings'] else "**UNLOCK SETTINGS**"
    c1, c2 = st.columns([0.5, 1.6], gap= 'small')
    
    with c1:
        if st.button(
                    label= lock_toggle, 
                    use_container_width= False,
                    on_click= lock_and_unlock,
                    disabled=st.session_state['generating_process'] or \
                             st.session_state['generation_complete']):
            
            st.session_state['lock_settings'] = True
        
    with c2:
        generate_bttn= st.button(
                                label= "# **GENERATE**", 
                                use_container_width= True,
                                type= 'primary',
                                disabled=st.session_state['generating_process'] or \
                                         st.session_state['generation_complete']
                                )
        
        if generate_bttn and st.session_state['lock_settings']:
            if not uploaded_image:
                st.error("Please upload an image before proceeding!", icon= "❌")
            else:
                st.session_state['generating_process'] = True
                st.rerun()
                
        elif generate_bttn and not st.session_state['lock_settings']:
            st.error("Lock settings before generate image", icon="🚨")

    with st.container(border=True):

        
        if st.session_state['generating_process'] and not st.session_state['generation_complete']:
            generate_image()
            st.rerun()  # Rerun to show the results after generation
            
        elif st.session_state['generation_complete']:
            
            st.title("Result")
        
            # Display the stored image
            if st.session_state['generated_image']:
                
                image_comparison(
                                img1= pil_img,
                                img2= st.session_state['generated_image'],
                                label1="BEFORE",
                                label2="AFTER",
                                )
            
            left, right = st.columns([0.125, 0.8])
            with right:
                download_image(st.session_state['generated_image'])
            with left:
                # Go back button outside the generate_image function
                if st.button("**Go back**", on_click= reset_generation):
                    pass  # The on_click handler will reset the states
        else:
            pass
