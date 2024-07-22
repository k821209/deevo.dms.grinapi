# GRIN Accession Data API

This Flask application provides an API to fetch and parse accession data from the GRIN (Germplasm Resources Information Network) database.

## Features

- Fetches accession data based on an input ID
- Parses HTML tables from the GRIN website
- Returns data in JSON format
- Includes a health check endpoint

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/k821209/deevo.dms.grinapi.git
   cd deevo.dms.grinapi 
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. The server will start on `http://localhost:8080`

3. Use the API:
   - To fetch accession data: `http://localhost:8080/?id=[accession_id]`
   - For a health check: `http://localhost:8080/health`
   - DEMO : `https://grinapi-dot-deevo-dms.an.r.appspot.com/?id=507422`

## API Endpoints

- `GET /`: Fetches accession data. 
  - Query parameter: `id` (optional, defaults to '507522')
  - Returns: JSON array of accession data

- `GET /health`: Health check endpoint
  - Returns: `{"status": "healthy"}` if the service is running

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- GRIN (Germplasm Resources Information Network) for providing the source data
- BeautifulSoup4 for HTML parsing capabilities
- Flask for the web framework
