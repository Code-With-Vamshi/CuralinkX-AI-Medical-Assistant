# 🧠 CuralinkX AI Medical Assistant

An AI-powered medical research assistant that provides **real-time insights, research papers, and clinical trials** based on user queries.

---

## 🚀 Features

* 🔍 Intelligent medical query analysis
* 📚 Fetches latest research papers (PubMed + OpenAlex)
* 🧪 Clinical trials data integration
* 🤖 AI-generated insights using LLM (Ollama)
* 📊 Real-time stats (papers, trials, response time)
* 🧠 What-if scenario analysis

---

## 🛠 Tech Stack

### Frontend

* React.js
* CSS (Modern UI with animations)

### Backend

* Python (Flask)
* Flask-CORS
* Requests

### AI Integration

* Ollama (Mistral model)

---

## 📂 Project Structure

```
CuralinkX-AI-Medical-Assistant/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│
├── README.md
├── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/Code-With-Vamshi/CuralinkX-AI-Medical-Assistant.git
cd CuralinkX-AI-Medical-Assistant
```

---

### 2️⃣ Backend Setup

```
cd backend
pip install -r requirements.txt
python app.py
```

👉 Runs on: `http://127.0.0.1:8000`

---

### 3️⃣ Frontend Setup

```
cd frontend
npm install
npm start
```

👉 Runs on: `http://localhost:3000`

---

## 🔗 API Endpoint

```
POST /analyze
```

### Request Body

```
{
  "disease": "Diabetes",
  "intent": "latest treatment",
  "location": "India",
  "what_if": "patient is obese"
}
```

---

## 🧠 How It Works

1. User enters disease + query
2. Backend expands query intelligently
3. Fetches:

   * Research papers (PubMed, OpenAlex)
   * Clinical trials
4. Ranks results based on relevance
5. AI generates insights using LLM
6. Frontend displays structured results

---

## 🎥 Demo

👉 (Add your demo video or live link here)

---

## 📌 Future Improvements

* User authentication
* Advanced AI diagnosis
* Real-time patient monitoring
* Mobile app version

---

## 👨‍💻 Author

**Vamshi Chandra**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
