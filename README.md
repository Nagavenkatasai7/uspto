# USPTO Opposition Trademark Scraper ⚖️

A comprehensive web application for retrieving and analyzing US and International trademark classes from USPTO opposition proceedings.

## 🌟 Features

- **Opposition Data Retrieval**: Fetch trademark data from USPTO opposition proceedings
- **Class Analysis**: Extract US and International trademark classes
- **Mark Type Classification**: AI-powered classification using Claude Vision API
  - Standard Text (Type 1)
  - Stylized/Design (Type 2)
  - Slogan (Type 3)
- **Comprehensive Reports**: Generate detailed Excel and JSON reports
- **Batch Processing**: Analyze multiple oppositions from party searches or URLs
- **Visual Dashboard**: Interactive Streamlit interface with progress tracking

## 📋 Requirements

- Python 3.8+
- USPTO API Key
- Anthropic (Claude) API Key for image classification

## 🚀 Quick Start (Streamlit Cloud)

**No installation needed!** Deploy directly to Streamlit Cloud:

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub account
3. Deploy this repository: `Nagavenkatasai7/uspto`
4. Add your API keys in the Secrets section (see Usage section below)

## 🚀 Local Installation

1. Clone the repository:
```bash
git clone https://github.com/Nagavenkatasai7/uspto.git
cd uspto
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
   - Copy `.env.example` to `.env`
   - Add your actual API keys to the `.env` file:
     ```
     USPTO_API_KEY=your_actual_uspto_key
     ANTHROPIC_API_KEY=your_actual_anthropic_key
     ```
   - **Important**: Never commit the `.env` file to GitHub (it's already in `.gitignore`)

## 💻 Usage

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. **Fork or use this repository**
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Sign in with GitHub**
4. **Click "New app"**
5. **Select your repository: `Nagavenkatasai7/uspto`**
6. **Set main file path: `web_app.py`**
7. **Click "Advanced settings" > "Secrets"**
8. **Add your API keys in TOML format:**
   ```toml
   USPTO_API_KEY = "your_actual_uspto_key"
   ANTHROPIC_API_KEY = "your_actual_anthropic_key"
   ```
9. **Click "Deploy"**

Your app will be live at: `https://[your-app-name].streamlit.app` 🚀

### Option 2: Run Locally

Run the Streamlit web interface:
```bash
streamlit run web_app.py
```

### Command Line Script

Run the Python scraper directly:
```bash
python uspto_opposition_scraper.py
```

## 📊 Output Formats

The application generates reports in multiple formats:

- **Excel (.xlsx)**: Detailed trademark class data with summary sheets
- **JSON (.json)**: Structured data for programmatic access
- **Copyable Text**: Tab-separated format for direct Excel pasting

## 🔧 Key Components

### `web_app.py`
Streamlit web application with interactive UI for:
- Single opposition searches
- Party name searches
- URL-based batch processing
- Real-time progress tracking
- Download capabilities

### `uspto_opposition_scraper.py`
Core scraper class with methods for:
- TTABVue data extraction
- TSDR API integration
- Mark image classification
- Class aggregation
- Result formatting

## 📖 API Integration

### USPTO TSDR API
- Retrieves trademark status data
- Fetches US and International classes
- Downloads trademark images

### Anthropic Claude API
- Analyzes trademark images
- Classifies mark types
- Detects visual elements and text

## 🛠️ Technologies

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **BeautifulSoup**: HTML parsing for TTABVue
- **Pandas**: Data manipulation and Excel export
- **Anthropic SDK**: Claude AI integration
- **Requests**: HTTP client for API calls

## 📝 Data Fields

The application extracts:
- Serial numbers and mark names
- Filing and termination dates
- US and International classes
- Mark types and descriptions
- Opposition results (Sustained/Dismissed)
- Party information (Plaintiff/Defendant)

## ⚠️ Rate Limiting

The scraper implements rate limiting to respect USPTO API limits:
- 0.75s delay between TSDR API calls
- Retry logic with exponential backoff
- Timeout handling for slow responses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Nagavenkatasai7

## 🙏 Acknowledgments

- USPTO for providing the TSDR API and TTABVue interface
- Anthropic for the Claude AI API
- Streamlit for the web framework

---

**Note**: This tool is for research and educational purposes. Ensure compliance with USPTO's terms of service and rate limits.

