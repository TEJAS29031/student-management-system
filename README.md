# 🎓 Student Management System

A comprehensive student management system built with Streamlit, SQLite, Docker, and CI/CD pipeline.

## Features

- ➕ Add new students
- 👥 View all students
- 🔍 Search students
- ✏️ Update student information
- 🗑️ Delete students
- 📊 Dashboard with statistics
- 📥 Export data to CSV

## Technologies Used

- **Frontend**: Streamlit
- **Database**: SQLite
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Testing**: Pytest, Selenium

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

### Docker Setup

1. Build the Docker image:
```bash
docker build -t student-management-system .
```

2. Run the container:
```bash
docker run -p 8501:8501 student-management-system
```

3. Access the application at `http://localhost:8501`

## Testing

### Run Unit Tests
```bash
pytest tests/test_database.py -v
```

### Run Selenium Tests
```bash
# First, start the application
streamlit run app.py

# In another terminal
pytest tests/test_selenium.py -v
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs unit tests on every push
- Performs code linting
- Builds and tests Docker image
- Runs on push to main branch and pull requests

## Project Structure
```
student-management-system/
├── app.py                 # Main application
├── database.py            # Database operations
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # CI/CD pipeline
├── tests/
│   ├── test_database.py  # Unit tests
│   └── test_selenium.py  # Selenium tests
└── README.md             # Documentation
```

## License

MIT License
## 🔐 Login Credentials

**Default Admin Access:**
- Username: `admin`
- Password: `admin123`

> **Note:** In production, implement proper authentication with hashed passwords stored in a database.


## 🐳 Docker Deployment


### Quick Start with Docker

1. **Build the image:**
```bash
   docker build -t student-management-system .
```

2. **Run the container:**
```bash
   docker run -d -p 8501:8501 --name student-app student-management-system
```

3. **Access the application:**
   Open your browser and go to `http://localhost:8501`

4. **Login credentials:**
   - Username: `admin`
   - Password: `admin123`

### Using Docker Compose
```bash
# Start the application
docker-compose up -d

# Stop the application
docker-compose down
```

### Docker Commands
```bash
# View logs
docker logs -f student-app

# Stop container
docker stop student-app

# Remove container
docker rm student-app

# List running containers
docker ps
```