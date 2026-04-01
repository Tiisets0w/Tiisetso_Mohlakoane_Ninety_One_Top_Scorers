import sqlite3
import re

def parse_csv(csv_string):
    lines = csv_string.strip().split("\n")
    data = []
    pattern = re.compile(r'^"?(.+?)"?\s*,\s*(\d+)$') #Using regex to correctly parse names with commas or quotes in the CSV
    for line in lines[1:]:
        line = line.strip()
        match = pattern.match(line)
        if not match:
            print(f"Skipping malformed line: {line}")
            continue
        name, score_str = match.groups()
        data.append({"Name": name.strip(), "Score": int(score_str)})
    return data

def get_top_scorers(data):
    if not data:
        return [], 0
    max_score = max(item['Score'] for item in data)
    top_scorers = [item['Name'] for item in data if item['Score'] == max_score]
    top_scorers.sort()
    return top_scorers, max_score

def save_to_db(data, db_name="scores.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS scores (Name TEXT, Score INTEGER)")
    c.execute("DELETE FROM scores")
    for item in data:
        c.execute("INSERT INTO scores (Name, Score) VALUES (?, ?)", (item['Name'], item['Score']))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    try:
        with open("TestData.csv", "r", encoding="utf-8") as f:
            csv_string = f.read()
    except FileNotFoundError:
        print("Error: 'TestData.csv' not found.")
        exit(1)

    data = parse_csv(csv_string)
    if not data:
        print("No valid data found in CSV.")
        exit(1)

    top_scorers, score = get_top_scorers(data)
    print("Top Scorers:")
    for name in top_scorers:
        print(name)
    print(f"Score: {score}")

    save_to_db(data)
    print("Data saved to 'scores.db'")