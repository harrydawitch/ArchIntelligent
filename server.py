from flask import Flask, request, jsonify
import base64
import io
from PIL import Image

from backend.inference import ArchIntelligent


# Load the Stable Diffusion XL model:
generate_pipeline = ArchIntelligent()

app = Flask(__name__)


# Endpoint for generating image
@app.route("/generate", methods= ['POST'])
def generate_image():
    
    # Get input settings from the frontend
    data = request.get_json()
    
    if not data:
        return jsonify({'Error': "No input data provided!"}), 400
    
    try:
        
        image = data.get("image")
        
        pos_prompt= str(data.get("pos_prompt", ""))
        neg_prompt= str(data.get("neg_prompt", ""))
        
        style = str(data.get("style_names", "Modern"))
        functional = str(data.get("functional_names", "Residential"))
        
        guidance = float(data.get("guidance", 7.5))
        geometry = float(data.get("condition_scale", 0.5))
        
        season = str(data.get("season", ""))
        weather = str(data.get("weather", ""))
        landscape = str(data.get("landscape", ""))
        time = str(data.get("time_of_day", ""))
        
        render_speed = int(data.get('render_speed', 30))
    
    
    except Exception as e:
        return jsonify({"error": "Invalid input data"}), 400
    
    
    # Utility function to convert image to Base64 string
    def image_to_base64(img):
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    def store_config():
        config = {}
        
        config['style_names'] = style
        config['functional_names'] = functional
        
        config['posprompt_1'] = pos_prompt
        config['negprompt_1'] = neg_prompt
        
        config['season'] = season
        config['landscape'] = landscape
        config['weather'] = weather
        config['time_of_day'] = time
        
        config['guidance'] = guidance
        config['condition_scale'] = geometry
        
        config['render_speed'] = render_speed
        
        config['image'] = image
    
        return config
    
    
    try:
        # Processing config from frontend
        config = store_config()
        generate_pipeline.process_config(config)
        
        image = generate_pipeline.generate()
        encoded_image = image_to_base64(image)
        
        return jsonify({'image': encoded_image})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug= True)