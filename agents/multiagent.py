import operator
from typing import TypedDict, Annotated, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
import os
from  google import genai
# --- CONFIGURATION ---
# Replace with your actual key or load from os.environ
# GEMINI_API_KEY = "Your-Key-Here" 
try:
    from agents.config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY =  os.getenv("GEMINI_API_KEY")


MODEL="gemini-2.5-flash"
llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0,google_api_key=GEMINI_API_KEY)

# --- 1. DEFINE STATE ---
class AgenticState(TypedDict):
    # Inputs
    image_data: Optional[str] # Placeholder for image bytes/url
    extracted_text: str       # The raw ingredients text
    user_persona: str         # "Athlete", "Parent", etc.
    
    # Internal Reports
    scientist_report: Optional[str]
    coach_report: Optional[str]
    
    # Final Outputs
    final_verdict: str
    ui_mode: str              # SAFE, WARNING, TRADEOFF

# --- 2. MOCK DATA (The "Reasoning" Anchor) ---
MOCK_KG = {
    "aspartame": "Risk: Headaches & Gut sensitivity",
    "sugar": "Risk: High Glycemic Index (Spikes Insulin)",
    "peanuts": "Risk: Severe Allergen (Anaphylaxis)",
    "caffeine": "Risk: Anxiety/Jitters",
    "protein": "Benefit: Muscle Repair"
}

# --- 3. DEFINE NODES ---



# --- 3. THE EXTRACTOR NODE (Vision Specialist) ---
client = genai.Client(api_key=GEMINI_API_KEY)

class Extractor:
    def __init__(self, llm=None):
        # We don't need the 'llm' argument anymore for this specific node
        # because we use the native 'client' defined above.
        pass

    def invoke(self, state: AgenticState):
        image_path = state["image_data"]
        
        # 1. Validation
        if not image_path:
            return {"extracted_text": "No image provided."}
        
        print(f"👀 Extractor: Uploading {image_path} to Gemini...")
        
        
        my_file = client.files.upload(file=image_path)
        response = client.models.generate_content(
        model=MODEL,
        contents=[my_file, "return text in the image"])

        print(response.text)
        print("👀 Extractor: Text extraction complete.")
        return {"extracted_text": response.text}
            
       

class Scientist:
    def __init__(self, llm):
        self.llm = llm
        
    def invoke(self, state: AgenticState):
        ingredients = state["extracted_text"].lower()
        
        # 1. Check Mock KG (Grounding)
        known_risks = [f"{k.upper()}: {v}" for k, v in MOCK_KG.items() if k in ingredients]
        
        # 2. Reasoning Prompt
        prompt = f"""You are a strict Toxicologist. 
        Analyze these ingredients: {ingredients}
        
        Known Graph Data: {known_risks}
        
        If you see a known risk, HIGHLIGHT IT. 
        If it's mostly chemical/processed, say so.
        Be cold and factual.
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        print("🧪 Scientist: Report Generated.")
        return {"scientist_report": response.content}

class Coach:
    def __init__(self, llm):
        self.llm = llm
        
    def invoke(self, state: AgenticState):
        persona = state["user_persona"]
        ingredients = state["extracted_text"]
        
        # 1. Intent-First Logic
        prompt = f"""You are a Nutrition Coach for a {persona}.
        The user wants to know if they should eat this.
        Ingredients: {ingredients}
        
        Ignore minor chemicals. Focus on the GOAL.
        - Athlete: Wants protein/energy.
        - Parent: Wants safety.
        
        Is this good for them?
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        print(f"💪 Coach: Analysis for {persona} done.")
        return {"coach_report": response.content}

class Synthesizer:
    def __init__(self, llm):
        self.llm = llm
        
    def invoke(self, state: AgenticState):
        sci = state["scientist_report"]
        coach = state["coach_report"]
        
        # The Decision Matrix Prompt
        prompt = f"""You are the Final Judge.
        Scientist Report: {sci}
        Coach Report: {coach}
        
        RULES:
        1. If Scientist says TOXIC/ALLERGEN -> ui_mode="WARNING"
        2. If Scientist dislikes it but Coach likes it -> ui_mode="TRADEOFF"
        3. If both agree it's good -> ui_mode="SAFE"
        
        OUTPUT FORMAT:
        Verdict: [One short sentence]
        Mode: [SAFE / WARNING / TRADEOFF]
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        # Simple parsing (You can make this more robust with JSON later)
        mode = "TRADEOFF"
        if "SAFE" in content: mode = "SAFE"
        if "WARNING" in content: mode = "WARNING"
        
        print(f"⚖️ Synthesizer: Verdict is {mode}")
        return {"final_verdict": content, "ui_mode": mode}

# --- 4. BUILD THE GRAPH ---

# Initialize Instances
extracter_node = Extractor()
scientist_node = Scientist(llm)
coach_node = Coach(llm)
synthesizer_node = Synthesizer(llm)

builder = StateGraph(AgenticState)

# Add Nodes
builder.add_node("extracter", extracter_node.invoke)
builder.add_node("scientist", scientist_node.invoke)
builder.add_node("coach", coach_node.invoke)
builder.add_node("synthesizer", synthesizer_node.invoke)

# --- KEY FIX: PARALLEL WIRING ---
# Your diagram shows the Extractor feeds BOTH Scientist and Coach.
# We do not want Scientist -> Coach (that's sequential).
# We want them to run efficiently in parallel.

builder.add_edge(START, "extracter")

# Fan Out: Extractor -> Scientist AND Coach
builder.add_edge("extracter", "scientist")
builder.add_edge("extracter", "coach")

# Fan In: Scientist AND Coach -> Synthesizer
builder.add_edge("scientist", "synthesizer")
builder.add_edge("coach", "synthesizer")

builder.add_edge("synthesizer", END)

# Compile
app = builder.compile()

# --- 5. RUN IT (TEST) ---
if __name__ == "__main__":
    test_input = {
        "image_data": "/home/laky/Desktop/hackathon/medicai/agents/coke.jpg", 
        "user_persona": "Athlete"
    }
    
    result = app.invoke(test_input)
    
    print("\n--- FINAL OUTPUT ---")
    print(f"UI Mode: {result['ui_mode']}")
    print(f"Verdict: {result['final_verdict']}")