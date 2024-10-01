# Data Visualization Assistant

This project is a Flask-based web application that allows users to upload CSV files, run plain English queries, and get data visualization results. The application supports creating plots based on the user's queries by leveraging the `pandas` library for data manipulation and `matplotlib` for visualizations. It also utilizes the Ollama API and llama-3.2-1B SLM to generate Python visualization code dynamically based on the data.

## Features

- **Upload CSV Files:** Users can upload CSV files directly from the web interface.
- **Run Queries:** Execute custom queries on the uploaded CSV data.
- **Visualize Results:** Automatically generate visualizations based on user-defined queries in Natural Language.
  
## Prerequisites

- **Ollama**: You must have Ollama installed (with a SLM like llama3.2:3B) and running locally, as the app communicates with it to generate the visualization code.
  - [Ollama Installation Guide](https://ollama.ai)
- **Python 3.8+**: The application is built using Python.
- **Flask**: A micro web framework used to create the application.
- **pandas**: For data manipulation.
- **matplotlib**: For generating plots.
