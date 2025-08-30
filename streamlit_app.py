import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Blood Test Analyzer",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .result-section {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-bottom: 1.5rem;
    }
    .highlight-section {
        background-color: #fff3cd;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin-bottom: 1.5rem;
    }
    .error-section {
        background-color: #f8d7da;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<h1 class="main-header">🩸 Blood Test Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">Upload your blood test report and get AI-powered analysis</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # API Configuration
        api_url = st.text_input(
            "API URL",
            value="http://localhost:8000",
            help="URL of your FastAPI backend"
        )

        # Query customization
        default_query = st.text_area(
            "Custom Query",
            value="Summarise my Blood Test Report and provide health recommendations",
            height=100,
            help="Customize the analysis request"
        )

        st.subheader("🔍 Search Past Reports")
        search_query = st.text_input("Enter a search query")
        if st.button("Search History"):
            try:
                resp = requests.get(f"{api_url}/search", params={"query": search_query, "top_k": 3})
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown("### 🔎 Search Results")
                    for doc, meta in zip(data["documents"][0], data["metadatas"][0]):
                        st.markdown(f"**Query:** {meta['query']}")
                        st.markdown(f"**File:** {meta['file_name']}")
                        st.markdown(f"**Analysis Snippet:** {doc[:300]}...")
                        st.markdown("---")
                else:
                    st.error(f"❌ API Error: {resp.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")

        st.subheader("ℹ️ About")
        st.markdown("""
        This application uses AI to analyze blood test reports and provide:
        - 📊 Report summary
        - 🏥 Health recommendations
        - 💊 Potential concerns
        - 🥗 Lifestyle suggestions
        """)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h2 class="sub-header">📁 Upload Blood Test Report</h2>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload your blood test report in PDF format"
        )

        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📄 File size: {uploaded_file.size} bytes")

        if uploaded_file is not None:
            if st.button("🔍 Analyze Report", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your blood test report..."):
                    try:
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                        data = {'query': default_query, 'user_id': 'guest123'}

                        response = requests.post(
                            f"{api_url}/analyze",
                            files=files,
                            data=data,
                            timeout=120
                        )

                        if response.status_code == 200:
                            result = response.json()

                            # Display results
                            st.markdown('<h2 class="sub-header">📊 Analysis Results</h2>', unsafe_allow_html=True)

                            if "Query-Specific Result" in result.get("analysis", ""):
                                # Highlight specific marker queries
                                st.markdown('<div class="highlight-section">', unsafe_allow_html=True)
                                st.markdown(f"**🔍 Query:** {result.get('query', 'N/A')}")
                                st.markdown(f"**📄 File Processed:** {result.get('file_processed', 'N/A')}")
                                st.markdown("**📋 Marker-Specific Analysis:**")
                                st.markdown(result.get("analysis", "No analysis available"))
                                st.markdown('</div>', unsafe_allow_html=True)

                            else:
                                # Full pipeline
                                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                                st.markdown(f"**🔍 Query:** {result.get('query', 'N/A')}")
                                st.markdown(f"**📄 File Processed:** {result.get('file_processed', 'N/A')}")
                                st.markdown("**📋 Analysis:**")
                                st.markdown(result.get("analysis", "No analysis available"))
                                st.markdown('</div>', unsafe_allow_html=True)

                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                            st.markdown('<div class="error-section">', unsafe_allow_html=True)
                            st.text(f"Error: {response.text}")
                            st.markdown('</div>', unsafe_allow_html=True)

                    except requests.exceptions.ConnectionError:
                        st.error("❌ Connection Error")
                        st.markdown('<div class="error-section">', unsafe_allow_html=True)
                        st.markdown("Unable to connect to the API server. Ensure backend is running.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    except requests.exceptions.Timeout:
                        st.error("⏰ Request Timeout")
                        st.markdown('<div class="error-section">', unsafe_allow_html=True)
                        st.markdown("The analysis took too long. Please try again.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"❌ Unexpected Error: {str(e)}")
                        st.markdown('<div class="error-section">', unsafe_allow_html=True)
                        st.markdown(f"An unexpected error occurred: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h2 class="sub-header">📈 Quick Stats</h2>', unsafe_allow_html=True)
        st.metric("Reports Analyzed", "0")
        st.metric("Success Rate", "0%")
        st.metric("Avg. Response Time", "0s")

        st.markdown('<h3>📋 Instructions</h3>', unsafe_allow_html=True)
        st.markdown("""
        1. **Upload** your blood test PDF  
        2. **Customize** the analysis query (optional)  
        3. **Click** Analyze Report  
        4. **Review** the AI-generated analysis  
        """)

        st.markdown('<h3>💡 Tips</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Ensure PDF is clear and readable  
        - Include all relevant test results  
        - Customize query for specific concerns  
        - Review results with a healthcare provider  
        """)


if __name__ == "__main__":
    main()
