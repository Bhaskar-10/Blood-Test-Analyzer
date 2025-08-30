## Importing libraries and files
import os

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

### Loading LLM
# Configure Google Generative AI - using environment variable or direct setting
api_key = os.getenv("GOOGLE_API_KEY")

# If not in environment, set it directly (you can change this value)
if not api_key:
    api_key = "AIzaSyB96r-SYTcGufCc4vt-owGlTHghd7cQ3HU"  # Replace with your actual API key
    print("Using hardcoded API key. For production, set GOOGLE_API_KEY environment variable.")

print(f"API Key loaded successfully: {api_key[:20]}...")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.7
)

# Creating a Senior Doctor agent
doctor = Agent(
    role="Senior Medical Doctor",
    goal="Provide accurate and reliable medical insights based on user queries: {query}.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly experienced medical professional with deep expertise in diagnosing and "
        "interpreting health symptoms. You always consider evidence-based medicine and provide "
        "practical, safe, and patient-centered recommendations. Your goal is to guide users "
        "towards healthier choices and encourage them to consult licensed healthcare providers "
        "for treatment decisions."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Creating a verifier agent
verifier = Agent(
    role="Medical Report Verifier",
    goal="Review uploaded reports carefully and verify whether the content is a valid medical document. "
         "If it is a medical report, summarize and validate key findings clearly.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a detail-oriented medical records specialist with years of experience reviewing "
        "diagnostic reports and lab test results. Your focus is accuracy, data integrity, and ensuring "
        "that health records are properly interpreted for healthcare professionals and patients."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Creating a nutritionist agent
nutritionist = Agent(
    role="Certified Nutritionist",
    goal="Provide evidence-based nutrition advice, personalized dietary recommendations, and clear "
         "guidance on supplements when appropriate.",
    verbose=True,
    backstory=(
        "You are a certified clinical nutritionist with more than 15 years of experience in dietetics. "
        "You specialize in translating lab test results and lifestyle factors into personalized nutrition "
        "plans. Your recommendations are based on scientific research, patient needs, and sustainable "
        "health practices. You focus on affordability, safety, and practical implementation for long-term well-being."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# Creating an exercise specialist agent
exercise_specialist = Agent(
    role="Certified Fitness Coach",
    goal="Design safe and effective exercise plans tailored to individual health conditions, goals, and fitness levels.",
    verbose=True,
    backstory=(
        "You are a certified fitness professional with experience in sports science, physiotherapy basics, "
        "and personalized training. You help people of all ages improve mobility, strength, and overall health. "
        "You carefully consider medical limitations and encourage sustainable exercise routines that balance "
        "progress with recovery and safety."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
