# AI Data Analyst Assistant

An intelligent data analysis tool powered by AI that helps you analyze, visualize, and generate insights from your datasets.

## Features

- 📊 **Data Analysis**: Comprehensive statistical analysis of your datasets
- 🤖 **AI-Powered Insights**: Generate intelligent insights using LLM integration
- 📈 **Data Visualization**: Create beautiful charts and visualizations
- 🔄 **Multi-Format Support**: Load data from CSV, Excel, JSON, and Parquet files
- 🚀 **REST API**: FastAPI-based REST API for easy integration
- 📋 **Data Quality Reports**: Automatic data quality assessment

## Project Structure

```
AI-Data-Analyst-Assistant/
│
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
│
├── data/                 # Data files directory
│
├── utils/                # Utility modules
│   ├── data_loader.py    # Data loading functionality
│   ├── analyzer.py       # Data analysis engine
│   └── llm_helper.py     # LLM integration
│
├── charts/               # Generated visualizations
│
└── tests/                # Unit tests
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Dhanush65196/AI-DATA_Analyst-Assistant.git
   cd AI-Data-Analyst-Assistant
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage

### Running the API Server

```bash
python app.py
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at `http://localhost:8000/docs`

### Example: Analyze a Dataset

```python
from utils.data_loader import DataLoader
from utils.analyzer import DataAnalyzer
from utils.llm_helper import LLMHelper

# Load data
loader = DataLoader()
df = loader.load_data('data/sample.csv')

# Analyze
analyzer = DataAnalyzer()
results = analyzer.analyze(df)

# Get insights
llm = LLMHelper()
insights = llm.get_insights(results)
print(insights)
```

### Using the REST API

**Analyze a file**:

```bash
curl -X POST "http://localhost:8000/analyze?file_path=data/sample.csv"
```

**Health check**:

```bash
curl "http://localhost:8000/health"
```

## API Endpoints

| Method | Endpoint   | Description       |
| ------ | ---------- | ----------------- |
| GET    | `/`        | Root endpoint     |
| GET    | `/health`  | Health check      |
| POST   | `/analyze` | Analyze a dataset |

## Configuration

Create a `.env` file in the project root:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning
- **matplotlib & seaborn**: Data visualization
- **fastapi**: Web API framework
- **openai**: AI/LLM integration
- **python-dotenv**: Environment variable management

See `requirements.txt` for full list.

## Development

### Running Tests

```bash
pytest tests/
```

### Installing Development Dependencies

```bash
pip install pytest pytest-cov black flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For support, email dhanush@example.com or open an issue in the repository.

## Roadmap

- [ ] Advanced data visualization dashboard
- [ ] Real-time data streaming support
- [ ] Multi-language LLM support
- [ ] Data export with formatted reports
- [ ] User authentication system
- [ ] Database integration

## Authors

- Dhanush (@Dhanush65196)

## Acknowledgments

- OpenAI for API access
- FastAPI for the excellent web framework
- The pandas and scikit-learn communities
