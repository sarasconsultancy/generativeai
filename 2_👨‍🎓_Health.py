import streamlit as st
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import re
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("api_key"))

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()

        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initialize streamlit application

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

input = st.text_input("Input Prompt : " , key="input")

upload_file = st.file_uploader("Choose an Image....", type=["jpg","jpeg","png"])

image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the Total Calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items which calories intake 
is bellow format

1. Item 1 - no of calories
2. Item 2 - no of calories
-----------
-----------
"""

## If submit button is clicked

if submit:
    image_data = input_image_setup(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)










