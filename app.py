from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import io
import json
import requests
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for matplotlib
import matplotlib.pyplot as plt
import base64
import os

# Define a directory to save uploaded CSV files
UPLOAD_FOLDER = 'uploads'  # Ensure this directory exists

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    
    df = pd.read_csv(file)
    
    # Get the top 5 records
    top_records = df.head(5).to_dict(orient='records')  # Convert to a list of dictionaries
    
    # Get column names for the table header
    columns = df.columns.tolist()
    
    return jsonify({'top_records': top_records, 'columns': columns})

@app.route('/query', methods=['POST'])
def query():
    file = request.files['file']
    query = request.form.get('query', '')
    
    df = pd.read_csv(file)
    
    try:
        result = df.query(query)
        output = io.StringIO()
        result.to_csv(output, index=False)
        mem = io.BytesIO()
        mem.write(output.getvalue().encode())
        mem.seek(0)
        
        return send_file(
            mem,
            as_attachment=True,
            download_name='query_result.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/visualize', methods=['POST'])
def visualize():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Create the directory if it doesn't exist

    file = request.files['file']
    query = request.form.get('query', '')
    
    # Save the uploaded CSV file to the specified directory
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)  # Save the file

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Get column names and datatypes
    columns_info = df.dtypes.to_dict()
    columns_info = {k: str(v) for k, v in columns_info.items()}
    
    # Prepare the prompt for Ollama
    prompt = f"""
    Given the following CSV file structure and query:
    
    Columns and datatypes:
    {json.dumps(columns_info, indent=2)}
    
    Query:
    {query}
    
    Generate Python code using pandas and matplotlib to visualize the data based on the query.
    Do not redefine the dataset in the code. Use 'df' as the variable name for the existing pandas DataFrame.
    DO NOT REDEFINE THE VARIABLE df IN YOUR CODE. ASSUME THAT THE VARIABLE df HAS BEEN INITIALIZED.
    The code should produce a single plot that best represents the queried data.
    Only provide the code in your response and do NOT add any additional content other than the code in your response.
    I should be able to execute your response as is as the code.
    Your response should start and end with python code and nothing else. It should not start with the word python in it.
    Append your generated code after the definition of 'df'.
    """
    
    # Send request to Ollama
    try:
        ollama_response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'llama3.2:3b',
            'prompt': prompt
        }, stream=True)  # Enable streaming
        
        # Initialize generated_code with the correct definition of df
        generated_code = f"import pandas as pd\nimport matplotlib.pyplot as plt\n\n"  # Start with imports
        generated_code += f"df = pd.read_csv('{file_path}')\n"  # Define df using the saved file path
        print("hahah", generated_code)
        
        for line in ollama_response.iter_lines():
            if line:
                try:
                    response_json = json.loads(line)
                    if 'response' in response_json:
                        generated_code += response_json['response']
                    if response_json.get('done', False):
                        break
                except json.JSONDecodeError:
                    print("Error decoding JSON:", line)
        
        if not generated_code:
            return jsonify({'error': 'No code generated from Ollama API'}), 500
        
        # Print the generated code for debugging
        print("Generated Code:\n", generated_code)  # Debug print
        
        # Execute the generated code
        try:
            exec(generated_code)
            
            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # Encode the image to base64
            img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            return jsonify({'image': img_base64})
        except Exception as e:
            return jsonify({'error': f'Error executing generated code: {str(e)}'}), 400
    except requests.RequestException as e:
        return jsonify({'error': f'Error communicating with Ollama API: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()