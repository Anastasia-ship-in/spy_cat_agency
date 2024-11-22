# Clone the repository
git clone git@github.com:Anastasia-ship-in/spy_cat_agency.git
# Navigate to the project directory
cd your-repo-name

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Configure the Database
Open the app/database.py file.
Modify the database connection string to match your local or remote database.
"DATABASE_URL = "postgresql://username:password@localhost/dbname"

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload

# Use Postman for API Requests
File: Cats.postman_collection.json (located in the project root).
Instructions: Open Postman → Click "Import" → Select the file → Import.