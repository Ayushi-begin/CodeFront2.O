import streamlit as st

def render():
    """
    Renders the landing page with flattened HTML, improved vertical spacing, 
    and a background image. Links now include &app=1 to prevent navigation resets.
    """
    
    bg_image_url = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=2000"

    html_code = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');

    /* ✅ HIDE SIDEBAR ONLY FOR LANDING PAGE */
    section[data-testid="stSidebar"] {{
        display: none;
    }}
    
    .stApp {{ 
        background: linear-gradient(to bottom, rgba(26, 92, 56, 0.85), rgba(5, 43, 22, 0.95)), url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Lato', sans-serif; 
        color: white; 
    }}
    
    .block-container {{ padding-top: 0 !important; padding-bottom: 5rem; max-width: 100% !important; padding-left: 1rem; padding-right: 1rem; }}
    header {{ visibility: hidden; }}

    /* ✅ NAVBAR WRAPPER */
    .navbar {{
        position: absolute;
        top: 20px;
        left: 30px;
        right: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
    }}
    
    .logo-container {{ display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.2rem; color: #dbece2; }}
    .logo-icon {{ background-color: #6bbf48; padding: 4px 8px; border-radius: 6px; color: #052b16; font-weight: 900; }}

    /* ✅ APP BUTTON */
    .app-btn {{
        background-color: #6bbf48;
        color: #0d3821;
        padding: 10px 26px;
        border-radius: 30px;
        font-weight: 700;
        text-decoration: none;
    }}
    
    .hero-container {{ 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        text-align: center; 
        padding: 100px 20px 80px 20px; 
        position: relative; 
    }}
    
    .main-title {{ 
        font-size: clamp(2.5rem, 5vw, 4.5rem); 
        font-weight: 400; 
        color: #eef5f1; 
        line-height: 1.1; 
        margin-bottom: 30px; 
    }}
    
    .highlight-text {{ color: #7bc758; font-weight: 700; }}
    
    .subtitle {{ 
        color: #aebfb5; 
        font-size: 1.1rem; 
        max-width: 700px; 
        line-height: 1.6; 
        margin: 0 auto 60px auto; 
    }}
    
    .cta-button {{ background-color: #6bbf48; color: #0d3821; padding: 16px 36px; border-radius: 50px; font-weight: 700; font-size: 1.1rem; text-decoration: none; display: inline-flex; align-items: center; gap: 12px; box-shadow: 0 4px 15px rgba(107, 191, 72, 0.3); transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; }}
    .cta-button:hover {{ transform: scale(1.05); background-color: #5dae4e; color: #0d3821; box-shadow: 0 6px 20px rgba(107, 191, 72, 0.5); }}
    
    .features-grid {{ 
        display: grid; 
        grid-template-columns: repeat(4, 1fr); 
        gap: 25px; 
        max-width: 1200px; 
        margin: 50px auto 0 auto; 
        padding: 20px; 
    }}
    
    .feature-card {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 40px 20px; text-align: center; display: flex; flex-direction: column; align-items: center; transition: transform 0.3s ease; height: 100%; }}
    .feature-card:hover {{ transform: translateY(-5px); background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.3); }}
    
    .icon-wrapper {{ width: 60px; height: 60px; background: rgba(255,255,255,0.05); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; color: #7bc758; }}
    .card-title {{ font-size: 1.1rem; font-weight: 700; color: #eef5f1; margin-bottom: 12px; }}
    .card-desc {{ font-size: 0.9rem; color: #aebfb5; line-height: 1.5; margin-bottom: 18px; }}

    .card-btn {{ font-size: 0.85rem; padding: 8px 18px; border-radius: 20px; background: rgba(107,191,72,0.15); border: 1px solid rgba(107,191,72,0.4); color: #7bc758; cursor: pointer; text-decoration: none; }}
    .card-btn:hover {{ background: rgba(107,191,72,0.3); }}

    @media (max-width: 900px) {{ .features-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 600px) {{ .features-grid {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 15px; padding-bottom: 20px; }} .feature-card {{ min-width: 260px; scroll-snap-align: center; }} .features-grid::-webkit-scrollbar {{ display: none; }} }}
</style>

<div class="navbar">
    <div class="logo-container">
        <div class="logo-icon">🌿</div>
        <span>PlantCare AI</span>
    </div>
    <a class="app-btn" href="?nav=Home&app=1" target="_self">App</a>
</div>

<div class="hero-container">
<div class="main-title">
Keep Your Plants <br>
<span class="highlight-text">Thriving & Healthy</span>
</div>
<p class="subtitle">
Get instant AI-powered diagnosis of your plant's health with weather insights. 
Simply upload a photo and receive expert care recommendations tailored to your local climate.
</p>
<a class="cta-button" href="?nav=Home&app=1" target="_self">
Check Your Plant's Health
</a>
</div>

<div class="features-grid">

<div class="feature-card">
<div class="icon-wrapper">📷</div>
<div class="card-title">Instant Scanning</div>
<div class="card-desc">Upload a photo and get results in seconds</div>
<a class="card-btn" href="?nav=Home&app=1" target="_self">Explore</a>
</div>

<div class="feature-card">
<div class="icon-wrapper">✨</div>
<div class="card-title">YOLO Model Analysis</div>
<div class="card-desc">Advanced Machine Learning model YOLO detect diseases and deficiencies</div>
<a class="card-btn" href="?nav=Results&app=1" target="_self">Learn More</a>
</div>

<div class="feature-card">
<div class="icon-wrapper">⛅</div>
<div class="card-title">Weather Insights</div>
<div class="card-desc">Real-time weather data for optimal plant care</div>
<a class="card-btn" href="?nav=Weather Insights&app=1" target="_self">View Weather</a>
</div>

<div class="feature-card">
<div class="icon-wrapper">🍃</div>
<div class="card-title">Agentic AI Recommendation</div>
<div class="card-desc">Get personalized care tips to restore plant health</div>
<a class="card-btn" href="?nav=Chatbot&app=1" target="_self">Get Advice</a>
</div>

</div>
"""
    st.markdown(html_code, unsafe_allow_html=True)