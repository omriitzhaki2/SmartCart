import streamlit as st
import base64
import os


@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache_data
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def set_title(title):
    return f"<h1 style='text-align: center; " \
           f"color: #20115E; font-family: Trebuchet MS;'>{title}</h1>"


def set_subtitle(subtitle, text_align='center'):
    return f"<h2 style='text-align: {text_align}; " \
           f"color: #20115E; font-family: Trebuchet MS;'>{subtitle}</h2>"


def set_subsubtitle(subsubtitle, text_align='center'):
    return f"<h3 style='text-align: {text_align}; " \
           f"color: #20115E; font-family: Trebuchet MS;'>{subsubtitle}</h3>"


def set_text(text, text_align='center', color='#20115E'):
    return f"<h6 style='text-align: {text_align};" \
           f"color: {color}; font-family: Trebuchet MS;'>{text}</h6>"

def set_text_list(text, text_align='left', color='#20115E'):
    return f"<h6 style='text-align: {text_align};" \
           f"color: {color}; font-size: 17px; font-family: Trebuchet MS;'>{text}</h6>"

def set_text_groceries_list(text, text_align='left', color='#20115E'):
    return f"<h6 style='text-align: {text_align};" \
           f"color: {color}; font-size: 17px; line-height: 1.8;; font-family: Trebuchet MS;'>{text}</h6>"


def set_text_with_dots(text):
    # Replace '.' with '.<br>' to add a line break after every period
    formatted_text = text.replace('.', '.<br> 🍴 ')
    return f"<div style='border: 2px solid #20115E; border-radius: 10px; padding: 15px;'>" \
           f"<h6 style='text-align: left;" \
           f"color: #20115E; font-size: 17px; line-height: 1.8; font-family: Trebuchet MS;'>🍴 {formatted_text}</h6>" \
           f"</div>"


def set_button(buttons_right="-260", margin_top="10"):
    st.markdown(
        f"""
            <style>
                .stButton>button {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #FFFFFF;
                    background-color: #25374A;
                    border-radius: 25px;
                    width: 200px;
                    height: 50px;
                    position: relative;
                    right: {buttons_right}px;
                    margin-top: {margin_top}px;
                    justify-content: center;
                    border: 2px solid white;
                }}
                .stButton>button:hover {{
                    background-color: #325375;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                }}
                .stButton > button:active {{
                    background-color: #6BA3A7;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                    position: relative;
                    top: 3px;
                }}
            </style>
            """
        , unsafe_allow_html=True)


def set_button_list(buttons_right="-260", margin_top="0"):
    st.markdown(
        f"""
            <style>
                .stButton>button {{
                    font-size: 20px;
                    font-weight: bold;
                    color: black;
                    background-color: #00FF49;
                    border-radius: 25px;
                    width: 200px;
                    height: 50px;
                    position: relative;
                    right: {buttons_right}px;
                    margin-top: {margin_top}px;
                    justify-content: center;
                }}
                .stButton>button:hover {{
                    background-color: #00FF49;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                }}
                .stButton > button:active {{
                    background-color: #00FF49;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                    position: relative;
                    top: 3px;
                }}
            </style>
            """
        , unsafe_allow_html=True)


def set_custom_button():
    css_style = f"""    
                    button{{
                    background-color: rgba(255, 255, 255, 0.5);
                    border: 1px solid #D3D3D3;   
                    font-size: 10px;
                    height: 0px;
                    right: 0px;
                    width: 100px;
                    color: #25374A;
                    margin-top: -8px;    
                    font-weight: bold;    
                    display: block;  }}
                    .stButton > button:hover {{  
                    color: red;
                }}
                    """

    return css_style


def set_download_button(buttons_right="-260", margin_top="10"):
    st.markdown(
        f"""
            <style>
                .stDownloadButton> button {{
                    font-size: 20px; 
                    font-weight: bold;
                    color: white; 
                    background-color: #25374A; 
                    border-radius: 25px;
                    width: 200px;
                    height: 50px;
                    position: relative;  
                    right: {buttons_right}px; 
                    margin-top: {margin_top}px;
                    justify-content: center;
                }}
                .stDownloadButton> button :hover {{
                    background-color: #325375;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                }}
                .stDownloadButton> button :active {{  
                    background-color: #325375;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                    position: relative;  
                    top: 3px;  
                }}
            </style>
            """
        , unsafe_allow_html=True)

def set_logo(logo_width="350px"):
    logo_path = os.path.join('layout', 'logo2.png')
    img_base64 = get_base64(logo_path)
    st.markdown(f"""
        <style>
            .center {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 20vh;
            }}
            .logo {{
                width: {logo_width};
            }}
        </style>
        <div class="center">
            <img src="data:image/png;base64,{img_base64}" class="logo">
        </div>
    """, unsafe_allow_html=True)
