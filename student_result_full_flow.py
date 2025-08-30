import requests
import os
import re
from bs4 import BeautifulSoup

def parse_raw_http_request(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split headers and body
    if '\n\n' in content:
        headers_part, body = content.split('\n\n', 1)
    else:
        headers_part, body = content.split('\r\n\r\n', 1)
    lines = headers_part.splitlines()
    # First line: POST /path HTTP/2
    request_line = lines[0]
    method, path, _ = request_line.split()
    url = 'https://eservices.moec.gov.cy' + path
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            headers[key] = value
    return url, headers, body

def extract_html_from_response(response_text):
    match = re.search(r"'html':'(.*?)'\}\}\)$", response_text, re.DOTALL)
    if not match:
        raise ValueError("Could not extract HTML from response.")
    html = match.group(1)
    html = html.replace('\\r\\n', '')
    html = html.replace('\\t', '')
    html = html.replace('\\', '')
    return html

def parse_gridview(html):
    import json
    soup = BeautifulSoup(html, 'html.parser')
    data_row = soup.find('tr', class_='dxgvDataRow_DevEx')
    if not data_row:
        print("No valid data row found.")
        return None
    cells = data_row.find_all('td')
    student_id = cells[0].get_text(strip=True)
    department = cells[1].get_text(strip=True)
    access_grade = cells[2].get_text(strip=True)
    grades = []
    for cell in cells[3:]:
        val = cell.get_text(strip=True)
        if val:
            grades.append(val)
    result = {
        "student_id": student_id, # Κωδικός Υποψηφίου
        "department": department, # Τμήμα Πρόσβασης
        "access_grade": access_grade, # Βαθμός Πρόσβασης
        "grades": grades # Βαθμολογίες ανά Πλαίσιο Πρόσβασης
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

def main():
    while True:
        student_id = input("Enter student id (1-9999): ")
        if student_id.isdigit() and 1 <= int(student_id) <= 9999:
            break
        print("Invalid student id. Please enter a number from 1 to 9999.")

    import datetime
    current_year = datetime.datetime.now().year
    max_year = current_year
    while True:
        year = input(f"Enter year (2018 to {max_year}): ")
        if year.isdigit() and 2018 <= int(year) <= max_year:
            break
        print(f"Invalid year. Please enter a year from 2018 to {max_year}.")

    # Pad student_id with zeros to 4 digits if needed
    padded_id = str(student_id).zfill(4)
    request_file = f'pagkypries_year_YYYY_student_with_id_XXXX_request.html'
    if not os.path.exists(request_file):
        print(f"Request file {request_file} not found.")
        return
    url, headers, body = parse_raw_http_request(request_file)
    # Replace all occurrences of XXXX with the padded student_id
    body = body.replace('XXXX', padded_id)
    # Replace YYYY in body, url, and headers
    body = body.replace('YYYY', year)
    url = url.replace('YYYY', year)
    headers = {k: v.replace('YYYY', year) if isinstance(v, str) else v for k, v in headers.items()}
    response = requests.post(url, headers=headers, data=body)

    # Parse and display the response
    html = extract_html_from_response(response.text)
    result = parse_gridview(html)
    if result:
        json_filename = f'pagkypries_year_{year}_student_with_id_{padded_id}_results.json'
        import json
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f'Results saved to {json_filename}')

if __name__ == '__main__':
    main()
