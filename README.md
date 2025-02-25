# Data Insights

**Data Insights** is a tool that leverages artificial intelligence to enhance data analysis and processing capabilities. Through natural language interaction, it empowers users to unlock valuable insights from their data effortlessly, without requiring deep programming expertise. Whether you're a beginner in data analysis or a seasoned professional, this tool offers an efficient and intuitive experience.

## Key Features

1. **Talk to Excel**  
   Simply ask questions in natural language, such as "Show me the top five products by sales," and instantly extract insights from Excel files.

2. **Interact with Databases**  
   Connect to databases and retrieve results with straightforward commands, eliminating the need for complex SQL queries.
## Technologies Involved

Data Insights is built upon powerful open-source technologies:

- **[Pandas AI](https://getpanda.ai/)**: An extension of the Pandas library, enabling natural language queries for data analysis.
- **[Ollama](https://ollama.com/)**: A framework for running large language models locally, powering the AI-driven interactions.
- **[DeepSeek Code](https://github.com/deepseek-ai/DeepSeek-Coder-V2)**: A coding assistant that enhances development efficiency and supports the project’s backend logic.
- **[Streamlit](https://streamlit.io/)**: A Python framework for creating interactive web applications, making it easy to build and share data-driven interfaces.

### 📦 Installation

To get started with Data Insights, you'll need to set up a Python environment. We recommend using MiniConda for management. Follow these steps:

### 1. Install MiniConda
   Download and install [MiniConda](https://docs.conda.io/en/latest/miniconda.html), a lightweight Python environment manager.

### 2. Create a Python Environment
   Run the following command in your terminal to create a dedicated Python 3.11 environment:
   ```bash
   conda create -n data_insights python=3.11
   ```

### 3. Install Dependencies
   The project dependencies are listed in the `requirements.txt` file. To install them, ensure your environment is activated, then run the following command in your terminal:
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
   ```

### 4. Install Ollama Locally

Follow these steps to set up Ollama on your local machine and get started with the DeepSeek Coder model:

1. **Download Ollama**:  
   Visit the [official Ollama website](https://ollama.com/) and download the installer for your operating system (Windows, macOS, or Linux).

2. **Launch Ollama**:  
   After installation, open your terminal or command prompt and start the Ollama service by running:
3. **Pull the DeepSeek Model**:  
   Download the DeepSeek Coder model by executing the following command in your terminal:
   ```bash
   ollama pull deepseek-coder-v2 or ollama run deepseek-coder-v2
   ```

### 💻 Usage

#### Talk to Excel
   ```bash
     streamlit run data_insights_excel.py
   ```
