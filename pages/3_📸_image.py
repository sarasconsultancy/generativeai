import streamlit as st
from prompt_generator import PromptGenerator
#from image_generator import ImageGenerator
#from img2img import Image2Image

from io import BytesIO

if 'llm_prompt' not in st.session_state:
    st.session_state['llm_prompt'] = None

st.set_page_config(page_title="Image to Image Generator", page_icon="💻", layout='wide')

st.title("Image to Image Generator")

with st.sidebar:
    image = st.file_uploader(label="Upload an Image", label_visibility="collapsed", type=["png","jpg","jpeg"],
                             accept_multiple_files=False, help= "Upload an image to use HuggingFace Img2Img Model")
    

col1, col2 = st.columns(2, gap="large")

with col1:
    if image:
        st.write("Image Uploaded")
        st.image(image=image, caption=image.name, use_column_width="always")
        user_prompt=st.text_input(label="Enter Your Prompt Idea Here")
        if st.button(label="Generate"):
            promt_generator=PromptGenerator()
            llm_prompt=promt_generator.get_response(user_prompt)
            st.session_state['llm_prompt'] == llm_prompt

if 'llm_prompt' in st.session_state and st.session_state['llm_prompt'] is not None:
    with col2:
        if image:
            image_generator=Image2Image(img=image)
        else:
            image_generator=ImageGenerator()

        with st.spinner():
            prompt=st.session_state['llm_prompt']
            st.write(prompt)
            image=image_generator.generate(prompt=prompt)
            img_bytes = BytesIO
            image.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            st.image(image=image, width=500)
            st.download_button(label="Download", data=img_bytes,file_name="image.png", mime='imge/png')


                  
        
        
        
        



    

