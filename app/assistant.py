import os
import google.generativeai as genai
from .calculator import FootprintResult

def get_insights(footprint: FootprintResult) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_google_gemini_api_key_here":
        return "⚠️ **GEMINI_API_KEY is not set.** Cannot provide dynamic insights. Please add your key to the `.env` file and restart the server."
    
    try:
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for speed and efficiency as per instructions
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        prompt = f"""
        The user has a monthly carbon footprint breakdown as follows:
        - Transport: {footprint.transport_co2_lbs} lbs CO2
        - Energy: {footprint.energy_co2_lbs} lbs CO2
        - Diet: {footprint.diet_co2_lbs} lbs CO2
        - Total: {footprint.total_co2_lbs} lbs CO2
        
        You are a smart, dynamic sustainability assistant. Analyze this footprint and provide exactly 3 highly practical, 
        real-world actions the user can take to reduce their emissions. Focus primarily on their highest emission category.
        Format your response beautifully using Markdown with bolding and bullet points. Be encouraging and concise.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"**Error generating insights:** {str(e)}"

def get_chat_response(message: str, history: list) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_google_gemini_api_key_here":
        return "⚠️ **GEMINI_API_KEY is not set.**"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        formatted_history = []
        for msg in history:
            role = 'user' if msg['role'] == 'user' else 'model'
            formatted_history.append({'role': role, 'parts': [msg['content']]})
            
        chat_session = model.start_chat(history=formatted_history)
        
        system_prompt = "You are a friendly, expert sustainability and carbon footprint assistant. Keep your answers concise, practical, and highly relevant."
        response = chat_session.send_message(f"{system_prompt}\n\nUser: {message}")
        return response.text
    except Exception as e:
        return f"**Error generating chat response:** {str(e)}"
