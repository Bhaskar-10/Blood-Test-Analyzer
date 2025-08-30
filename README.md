# 🩸 Blood Test Analyzer - Streamlit Frontend

A beautiful and user-friendly web interface for the Blood Test Analyzer application.

## 🚀 Quick Start

### Install dependencies
```bash
# Install dependencies
pip install -r requirements.txt

```

### Start
```bash
# Terminal 1: Start the FastAPI backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start the Streamlit frontend
streamlit run streamlit_app.py --server.port 8501
```

## 🌐 Access Points

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## ✨ Features

### 🎨 Beautiful UI
- Modern, responsive design
- Intuitive file upload interface
- Real-time progress indicators
- Professional styling with custom CSS

### ⚙️ Configuration Options
- **API URL**: Configure backend endpoint
- **Custom Queries**: Personalize analysis requests
- **File Type Validation**: PDF upload support

### 📊 Analysis Results
- Structured result display
- Query tracking
- File processing confirmation
- Error handling with helpful messages

### 🔧 Sidebar Features
- Settings panel
- Instructions and tips
- Quick statistics
- About section

## 📁 File Structure

```
blood-test-analyser-debug/
├── streamlit_app.py          # Main Streamlit application
├── start_app.py             # Startup script for both services
├── main.py                  # FastAPI backend
├── agents.py                # AI agents configuration
├── task.py                  # Task definitions
├── tools.py                 # Tool definitions
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (API key)
```

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   ```bash
   # Create .env file with your Google API key
   echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
   ```

3. **Start the Application**:
   ```bash
   python start_app.py
   ```

## 🎯 Usage

1. **Open the Frontend**: Navigate to http://localhost:8501
2. **Upload PDF**: Drag and drop or select a blood test report PDF
3. **Customize Query**: Modify the analysis request in the sidebar (optional)
4. **Analyze**: Click "Analyze Report" button
5. **Review Results**: View the AI-generated analysis

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Generative AI API key

### Streamlit Configuration
The frontend can be customized by modifying `streamlit_app.py`:
- Change default API URL
- Modify styling (CSS)
- Add new features
- Customize error messages

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**:
   - Ensure the FastAPI backend is running on port 8000
   - Check the API URL in the sidebar settings

2. **File Upload Issues**:
   - Ensure the file is a valid PDF
   - Check file size (should be reasonable)

3. **API Key Issues**:
   - Verify your Google API key is correct
   - Ensure the `.env` file is in the project root

4. **Port Conflicts**:
   - Change ports in the startup script if needed
   - Check if ports 8000 and 8501 are available

### Debug Mode
```bash
# Run with debug information
streamlit run streamlit_app.py --logger.level debug
```

## 🎨 Customization

### Styling
Modify the CSS in `streamlit_app.py` to change the appearance:
```python
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #e74c3c;
        /* Add your custom styles */
    }
</style>
""", unsafe_allow_html=True)
```

### Adding Features
- Add new analysis options in the sidebar
- Implement file validation
- Add result export functionality
- Include user authentication

## 📈 Performance Tips

1. **File Size**: Keep PDF files under 10MB for optimal performance
2. **API Timeout**: The frontend waits up to 120 seconds for analysis
3. **Caching**: Streamlit automatically caches results for better performance

## 🔒 Security Notes

- API keys are stored locally in `.env` file
- File uploads are processed securely
- No data is stored permanently on the server
- All communication uses HTTPS when deployed

## 🚀 Deployment

### Local Development
```bash
python start_app.py
```

### Production Deployment
1. Set up a production server
2. Configure environment variables
3. Use a process manager (PM2, Supervisor)
4. Set up reverse proxy (Nginx)
5. Enable HTTPS

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at http://localhost:8000/docs
3. Check the console logs for error messages

---

**Happy Analyzing! 🩸✨**
