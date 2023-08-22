# Clockify Task Name Fetcher

This is a Python script for retrieving task names from Clockify using the Clockify API.

## Prerequisites

Before you can run this script, ensure you have the following prerequisites:

- **Python**: You should have Python 3.7 or later installed on your computer. If you don't have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/).

## Installation

To run the Clockify Task Name Fetcher, follow these steps:

1. Open the `.env.sample` file provided in the project directory and add your Clockify API key, project ID, and workspace ID. Save it as `.env`.

Replace `your_api_key_here`, `your_project_id_here`, and `your_workspace_id_here` with your actual Clockify API key, project ID, and workspace ID.

2. Open your terminal or command prompt.

3. Navigate to the project's root directory.

4. Activate the virtual environment (if you created one):

- On Windows:

  ```
  .\venv\Scripts\activate
  ```

- On macOS and Linux:

  ```
  source venv/bin/activate
  ```

5. Install the required Python packages using the following command:

``pip install -r requirements.txt
``
6. Run the script using the following command:

 ``
python main.py
``

7. The script will make an API request to Clockify and retrieve the task names associated with the specified project and workspace. The task names will be displayed in the terminal.

