# PubMed Paper Fetcher

## Overview

This program fetches research papers from PubMed based on a given search query. It extracts details such as the title, publication date, non-academic authors, company affiliations, and corresponding author emails.

## Project Structure

```
├── pubmed_fetcher.py      # Main script to fetch and process PubMed data
├── pyproject.toml         # Poetry configuration file
├── README.md              # Documentation
├── requirements.txt       # Optional dependency list
```

## Installation

This project uses Poetry for dependency management. Ensure Poetry is installed on your system before proceeding.

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/your-username/pubmed_search.git
cd pubmed_search
```

### 2️⃣ Install Dependencies

```sh
poetry install
```

### 3️⃣ Activate the Virtual Environment (Optional)

```sh
poetry shell
```

## Execution

### Running the Script Manually

```sh
poetry run python pubmed_fetcher.py "COVID-19[Title] AND Nature[Journal]"
```

### Running via Executable Command (Recommended)

The project provides an executable command `get-papers-list` via Poetry.

#### 🔹 Run the Program

Using Poetry directly:

```sh
poetry run get-papers-list "COVID-19[Title] AND Nature[Journal]"
```

If inside the Poetry shell:

```sh
get-papers-list "COVID-19[Title] AND Nature[Journal]"
```

## Command-line Options

| Option        | Description                                    |
| ------------- | ---------------------------------------------- |
| `-h, --help`  | Display usage instructions                     |
| `-d, --debug` | Print debug information during execution       |
| `-f, --file`  | Save results to a CSV file instead of printing |

## Tools and Dependencies

- **Poetry**: Dependency management ([Docs](https://python-poetry.org/))
- **Requests**: HTTP requests for PubMed API ([Docs](https://docs.python-requests.org/))
- **argparse**: Command-line argument parsing ([Docs](https://docs.python.org/3/library/argparse.html))
- **ChatGPT**: Assisted in development and documentation improvements([chat link](https://chatgpt.com/share/67d44043-872c-800d-b68d-a38026ddc4ab))
### 🚀 Features

- Search for articles using PubMed's ESearch API

- Retrieve detailed metadata using EFetch API

- Save results as a CSV file

- Command-line interface for easy execution

- Rate-limit handling (avoids HTTP 429 errors)

- Multi-threaded execution for faster processing

  ### Result
![image](https://github.com/user-attachments/assets/184fffa6-30d1-4fae-8e0b-267f7c9e26c7)

## Updating Code on GitHub

To push changes to GitHub:

```sh
git add .
git commit -m "Updated README with get-papers-list details"
git push origin main
```

