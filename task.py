## Importing libraries and files
from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist

## Creating a task to help solve user's query
help_patients = Task(
    description=(
        "Understand and address the user's medical query: {query}. "
        "Analyze the problem carefully, provide a clear explanation, and offer evidence-based "
        "guidance. Ensure that advice is safe, practical, and encourages users to seek "
        "professional consultation when necessary."
    ),
    expected_output=(
        "A detailed, user-friendly response including:\n"
        "- Summary of the query in simple terms\n"
        "- Possible explanations and considerations (non-diagnostic)\n"
        "- General safe recommendations\n"
        "- Clear disclaimer that professional consultation is required for treatment decisions"
    ),
    agent=doctor,
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description=(
        "Analyze the provided blood report or user query ({query}) to identify potential "
        "nutritional insights. Provide evidence-based dietary recommendations tailored to "
        "the findings, while ensuring safety and practicality. Focus on nutrition, hydration, "
        "and lifestyle habits rather than prescribing treatments."
    ),
    expected_output=(
        "A structured nutrition report including:\n"
        "- Key findings related to nutrition from the input\n"
        "- Foods to include for better health\n"
        "- Foods to limit or avoid\n"
        "- Guidance on supplements (only if necessary)\n"
        "- Practical tips for maintaining a balanced diet"
    ),
    agent=nutritionist,
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description=(
        "Develop a safe and effective exercise plan based on the user's query ({query}) "
        "and any health information provided. Recommendations should be personalized, "
        "consider medical limitations, and encourage sustainable habits. Ensure the plan "
        "balances strength, mobility, endurance, and rest."
    ),
    expected_output=(
        "A personalized exercise plan including:\n"
        "- Warm-up and stretching guidance\n"
        "- Recommended types of exercises (strength, cardio, flexibility)\n"
        "- Suggested weekly routine with safe intensity levels\n"
        "- Rest and recovery advice\n"
        "- Safety precautions and when to consult a professional"
    ),
    agent=exercise_specialist,
    async_execution=False,
)

## Creating a verification task
verification = Task(
    description=(
        "Carefully review the uploaded document to determine whether it is a medical report, "
        "such as a blood test, or another type of file. If it is medical, highlight key sections "
        "and confirm its validity. If not, provide a clear explanation."
    ),
    expected_output=(
        "A verification report including:\n"
        "- Whether the document is a medical report or not\n"
        "- Key observations (if medical)\n"
        "- Any inconsistencies or issues\n"
        "- A professional and concise conclusion"
    ),
    agent=verifier,
    async_execution=False,
)
