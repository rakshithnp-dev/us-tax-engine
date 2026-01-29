# 🗺️ US Tax Engine

An enterprise-grade US Tax Compliance Engine built with Streamlit and Plotly. This application helps businesses monitor economic nexus exposure across US states and calculate real-time tax rates based on geolocation.

## 🌟 Features

- **Economic Nexus Monitor**: Visualize tax liability across the USA using an interactive choropleth heatmap.
- **Real-Time Rate Calculator**: Simulate tax determination calls for specific zip codes (e.g., Beverly Hills, New York, Miami).
- **Interactive Reports**: Detailed tax breakdowns and audit-ready data visualizations.
- **JSON API Simulation**: Preview the raw data payloads used in enterprise tax determination.

## 🚀 Live Demo

🔗 **Deployed on Azure**: [Your Azure URL will be here]

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## 🛠️ Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/us-tax-engine.git
   cd us-tax-engine
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

## 🎯 Usage

### Economic Nexus Monitor
1. Navigate to the **Economic Nexus Monitor** tab.
2. Upload a sales CSV file with columns `state_code` and `amount`.
3. View the interactive map indicating where your business has triggered tax obligations.

### Real-Time Rate Calculator
1. Navigate to the **Real-Time Rate Calculator** tab.
2. Enter a supported Zip Code (e.g., `90210`, `10001`, `73301`).
3. Enter the transaction amount to see the tax breakdown between state and city jurisdictions.

## 🏗️ Project Structure

```
us-tax-engine/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── startup.sh           # Azure App Service startup script
├── .deployment          # Azure deployment config
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## ☁️ Azure Deployment

This application is configured for easy deployment to Azure App Service using the ZIP deployment method.

### Deployment Steps

1. Create an Azure App Service (Python 3.11, Linux).
2. Enable Basic Auth in Azure Configuration (if using ZIP deployment script).
3. Push code to GitHub.
4. Deploy using the provided ZIP deployment scripts.

## 📝 License

This project is open-source and available under the MIT License.

## 📧 Support

For questions or issues, please open a GitHub issue.

---

Built with ❤️ using Streamlit and Plotly | Deployed on Azure
