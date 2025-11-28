import os
from dotenv import load_dotenv

import torch
import numpy as np
import cv2
from PIL import Image

from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel

class ArchIntelligent:
    def __init__(self):
        # Get private variables from enviroment
        load_dotenv("backend\.env")
        
    
        self.hf_token = os.getenv("HF_TOKEN")
        self.style_models = os.getenv("STYLE_MODELS")
        self.room_style_models= os.getenv("ROOM_STYLE_MODELS")
        self.room_type_models= os.getenv("ROOM_TYPE_MODELS")
        self.functional_models= os.getenv("FUNCTION_MODELS")
        self.enhancement= os.getenv("REALISM_ENHANCE")
        self.controlnet_model= os.getenv("CONTROLNET")
        self.base_model = os.getenv("BASEMODEL")
        
        self.model_config = {}
        
        # Configure ControlNet model
        controlnet = ControlNetModel.from_pretrained(
                                                    self.controlnet_model,
                                                    torch_dtype= torch.float16,
                                                    cache_dir= r"huggingface_cache",
                                                    token= self.hf_token,
                                                    variant= 'fp16',
                                                    )
        
        self.pipeline= StableDiffusionXLControlNetPipeline.from_pretrained(
                                                            self.base_model,
                                                            controlnet= controlnet,
                                                            torch_dtype= torch.float16,
                                                            cache_dir= r"huggingface_cache",
                                                            token= self.hf_token,
                                                            variant= 'fp16',
                                                            )

        
        #  Enable memory-efficient optimizations
        try:
            self.pipeline.enable_xformers_memory_efficient_attention()
            self.pipeline.enable_vae_slicing()
            self.pipeline.enable_sequential_cpu_offload()

            print(f"xFormers enabled\nVAE Slicing mode enabled\nSequential CPU Offload enabled!")
        except Exception as e:
            print(f"Warning: Some optimizations failed: {e}")
            


            

    def img2canny(self, input_img):
        """
        Processing user's condition image into edge map
        
        Parameters
            input_img : PIL image

        Returns
           PIL image
        """
        
        np_image = np.array(input_img)
        
        # Convert the image into a grayscale image then extract edge map
        canny = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        canny = cv2.resize(canny, (1024, 1024))
        canny = cv2.Canny(canny, 100, 200)
        
        canny = Image.fromarray(canny)
        
        return canny        

    def process_config(self, config: dict, mode):
        
        style_dict = {"Modern": "Modernism", "Minimalism": "Minimalism", "Art Deco": "ArtDeco",
                   "Art Nouveau": "ArtNouveau", "Baroque": "Baroque", "Brutalist": "Brutalist",
                   "Classical": "Classical", "Neo-Classical": "Neo-Classical", "Cyberpunk": "Cyberpunk",
                   "Deconstructivism": "Deconstructivism", "Futurism": "Futurism", "Gothic": "Gothic",
                   "Neo-Futurism": "Neo-Futurism", "Sustainable": "Sustainable", "Victorian": "Victorian"}
        
        functional_dict = {"Residential": "Modern", "Villa": "Modern", "Office": "Office", "Skyscraper": "SkyScraper",
                           "Hotel": "Hotel", "School Campus": "SchoolCampus", "Farmhouse": "Farmhouse", "Playground": "PlayGround",
                           "Park": "Park", "Apartment": "Apartment", "Hospital": "Hospital", "Kindergarten": "KinderGarten",
                           "Church": "Church", "Container": "Container", "Bridge": "Bridge", "Resort": "Resort", "Airport": "Airport",
                           "Factory": "Factory", "Stadium": "Stadium", "Temple": "Temple", "Tree House": "TreeHouse"}
        
        interior_style_dict= {"Art Deco": "artdeco", "Cream": "cream", "Cyberpunk": "cyberpunk",
                         "European": "european", "Industrial": "industrial", "Japanese": "japanese",
                         "Memphis": "memphis", "Minimalism": "minimalism", "Mixing": "mixing",
                         "Modern": "modern", "Neo-Classical": "neo-classical", "Nordic": "nordic",
                         "Royal": "royal", "Southeast Asian": "southeastasian", "Wabi sabi": "wabisabi"}
        
        room_type_dict= {"Barbershop": "barbershop", "Bathroom": "bathroom", "Bedroom": "bedroom",
                         "Bookstore": "bookstore", "Club": "club", "Coffeshop": "coffeshop",
                         "Convience Store": "conviencestore", "Gym": "gym", "Hospital": "hospital",
                         "Kids room": "kidsroom", "Kindergarden": "kindergarden", "Kitchen": "kitchen", 
                         "Living room": "livingroom", "Office": "office", "Shopping mall": "shoppingmall",
                         "Swimming pool": "swimmingpool", "Theater": "theater"}
        
        styles= config['style_names']
        functional= config['functional_names']
        
        season = config['season']
        landscape= config['landscape']
        weather= config['weather']
        day= config['time_of_day']
        
        config['posprompt_2'] = f"(realistic), ({styles}), ({functional}), ({landscape}), ({season}), ({weather}), ({day}), (high quality),\
                                    (high resolution), 4k render, detail, beautiful, cinematic lighting, hyper-realistic"
                                    
        config['negprompt_2'] = "(blurry), details are low, overlapping, (grainy), multiple angles, deformed structures, unnatural, unrealistic, cartoon, \
                                 anime, (painting), drawing, sketch, gibberish text, logo, noise, jpeg artifacts, mutation, (worst quality), (low quality), (low resolution),\
                                 messy, watermark, signature, cut off, low contrast, underexposed, overexposed, draft, disfigured, ugly, tiling, out of frame"

        if mode == "exterior":
            config["LoRA_style"] = style_dict[styles]
            config["LoRA_functional"] = functional_dict[functional]
        if mode == "interior":
            config["LoRA_style"] = interior_style_dict[styles]
            config["LoRA_functional"] = room_type_dict[functional]
            
        config['adapter_weights'] = [1.0, 1.0, 0.8]
           
        
        self.model_config = config
        self.mode= mode
    

    def generate(self):
        """
        Generate building image using user's input arguments 
        """
        
        # Get user's prompts from dictionary
        first_prompt = self.model_config["posprompt_1"]
        second_prompt = self.model_config["posprompt_2"]
        first_negprompt = self.model_config["negprompt_1"]
        second_negprompt = self.model_config["negprompt_2"]
        
        # Get user's image
        input_image = self.model_config['image']
        
        # Get ControlNet conditioning scale value
        controlnet_condition = self.model_config["condition_scale"]
        
        # Get guidance scale value
        guidance_scale = self.model_config["guidance"]
        
        # Get render speed
        render_speed = self.model_config["render_speed"]
        
        # Get LoRA weight's name and their corresponding adapter weights
        LoRA_style_names = self.model_config['LoRA_style']
        LoRA_functional_names = self.model_config['LoRA_functional']
        LoRA_enhancement_names = 'Realism'
        adapter_weights = self.model_config['adapter_weights']
        
        LoRA_names = [LoRA_style_names, LoRA_functional_names, LoRA_enhancement_names]
        
        self.pipeline.unload_lora_weights()
        print(f"\n\nUNLOADED PREVIOUS MODELSgit\n\n")
        
        os.environ['HF_HOME'] = r"huggingface_cache"     
        
        if self.mode == "exterior":   
            self.pipeline.load_lora_weights(
                                            self.style_models,
                                            weight_name= f"{LoRA_style_names}.safetensors", 
                                            adapter_name= LoRA_style_names
                                            )
        

            self.pipeline.load_lora_weights(
                                            self.functional_models,
                                            weight_name= f"{LoRA_functional_names}.safetensors", 
                                            adapter_name= LoRA_functional_names
                                            )
        
        if self.mode == "interior":
            
            self.pipeline.load_lora_weights(
                                            self.room_style_models,
                                            weight_name= f"{LoRA_style_names}.safetensors", 
                                            adapter_name= LoRA_style_names
                                            )
        

            self.pipeline.load_lora_weights(
                                            self.room_type_models,
                                            weight_name= f"{LoRA_functional_names}.safetensors", 
                                            adapter_name= LoRA_functional_names
                                            )
        
        self.pipeline.load_lora_weights(
                                        self.enhancement,
                                        weight_name= f"realarchvis_xlV10.safetensors",
                                        adapter_name= LoRA_enhancement_names
                                        )
        
        print(f"Finished loading models")
    

        self.pipeline.set_adapters(adapter_names= LoRA_names, adapter_weights= adapter_weights)
        print(f"Adapted models")
        
        # Transform the image into a depth map that is compatible with ControlNet   
        conditional_image = self.img2canny(input_image)
        
        # Setup the pipeline then generate image
        image = self.pipeline(
                            prompt= first_prompt,
                            prompt_2= second_prompt,
                            negative_prompt= first_negprompt,
                            negative_prompt_2= second_negprompt,
                            
                            image= conditional_image,
                            controlnet_conditioning_scale= controlnet_condition,
                            num_inference_steps= render_speed,
                            guidance_scale= guidance_scale
                             ).images[0]
        
        return image

    
if __name__ == '__main__':
    print("Loading")
    pipe = ArchIntelligent()

    print("Finished")
