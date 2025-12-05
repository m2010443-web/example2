# 📊 Sales Analytics Platform

<div align="center">

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://example2-ibx2nkjc542tgeqhndvqym.streamlit.app/)

**Language / Язык:**

[![🇬🇧 English](https://img.shields.io/badge/lang-English-blue?style=for-the-badge)](README.md) [![🇷🇺 Русский](https://img.shields.io/badge/lang-Русский-red?style=for-the-badge)](README.ru.md)

---

*Interactive platform for sales data analysis*

</div>

---

## 📖 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Docker](#docker)
- [Demo Data](#demo-data)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## ✨ Features

- 📁 **Data Loading** - Support for CSV and Excel formats
- 🎬 **Demo Data** - 3 ready-to-use datasets for instant demo
- 📊 **Interactive Dashboards** - KPI metrics and visualizations
- 📈 **Advanced Analytics** - Correlations, grouping, top-N analysis
- 🎨 **Beautiful Charts** - Plotly for interactive visualizations
- 💾 **Data Export** - Download results in CSV format

---

## 🚀 Three Ways to Run

| Method | Description | Setup Time |
|--------|-------------|------------|
| 🌐 **Online** | Click the badge above | 0 minutes |
| 🐳 **Docker** | `docker-compose up` | 2 minutes |
| 💻 **From Source** | `pip install -r requirements.txt` | 3 minutes |

---

## 📦 Quick Start

### Option 1: Online (No Installation Required)
Click the **"Open in Streamlit"** badge at the top of this page!

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/example2-main.git
cd example2-main

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🐳 Docker

### Option 1: Docker Compose (Recommended)

**Prerequisites:**
- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

**Steps:**
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/example2-main.git
cd example2-main

# Start the application
docker-compose up

# Access the app at http://localhost:8501
```

**Stopping:**
```bash
# Press Ctrl+C in the terminal, or run:
docker-compose down
```

### Option 2: Manual Docker Build

```bash
# Build the Docker image
docker build -t sales-analytics .

# Run the container
docker run -p 8501:8501 sales-analytics

# Access the app at http://localhost:8501
```

### Useful Docker Commands

```bash
# View running containers
docker ps

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# View logs
docker logs <container_id>

# Clean up unused resources
docker system prune -a
```

---

## 🎬 Demo Data

The application includes 3 ready-to-use datasets for testing:

1. **📊 Detailed Sales** (2000 records)
   - Complete order information
   - Products, regions, and channels
   - Customer segments and sales representatives

2. **📅 Monthly Statistics** (12 months)
   - Aggregated monthly data for 2023
   - Revenue, orders, and customer metrics
   - Growth trends and patterns

3. **🏆 Top Products** (10 items)
   - Best-selling products ranked by revenue
   - Sales volume and ratings
   - Return rates and performance metrics

**How to use:** Simply select a dataset from the dropdown menu and click "Load Demo Data" - no files needed!

---

## 📊 Project Structure

```
example2-main/
├── app.py                 # Main Streamlit application
├── demo_data.py           # Demo data generator
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .dockerignore         # Docker build exclusions
├── README.md             # English documentation
├── README.ru.md          # Russian documentation
├── src/
│   ├── __init__.py
│   ├── data_loader.py    # Data loading and processing
│   ├── analysis.py       # Analytics functions
│   └── plotting.py       # Visualizations
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   └── test_plotting.py
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

---

## 🧪 Testing

```bash
# Install testing dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations |
| **NumPy** | Numerical computing |
| **OpenPyXL** | Excel file support |
| **Pytest** | Testing framework |
| **Docker** | Containerization |

---

## 📚 Usage Guide

### Loading Data
1. Launch the application
2. Choose between demo data or upload your own CSV/Excel file
3. Supported formats: `.csv`, `.xlsx`, `.xls`

### Exploring Data
- **Overview**: View data statistics and basic information
- **KPI Metrics**: Monitor key performance indicators
- **Visualizations**: Create interactive charts and graphs
- **Analysis**: Perform correlation analysis, grouping, and top-N queries

### Exporting Results
- Download processed data as CSV
- Export visualizations as images
- Save analysis results for reporting

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## 🐛 Troubleshooting

### Common Issues

**Port 8501 already in use:**
```bash
# Change port in docker-compose.yml:
ports:
  - "8502:8501"
```

**Docker build fails:**
```bash
# Clean Docker cache and rebuild:
docker system prune -a
docker-compose build --no-cache
```

**Application doesn't load:**
- Wait 30-60 seconds after starting
- Check Docker Desktop is running
- Verify port is not blocked by firewall

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

- **GitHub**: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- **Email**: your.email@example.com
- **Issues**: [Report a bug](https://github.com/YOUR_USERNAME/example2-main/issues)

---

## 🌟 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data visualization powered by [Plotly](https://plotly.com/)
- Containerized with [Docker](https://www.docker.com/)

---

<div align="center">

**Made with ❤️ and ☕**

[![🇷🇺 Читать на русском](https://img.shields.io/badge/Читать_на-Русском-red?style=for-the-badge)](README.ru.md)

[⬆ Back to top](#-sales-analytics-platform)

</div>
