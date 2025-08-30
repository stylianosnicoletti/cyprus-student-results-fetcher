# Cyprus Student Results Fetcher

This Python script allows students to easily search and view their exam results from the Cyprus Ministry of Education DevExpress ASP.NET GridView system. Results are displayed in the terminal and saved in a JSON file for each query.

## Features
- Search results by student ID and year (2018 to current year)
- Saves parsed results in a readable JSON file
- Validates input for allowed year and student ID range

## Prerequisites
- Python 3.7 or newer

### Required Python Packages
- `requests`
- `beautifulsoup4`

Install them using pip:

```sh
pip install requests beautifulsoup4
```

## Usage
1. Place your request template file (e.g., `pagkypries_year_YYYY_student_with_id_XXXX_request.html`) in the same folder as the script.
2. Run the script:

```sh
python student_result_full_flow.py
```

3. Enter your student ID (between 1 and 9999) and the year (from 2018 to next year) when prompted.
4. The script will fetch, parse, and display your results. It will also save them in a file named:

```
pagkypries_year_{year}_student_with_id_{padded_id}_results.json
```

## Troubleshooting
- If you get a "Request file not found" error, make sure your request template file exists and is named correctly.
- If you get no results, verify your student ID and year are correct and that the server is online.

## License
MIT
