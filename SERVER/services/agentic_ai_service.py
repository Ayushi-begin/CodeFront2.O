from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Updated import
from langgraph.graph import StateGraph, END  # ✅ Updated for latest LangGraph API
from services.weather_service import get_current_weather, get_forecast_weather
from config.db import report_db
from config.settings import Settings

# ✅ 1. Define Tools
@tool
def fetch_weather_tool(lat: float, lon: float) -> str:
    """Fetches current and forecast weather data for given coordinates."""
    current = get_current_weather(lat, lon)
    forecast = get_forecast_weather(lat, lon)

    summary = (
        f"Current weather in {current['city']}: {current['condition']}, "
        f"{current['temperature']}°C, humidity {current['humidity']}%, "
        f"wind {current['wind_speed']} m/s.\n"
        f"Upcoming forecast: "
        + ", ".join(
            [f"{day['date']} - {day['condition']} ({day['avg_temperature']}°C)" for day in forecast]
        )
    )
    return summary


@tool
def fetch_plant_history_tool(plant_name: str) -> str:
    """Fetches last few plant disease records from DB."""
    records = list(report_db["reports"].find({"disease": {"$regex": plant_name, "$options": "i"}}))
    if not records:
        return f"No records found for {plant_name}."
    response = []
    for rec in records[-3:]:
        response.append(f"{rec['disease']} ({rec['confidence']}%) - {rec['recommendation']}")
    return " | ".join(response)


@tool
def analyze_yolo_result_tool(disease: str, confidence: float) -> str:
    """Summarizes disease detection."""
    return f"The YOLO model detected {disease} with {confidence}% confidence."


# ✅ 2. Define LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.4,
    google_api_key=Settings.GEMINI_API_KEY  # ✅ explicitly pass the key
)


# ✅ 3. Define LangGraph State Schema
def agentic_node(state):
    """
    Combines all tools and reasoning to form a final analysis.
    """
    lat = state["lat"]
    lon = state["lon"]
    disease = state["disease"]
    confidence = state["confidence"]

    # Fetch contextual info
    weather_info = fetch_weather_tool.invoke({"lat": lat, "lon": lon})
    history_info = fetch_plant_history_tool.invoke({"plant_name": disease})
    yolo_info = analyze_yolo_result_tool.invoke({"disease": disease, "confidence": confidence})

    # Build prompt for Gemini
    query = (
        f"{yolo_info}\n\n"
        f"Weather Info: {weather_info}\n"
        f"Past Records: {history_info}\n\n"
        f"Based on these details, give recommendations in pointers like the weather now, suitable upcoming day, is it necessary to worry and the feritilizers for the plant's health and treatment, also use the past records of that plant. if the detected disease has the word healthy in it then it means there is no disease"
    )

    # Call Gemini model
    response = llm.invoke(query)
    return {"recommendation": response.content if hasattr(response, "content") else response}


# ✅ 4. Build LangGraph
graph = StateGraph(dict)
graph.add_node("agentic", agentic_node)
graph.set_entry_point("agentic")
graph.add_edge("agentic", END)


# ✅ 5. Run workflow
def run_agentic_analysis(lat: float, lon: float, disease: str, confidence: float):
    """
    Integrates YOLO + Weather + Plant History using LangGraph agent.
    """
    inputs = {
        "lat": lat,
        "lon": lon,
        "disease": disease,
        "confidence": confidence
    }
    result = graph.compile().invoke(inputs)
    return {"recommendation": result["recommendation"]}
