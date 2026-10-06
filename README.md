# Card Guardian 🛡️

**Card Guardian** is an AI-powered assistant designed to navigate complex credit card benefit guides, terms, and fine print. Using tree-based document structure reasoning powered by [PageIndex](https://github.com/vectara/pageindex) and Google Gemini (via LiteLLM), it accurately determines coverage eligibility (e.g., cell phone protection, travel insurance, purchase warranties) without relying on traditional vector embeddings.

---

## 🚀 Features

- **Structural Reasoning**: Directly navigates the document hierarchy rather than chunking text arbitrarily.
- **Accurate Grounding**: Answers questions using *only* the verified legal terms from your credit card agreement.
- **Zero Hallucination**: Isolates the exact sections and clauses applicable to your claim.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API key

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/Trisshita/Card-Gaurdian.git
cd Card-Gaurdian
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root based on `.env.example`:
```bash
cp .env.example .env
```
Add your Gemini API key to `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📖 Usage

### Step 1: Index your Card Benefits Document
Place your credit card agreement PDF (e.g., `card.pdf`) in the project directory, then generate the structured document tree:
```bash
python run_pageindex.py --pdf_path card.pdf
```
This generates `document_structure.json` containing the hierarchical outline and content sections.

### Step 2: Query the Advocate
Run the inquiry application:
```bash
python app.py
```
This will parse the question against the document tree, retrieve the exact clauses, and output a clear, consumer-friendly answer.

---

## 📁 Project Structure

```text
├── card.pdf            # Sample credit card benefits agreement
├── run_pageindex.py    # Document indexer & structure generator
├── app.py              # Main AI consumer advocate query runner
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
└── README.md           # Project documentation
```
