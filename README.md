# Top Scorers Application

This project reads a CSV file containing people’s names and test scores, determines the top scorers, prints them to STDOUT, saves all data into a SQLite database, and exposes a RESTful API to interact with the scores.

---

## Project Features

- Reads a CSV (`TestData.csv`) with names and scores.  
- Parses CSV manually using regex, handling names with commas and optional quotes.  
- Determines top scorer(s) and prints them to STDOUT.  
- Saves all data into a SQLite database (`scores.db`).  
- Provides a RESTful API with endpoints:
  - `POST /scores` → Add a new score  
  - `GET /scores?name=NAME` → Retrieve a specific person's score  
  - `GET /top` → Retrieve the top scorer(s)  

---

## Design Choices & Assumptions

- Manual CSV Parsing:  
  - Regex handles names with commas and optional quotes.  
  - Malformed lines are skipped with a warning to maintain data integrity.  

- Top Scorers Logic:  
  - Maximum score is determined from all valid entries.  
  - Multiple top scorers are handled and sorted alphabetically.  
  - Output goes directly to STDOUT.  

- Database Choice:  
  - SQLite is used for simplicity and portability.  
  - Database is automatically created and cleared before saving new CSV data.  

- REST API Implementation:  
  - Built using Python’s built-in `http.server` and `sqlite3`.  
  - Minimalistic and human-readable, easy to maintain.  
  - Optional root endpoint `/` returns a simple “API is running” message.  

- Assumptions:  
  - CSV is UTF-8 encoded with a header row.  
  - Scores are integers; invalid scores are skipped.  
  - API assumes a local, trusted environment (no authentication).  

---

## Getting Started

### 1.Download the Project

Ensure the folder contains:  
- `top_scorers.py`  
- `api.py`  
- `TestData.csv`  

---

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate      # since I used Windows this is the command for it

## Run Top Scorers Script
##Step 1
`python top_scorers.py` #use this command in the CLI of your choice , I used CMD
 #YOU SHOULD SEE :
Top Scorers:
George, Of The Jungle
Sipho Lolo
Score: 78
Data saved to 'scores.db'

##Step 2: Run the REST API server
`python api_server.py` #still in CMD, the server runs on local host http://localhost:8000

##Step 3: Example post : I used curl
curl -X POST http://localhost:8000/scores -H "Content-Type: application/json" -d "{\"Name\":\"Bob Marley\",\"Score\":85}"
##To get that specific person's score
curl "http://localhost:8000/scores?name=Bob%20Marley"

