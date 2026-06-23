# Setup Project Commands

## 1. Buat dan masuk ke folder proyek
`mkdir fraud-detection-db`
`cd fraud-detection-db`
## 2. Buat Virtual Environment
`python -m venv venv`
## 3. Aktifkan Virtual Environment (Untuk Windows)
`venv\Scripts\activate`
## 4. Install SQLAlchemy (ORM) dan PyMySQL (Driver koneksi MySQL)
`pip install sqlalchemy pymysql`
## 5. Install .env in python
`pip install python-dotenv`
## 6. Install Liblary faker for datafake
`pip install faker`

# Database Python Configurations
Database Local URL: `mysql+pymysql://<DATABSE_USERNAME>:<DATABSE_PASSWORD>@localhost:3306/<DATABSE_NAME>`

**please add this in .gitigore pyhon manual project**
.env
venv/
__pycache__/