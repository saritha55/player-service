
# 🏏 Player Management Service

A backend service that manages player data, supports role-based data filtering, stores player statistics, and includes a bonus nickname generator using AI (Python + TinyLlama).

---

## 🔧 Tech Stack

- Java 17
- Spring Boot
- RESTful APIs
- H2 In-Memory DB (easily switchable to MySQL/PostgreSQL)
- Python 3 (Flask for nickname generator)
- JUnit for testing

---

## 🚀 Run Locally

### 📦 Prerequisites

- Java 17+
- Maven
- Python 3.10+ with `Flask`, `transformers`, `torch` (for nickname service)

### 🛠️ Setup & Start Java App

```bash
# Clone the repository
git clone https://github.com/saritha55/player-service.git
cd player-service

# Start the Spring Boot app
mvn spring-boot:run
```

### 🧠 Setup & Run Python Nickname Generator (Optional)

```bash
cd nickname-generator
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start Flask app
python app.py
```

---

## 🌐 API Endpoints

### ✅ Java (Spring Boot)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/players?isAdmin=true` | Get all players (admin view) |
| `GET` | `/v1/players/{id}?isAdmin=false` | Get one player (limited view) |
| `POST` | `/v1/players` | Add a new player |
| `DELETE` | `/v1/players/{id}` | Delete player by ID |

#### Sample JSON for POST `/v1/players`

```json
{
  "id": 1,
  "firstName": "Virat",
  "lastName": "Kohli",
  "age": 35
}
```

---

### 🧠 Python Nickname Generator (Bonus)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `http://localhost:5000/generate-nickname` | AI-based nickname suggestion |

#### Sample Body

```json
{
  "country": "India"
}
```

---

## ✅ Test the App

### 🔍 Unit + Integration Tests (Java)

```bash
# From root of project
mvn test
```

---

## 🗂️ Project Structure

```
player-service/
├── src/
│   ├── main/
│   │   ├── java/com/example/player/
│   │   │   ├── PlayerController.java
│   │   │   ├── PlayerService.java
│   │   │   ├── Player.java
│   │   │   └── PlayerServiceApplication.java
├── nickname-generator/
│   ├── app.py
│   └── venv/  <-- (ignored from Git)
├── README.md
└── .gitignore
```

---

## 🚫 GitHub Large File Fixes

To avoid issues with GitHub file limits:

- `venv/` is added to `.gitignore`
- Avoid pushing `.dylib`, `.pkl`, or `.pt` files to GitHub
- Cleaned up `.git` before push using:

```bash
rm -rf .git
git init
git remote add origin https://github.com/saritha55/player-service.git
git add .
git commit -m "Clean init"
git push -f origin master
```

---

## 🎤 How to Present in Interview

🔹 **Start With Overview**:
> "This project is a Spring Boot backend for managing players, with role-based access and a bonus AI nickname generator built with Python + TinyLlama."

🔹 **Tech Stack Justification**:
> "I used H2 for fast local testing. The code supports switch to MySQL/PostgreSQL by changing configs."

🔹 **Role-Based Logic**:
> "I used `isAdmin` as a query param to dynamically filter fields returned per role."

🔹 **Show Tests**:
> "Service and controller layers are covered using JUnit."

🔹 **Demo with Postman**:
- `GET /v1/players?isAdmin=true`
- `POST /generate-nickname` with `{"country": "India"}`

---