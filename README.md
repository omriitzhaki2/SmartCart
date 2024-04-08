<h1 id="title">SmartCart</h1>

<p id="description">Welcome to SmartCart! An innovative solution revolutionizing your supermarket shopping experience. SmartCart simplifies the pre-buying process and optimizes in-store shopping through a user-friendly interface. Our system is designed to enhance every aspect of your grocery trip, from creating personalized shopping lists to navigating the store efficiently.

To get started with SmartCart and transform your shopping experience, follow the link: https://smartcart1.streamlit.app/ </p>

<img src="https://github.com/omriitzhaki2/SmartCart/blob/be6ba95fd6e848ef0ba358665b91532d5036a10a/layout/logo2.png" width="250" align="center"/>

<h2>🛠️ Installation Steps:</h2>

<p id="description">You don't have to run our app local. You can simply use our public link. </p>

<p id="description">To use the app, you'll need to set up three keys: Firebase, Google API, and OpenAI Replace the existing st.secret lines in file utils.py with your corresponding keys in the following locations: </p>

<p id="description">Line 36- Replace with your Firebase key:</p>

```
FIREBASE_JSON = st.secrets['FIREBASE_JSON']
```
<p id="description">Line 44- Replace with your Google API key:</p>

```
api_key = st.secrets['GOOGLE_API']
```

<p id="description">Line 61- Replace with your OpenAI key:</p>

```
OPENAI_KEY = st.secrets['OPENAI_KEY']
```

<p>Then, Run the app and enjoy!:</p>

```
streamlit run main.py
```
