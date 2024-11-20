import gradio as gr
import pytesseract
from PIL import Image

# Function to extract text using OCR
def ocr_extract_text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to analyze ingredients
def analyze_ingredients(text):
    vegan_ingredients = ["sugar", "salt", "flour"]
    non_vegan_ingredients = ["milk", "egg", "gelatin"]
    haram_ingredients = ["pork", "alcohol"]

    words = text.lower().split()
    results = {
        "vegan": all(ingredient not in non_vegan_ingredients for ingredient in words),
        "halal": all(ingredient not in haram_ingredients for ingredient in words),
    }
    return results

# Function to compute health score
def compute_health_score(text):
    health_impact = {
        "sugar": -2,
        "salt": -1,
        "fiber": +2,
        "vitamins": +3,
    }
    score = 5  # Neutral baseline score
    for word in text.lower().split():
        score += health_impact.get(word, 0)
    return max(0, min(10, score))  # Keep score between 0-10

# Gradio interface function
def analyze_image(image_path):
    ingredients_text = ocr_extract_text(image_path)
    if "Error" in ingredients_text:
        return ingredients_text, "", ""

    dietary_results = analyze_ingredients(ingredients_text)
    health_score = compute_health_score(ingredients_text)

    return ingredients_text, dietary_results, f"Health Score: {health_score}/11"

# Updated Gradio Interface
interface = gr.Interface(
    fn=analyze_image,
    inputs=gr.Image(type="filepath"),  # Updated to filepath
    outputs=[
        gr.Textbox(label="Extracted Ingredients"),
        gr.Textbox(label="Dietary Analysis (Vegan/Halal)"),
        gr.Textbox(label="Health Score"),
    ],
    title="Food Product Analyzer",
    description="Upload an image of the ingredients to check if the product is vegan, halal, and healthy!",
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()