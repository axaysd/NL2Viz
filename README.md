
# **Data Visualization Assistant**

Transform natural language queries into data visualizations with ease. This Flask-based web application uses a fine-tuned **Llama3.2-1B** model to dynamically generate Python visualization code from plain English queries. It integrates seamlessly with `pandas` for data manipulation and `matplotlib` for creating stunning plots.

## **Features**

- **Upload CSV Files**: Upload CSV files directly from the web interface for analysis.
- **Natural Language Queries**: Run plain English queries such as:
  - _"Create a line chart of temperature over time."_  
  - _"Show a bar chart of sales by region."_
- **Dynamic Visualizations**: Generate bar charts, scatter plots, line graphs, and more based on your queries.
- **Model Integration**: Leverages a fine-tuned **Llama3.2-1B** model (fine-tuned using **Unsloth**) to convert English queries into accurate Python `matplotlib` code.

## **Technical Highlights**

- **Fine-Tuned Model**: Powered by a fine-tuned **Llama3.2-1B** model, trained on a dataset of 500 query-to-code pairs to ensure precise code generation.
- **Flask Framework**: Provides a clean and responsive web interface for file uploads and query execution.
- **Data Processing**: Uses `pandas` for efficient manipulation and filtering of datasets.
- **Visualization**: Produces professional-grade visualizations with `matplotlib`.

## **Prerequisites**

Before running the application, ensure you have the following installed:

- **[Ollama](https://ollama.ai)**: Required to run the Llama3.2-1B model locally for query-to-code transformation.
- **Python 3.8+**: Ensure Python 3.8 or later is installed.
- **Flask**: A lightweight framework for the web application.
- **pandas**: For flexible and efficient data manipulation.
- **matplotlib**: To generate visualizations.

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure **Ollama** is running locally with the fine-tuned **Llama3.2-1B** model.

4. Start the Flask application:
   ```bash
   python app.py
   ```

5. Access the application in your browser at:
   ```
   http://127.0.0.1:5000
   ```

## **Usage**

1. Upload your CSV file via the web interface.
2. Enter your query in plain English, such as:
   - _"Show me a pie chart of market share by product."_
3. View the generated visualization directly in the app.

---

### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
