# Auction API

A simple REST API for a live auction system built with FastAPI and SQLite.

## If there is no live link setup steps are as follows:

1. Clone the repo
   git clone https://github.com/ratpoop/auction-api.git
   cd auction-api

2. Create a virtual environment and activate it
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux

3. Install dependencies
   pip install fastapi uvicorn sqlalchemy

4. Run the server
   uvicorn main:app --reload

5. Open index.html in your browser to use the UI
   Or visit http://localhost:8000/docs for the API explorer
