import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_table_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', id='searchtable')
        return table
    except requests.RequestException as e:
        print(f"An error occurred while fetching the data: {e}")
        return None

def safe_extract(cell, attr=None, sub_attr=None, default=""):
    try:
        if attr:
            value = getattr(cell, attr)
            if value == None: return {}  
            elif sub_attr and hasattr(value, sub_attr):
                return value.get(sub_attr, default)
            elif isinstance(value, dict) and sub_attr:
                return value.get(sub_attr, default)
            elif value == None: return {}  
            return value
        return cell.text.strip()
    except AttributeError:
        return default

def parse_table_to_json(table):
    base_grin_url = 'https://npgsweb.ars-grin.gov/'
    base_global_grin_url = 'https://npgsweb.ars-grin.gov/gringlobal/'
    if not table:
        return {"error": "Table not found"}
    
    rows = table.find('tbody').find_all('tr')
    data_array = []
    
    for row in rows:    
        cells = row.find_all('td')
        
        if len(cells) < 17:  # Ensure we have enough cells
            continue  # Skip this row if it doesn't have enough cells
        
        data = {
            "accession_id": safe_extract(cells[1]),
            "accession_url": base_global_grin_url + safe_extract(cells[1], 'a', 'href') if safe_extract(cells[1], 'a', 'href') != {} else None,
            "plant_name": safe_extract(cells[2]),
            "taxonomy_name": safe_extract(cells[3]),
            "taxonomy_url" : base_global_grin_url + safe_extract(cells[3], 'a', 'href') if safe_extract(cells[3], 'a', 'href') != {} else None,
            "origin": safe_extract(cells[4]),
            "genebank_name": safe_extract(cells[5]),
            "genebank_url": base_global_grin_url + safe_extract(cells[5], 'a', 'href') if safe_extract(cells[5], 'a', 'href') != {} else None,
            "image_url": base_grin_url + safe_extract(cells[6],'img','src') if safe_extract(cells[6],'img','src') != {} else None,
            "image_alt": safe_extract(cells[6],'img','alt'),
            "image_display_url": base_global_grin_url + safe_extract(cells[6], 'a', 'href') if safe_extract(cells[6], 'a', 'href') != {} else None,
            "received": safe_extract(cells[8]),
            "source_type": safe_extract(cells[9]),
            "source_date": safe_extract(cells[10]),
            "collection_site": safe_extract(cells[11]),
            "coordinates": safe_extract(cells[12]),
            "elevation": safe_extract(cells[13]),
            "habitat": safe_extract(cells[14]),
            "improvement_status": safe_extract(cells[15]),
            "narrative": safe_extract(cells[16])
        }
        data_array.append(data)
    
    return data_array

@app.route('/')
def get_accession_data():
    accession_id = request.args.get('id', '507522')  # Default to 507522 if no ID is provided
    url = f"https://npgsweb.ars-grin.gov/gringlobal/search?q={accession_id}"
    table = get_table_data(url)
    if table:
        data = parse_table_to_json(table)
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve the table data."}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)