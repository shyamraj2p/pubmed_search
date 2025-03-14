# PubMed Paper Fetcher

## 📌 Overview
This project allows users to fetch research papers from **PubMed** that contain company-affiliated authors. It retrieves paper details such as **title, publication date, author affiliations, and corresponding author emails**. The program supports command-line execution with options to **save results to a CSV file** and enable **debug mode**.

## 📂 Code Organization
```
├── pubmed_fetcher.py      # Main script to fetch and process PubMed data
├── pyproject.toml         # Poetry configuration file
├── README.md              # Documentation
└── requirements.txt       # Dependencies list (auto-managed by Poetry)
```

## 🔧 Installation & Setup

### **1️⃣ Install Poetry**
If you haven't installed Poetry, run:
```bash
pip install poetry
```

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/shyamraj2p/pubmed_search.git
cd pubmed_search
```

### **3️⃣ Install Dependencies**
Run the following command to install all required dependencies:
```bash
poetry install
```

### **4️⃣ Activate the Virtual Environment**
```bash
poetry shell
```

## 🚀 Execution

### **Run the Program with a Query**
```bash
python pubmed_fetcher.py "COVID-19[Title] AND Nature[Journal]"
```

### **Enable Debug Mode**
```bash
python pubmed_fetcher.py "COVID-19[Title]" -d
```

### **Save Results to CSV**
```bash
python pubmed_fetcher.py "COVID-19[Title]" -f results.csv
```

### **Display Help Message**
```bash
python pubmed_fetcher.py -h
```

## 🛠️ Tools & Libraries Used
- **Requests** ([docs](https://docs.python-requests.org/en/latest/)): Fetches data from the PubMed API.
- **argparse** ([docs](https://docs.python.org/3/library/argparse.html)): Handles command-line arguments.
- **XML.etree.ElementTree** ([docs](https://docs.python.org/3/library/xml.etree.elementtree.html)): Parses PubMed XML responses.
- **CSV Module** ([docs](https://docs.python.org/3/library/csv.html)): Saves output in CSV format.
- **ThreadPoolExecutor** ([docs](https://docs.python.org/3/library/concurrent.futures.html)): Enables multithreading to fetch paper details efficiently.

## 📌 Notes
- The script **automatically handles API rate limits** by implementing exponential backoff.
- Company-affiliated authors are identified using keywords like **pharma, biotech, corp, gmbh, medtech, etc.**
- Email extraction is based on a regex pattern matching common email formats.

## 🤝 Contribution
Feel free to fork this repository, raise issues, or submit pull requests to improve the functionality!

---

📧 **Contact:** If you have any questions, reach out at [your email or GitHub issues].

