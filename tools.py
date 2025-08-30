import os
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool

# ---------------- TOOLS ---------------- #

@tool
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    """Read data from a PDF file"""
    try:
        docs = PyPDFLoader(file_path=path).load()
        full_report = "\n".join([d.page_content.strip() for d in docs])
        return full_report.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# --------- Value Extraction Helpers --------- #

def _extract_value(text: str, marker: str, pattern: str, normal_range: tuple):
    """Find a marker value, compare to normal range, return status string"""
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            value = float(match.group(1))
            low, high = normal_range
            if value < low:
                status = "Low"
            elif value > high:
                status = "High"
            else:
                status = "Normal"
            return f"{marker}: {value} → {status} (Normal range: {low}-{high})"
        except:
            return f"{marker}: Value found but could not parse."
    return None


def _summarize_values(text: str):
    """Summarize key blood markers"""
    results = []

    # Hemoglobin (g/dL)
    hemoglobin = _extract_value(text, "Hemoglobin", r"Hemoglobin[:\s]+([\d\.]+)", (12, 16))
    if hemoglobin: results.append(hemoglobin)

    # Vitamin D (ng/mL)
    vitamin_d = _extract_value(text, "Vitamin D", r"Vitamin\s*D[:\s]+([\d\.]+)", (20, 50))
    if vitamin_d: results.append(vitamin_d)

    # Glucose (mg/dL)
    glucose = _extract_value(text, "Glucose", r"Glucose[:\s]+([\d\.]+)", (70, 100))
    if glucose: results.append(glucose)

    # Cholesterol (mg/dL)
    cholesterol = _extract_value(text, "Cholesterol", r"Cholesterol[:\s]+([\d\.]+)", (0, 200))
    if cholesterol: results.append(cholesterol)

    return results if results else ["No numeric lab values detected."]


# --------- Nutrition Analysis --------- #

@tool
def analyze_nutrition_tool(blood_report_data: str) -> str:
    """Analyze nutrition based on blood report data"""
    if not blood_report_data or "Error" in blood_report_data:
        return "No valid blood report data provided."

    findings = []
    if "Hemoglobin" in blood_report_data:
        findings.append("Ensure iron/B12/folate intake if hemoglobin is low.")
    if "Vitamin D" in blood_report_data:
        findings.append("Low Vitamin D → sunlight exposure and supplements if prescribed.")
    if "Cholesterol" in blood_report_data:
        findings.append("High cholesterol → reduce saturated fats, increase fiber.")
    if "Glucose" in blood_report_data:
        findings.append("Abnormal glucose → limit sugars, eat balanced carbs.")

    if not findings:
        findings.append("No specific nutrition markers found in the report.")

    return "🧑‍⚕️ Nutrition Insights:\n- " + "\n- ".join(findings)


# --------- Exercise Planning --------- #

@tool
def create_exercise_plan_tool(blood_report_data: str) -> str:
    """Create exercise plan based on blood report data"""
    if not blood_report_data or "Error" in blood_report_data:
        return "No valid blood report data provided."

    recommendations = [
        "Include at least 30 minutes of walking or light cardio daily.",
        "2–3 strength training sessions per week.",
        "2–3 flexibility sessions (stretching or yoga).",
        "Rest 1–2 days per week."
    ]

    if "Cholesterol" in blood_report_data:
        recommendations.append("Prioritize aerobic exercise for cholesterol management.")
    if "Vitamin D" in blood_report_data:
        recommendations.append("Add outdoor exercise for natural Vitamin D exposure.")

    return "🏋️ Exercise Plan:\n- " + "\n- ".join(recommendations)


# ---------------- PIPELINE FUNCTION ---------------- #

def process_report(query: str, file_path: str):
    """Main pipeline to read, analyze and generate recommendations"""
    report = read_data_tool(file_path)
    if "Error" in report or not report:
        return {
            "query": query,
            "file_processed": "N/A",
            "analysis": "No analysis available"
        }

    # 📊 Report Summary (with values)
    summary_lines = _summarize_values(report)
    summary = "📊 Report Summary:\n" + "\n".join(f"- {line}" for line in summary_lines)

    # 🏥 Health Recommendations
    nutrition = analyze_nutrition_tool(report)

    # 🥗 Lifestyle (exercise)
    exercise = create_exercise_plan_tool(report)

    return {
        "query": query,
        "file_processed": file_path,
        "analysis": f"{summary}\n\n{nutrition}\n\n{exercise}"
    }
    