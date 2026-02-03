
# SPEND — Smart Processing of Expenses & Data

SPEND is a personal expense-tracking and analytics system that transforms unstructured financial documents—such as receipts and payment screenshots—into structured, analyzable transaction data.  
The project focuses on data extraction, normalization, and insight generation rather than manual expense entry.

---

## 🎯 Project Objective

The goal of SPEND is to help individuals understand their spending behavior by:
- Eliminating manual data entry  
- Structuring messy real-world financial data  
- Providing clear analytical views of expenses over time  

While designed as a personal finance tool, the system is intentionally built using **data-analysis principles** to demonstrate real-world data ingestion, processing, and visualization.

---

## 🧠 What the Project Does

- Accepts images of receipts and payment confirmations  
- Extracts raw text using OCR  
- Converts unstructured text into structured transaction records using an LLM  
- Normalizes transactions across different document types (receipts, UPI payments, etc.)  
- Assigns confidence scores to extracted data  
- Stores transactions persistently  
- Provides an interactive dashboard for analysis and exploration

---

## 🧩 System Architecture

```
Image Upload
↓
OCR (Tesseract)
↓
LLM-based Semantic Parsing (Gemini)
↓
Normalization + Confidence Scoring
↓
SQLite Database
↓
Analytics Queries
↓
Interactive Dashboard (Streamlit)
```

Each component is modular and reusable, allowing the system to scale or integrate with APIs and other frontends.

---

## 🛠️ Tech Stack

**Language & Core**
- Python

**Data Extraction**
- Tesseract OCR  
- Pillow / OpenCV  

**Semantic Parsing**
- Gemini LLM (free tier, rate-limited with throttling)

**Data Processing & Analysis**
- Pandas

**Storage**
- SQLite

**Visualization & UI**
- Streamlit

---

## 📊 Dashboard Features

- Upload single or multiple expense images  
- Live processing feedback with status indicators  
- Spending overview and transaction history  
- Analysis by:
  - Merchant  
  - Payment method / wallet  
  - Time (daily / monthly trends)  
- Detection of unusually high expenses  
- Automatic dashboard refresh on new data ingestion  

The dashboard is designed to remain simple and personal, while still supporting analytical exploration.

---

## 🔒 Handling Real-World Constraints

- **API Rate Limits**  
  The system includes throttling and retry logic to gracefully handle free-tier LLM request limits.

- **Data Reliability**  
  Each transaction includes a confidence score based on extraction quality, allowing low-confidence data to be identified or filtered.

These design decisions reflect real-world data system constraints rather than idealized assumptions.

---

## 🚀 How to Run the Project

### 1. Create and activate virtual environment

```bash
python -m venv myEnv
myEnv\Scripts\Activate
```

### 2. Install dependencies

```bash
pip install streamlit pandas pytesseract pillow opencv-python google-genai
```

### 3. Set environment variable

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the dashboard

```bash
python -m streamlit run dashboard/dashboard.py
```

---

## 📁 Project Structure

```
SPEND/
│
├── main.py                # Core ingestion pipeline
├── dashboard/
│   └── dashboard.py       # Streamlit dashboard
├── analytics/
│   └── queries.py         # Analytical queries
├── llm/
│   ├── gemini_client.py   # LLM interaction
│   └── prompt.py
├── ocr/
│   └── image_utils.py
├── core/
│   ├── normalizer.py
│   └── confidence.py
├── storage/
│   └── db.py
├── spend.db               # SQLite database
└── README.md
```

---

## 📌 Key Takeaways

* Demonstrates end-to-end data handling from unstructured sources
* Emphasizes analytical thinking over raw automation
* Handles real-world issues such as noisy data and API limits
* Designed to be explainable, extensible, and interview-ready

---

## 🔮 Future Improvements

* Category-level expense classification
* Exporting data to CSV / Excel
* Backend API for multi-user support
* Advanced trend analysis and forecasting

---

## 👤 Author

Developed as a personal project to explore practical data ingestion, analysis, and visualization using real-world financial data.

---

### ✅ This README is now:
- Markdown-valid  
- Recruiter-friendly  
- Analyst-aligned  
- GitHub-ready  
- Interview-safe  
