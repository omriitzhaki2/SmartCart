import streamlit as st
import base64

streamlit_style = """ <style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
html, body, [class*="css"]  {
font-family: 'Roboto', sans-serif;
}
</style>
"""


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
           f"color: #20115E';>{title}</h1>"


def set_subtitle(subtitle, text_align='center'):
    return f"<h2 style='text-align: {text_align}; " \
           f"color: #20115E'>{subtitle}</h2>"


def set_subsubtitle(subsubtitle, text_align='center'):
    return f"<h3 style='text-align: {text_align}; " \
           f"color: #20115E'>{subsubtitle}</h3>"


def set_text(text, text_align='center'):
    return f"<h6 style='text-align: {text_align};" \
           f"color: #20115E'>{text}</h6>"


def set_text_with_dots(text):
    # Replace '.' with '.<br>' to add a line break after every period
    formatted_text = text.replace('.', '.<br>')
    return f"<h6 style='text-align: left;" \
           f"color: #20115E'>{formatted_text}</h6>"


def set_button(buttons_right="-260", margin_top="10"):
    st.markdown(
        f"""
            <style>
                .stButton>button {{
                    font-size: 20px;
                    font-weight: bold;
                    color: black;
                    background-color: #6BA3A7;
                    border-radius: 25px;
                    width: 200px;
                    height: 50px;
                    position: relative;
                    right: {buttons_right}px;
                    margin-top: {margin_top}px;
                    justify-content: center;
                }}
                .stButton>button:hover {{
                    background-color: #2C8896;
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

def set_download_button(buttons_right="-260", margin_top="10"):
    st.markdown(
        f"""
            <style>
                .stDownloadButton> button {{
                    font-size: 20px; 
                    font-weight: bold;
                    color: black; 
                    background-color: #6BA3A7; 
                    border-radius: 25px;
                    width: 200px;
                    height: 50px;
                    position: relative;  
                    right: {buttons_right}px; 
                    margin-top: {margin_top}px;
                    justify-content: center;
                }}
                .stDownloadButton> button :hover {{
                    background-color: #2C8896;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                }}
                .stDownloadButton> button :active {{  
                    background-color: #6BA3A7;
                    color: #FFFFFF;
                    border-color: #FFFFFF;
                    position: relative;  
                    top: 3px;  
                }}
            </style>
            """
        , unsafe_allow_html=True)

def set_logo(logo_width="200px"):
    logo_path = f'layout\logo_new.png'
    img_base64 = get_base64(logo_path)
    st.markdown(f"""
        <style>
            .center {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 20vh; /* Use the full height of the viewport */
            }}
            .logo {{
                width: {logo_width};
            }}
        </style>
        <div class="center">
            <img src="data:image/png;base64,{img_base64}" class="logo">
        </div>
    """, unsafe_allow_html=True)





