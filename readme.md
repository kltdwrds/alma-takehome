# Lead Management Application

This is a FastAPI application for managing leads, allowing prospects to submit leads publicly and attorneys to view/update them internally. It uses SQLite for storage and includes simulated email notifications.

Available for prompt review at: https://replit.com/@edwardsky1/alma-takehome

## Prerequisites

- Python 3.6 or later
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

1. **Clone or Navigate to the Project Directory**

   ```bash
   cd /path/to/alma-takehome
   ```

2. **Create and Activate a Virtual Environment**

   Create a virtual environment to isolate dependencies:

   ```bash
   python -m venv .venv
   ```

   Activate it:

   - **Unix-like (Linux/macOS)**:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install fastapi uvicorn sqlalchemy "pydantic[email]" python-multipart
   ```

## Running the Application

The SQLite database (`leads.db`) will be created automatically on first run.

1. **Start the FastAPI Server**

   Run the application with Uvicorn:

   ```bash
   python -m uvicorn main:app --reload
   ```

2. **Access the API**

   The API is now running at `http://127.0.0.1:8000`. You can interact with it using tools like `curl`, Postman, or a browser.

   - **Public Endpoint**:
     - `POST /leads`: Submit a new lead with form data (`first_name`, `last_name`, `email`, `resume`).
   - **Internal Endpoints** (require authentication):
     - `GET /leads`: List all leads.
     - `PATCH /leads/{id}`: Update a lead’s state.

## Testing the API

1. **Submit a Lead**

   Use `curl` to test the `POST /leads` endpoint:

   ```bash
   curl -X POST "http://127.0.0.1:8000/leads" \
     -F "first_name=John" \
     -F "last_name=Doe" \
     -F "email=john.doe@example.com" \
     -F "resume=@/path/to/resume.pdf"
   ```

   - Replace `/path/to/resume.pdf` with the path to a real PDF file.
   - Response: JSON with lead details.
   - Console: Simulated email outputs for the prospect and attorney.

2. **List Leads**

   Use `curl` to test the `GET /leads` endpoint (requires authentication):

   ```bash
   curl -u admin:password http://127.0.0.1:8000/leads
   ```

   - Credentials: Username `admin`, password `password`.
   - Response: JSON list of all leads.

3. **Update a Lead**

   Update a lead’s state to `REACHED_OUT`:

   ```bash
   curl -u admin:password -X PATCH "http://127.0.0.1:8000/leads/1" \
     -H "Content-Type: application/json" \
     -d '{"state": "REACHED_OUT"}'
   ```

   - Replace `1` with a valid lead ID.
   - Response: Updated lead details or 404 if not found.
