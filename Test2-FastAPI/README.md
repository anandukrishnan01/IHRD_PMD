# FastAPI Dashboard 

### Challenge Overview:

The objective of this coding challenge is to create an interactive and informative dashboard from a dataset (dataset_netflix.csv). The dashboard should present insightful visualizations and analytics derived from the dataset, providing a clear and comprehensive understanding of its contents. A example dashboard is provided in the code

### How to run application

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 5001

or

docker-compose up   
```

Open http://127.0.0.1:5001/ in browser

## Task

To create the most informative and user-friendly dashboards that effectively communicate the data insights. Creativity, clarity, and efficiency are key.

## Instructions for Candidates

Familiarize yourself with dataset_netflix.csv to understand the data you'll be visualizing.

1. Setup Development Environment:
    Ensure you have Python 3 and FastAPI installed.
    Optionally, set up SQLite if you plan to use a database.

2. Application Development:
    - Develop the dashboard using FastAPI.
    - Make sure the application runs on 0.0.0.0 at port 5001.
    - Ensure all dashboard features are accessible via http://0.0.0.0:5001/.

3. Create the Dashboard:
    Use suitable libraries for data processing and visualization (e.g., Pandas, Matplotlib, Plotly etc).
    Focus on creating informative and user-friendly interfaces.

4. Optional Database Integration:
    If needed, use SQLite3 to manage and query the dataset.
    Document any database schema or migrations.

5. Testing:
    Test your application thoroughly to ensure all features work as expected.

6. Documentation:
    - Create a README file including:
    - An overview of the dashboard.
    - Details of building components and any external libraries used.
    - Highlight unique features or functionalities of your dashboard.
    - Provide detailed instructions on how to run the application.

7. How to Submit answer:
    - Submit your complete project code along with the README file to a public Github repository
    - Ensure your code is well-commented, follow proper structure and follows good coding practices.
    - Share public Github repository in provided Google forms


8. Running the Application:
    - Your application should be startable with the command: ```uvicorn app:app --reload --host 0.0.0.0 --port 5001```
