# Email Spam Classifier - How to Run in VS Code

Student: A Ganesh

## Files in this folder

| File | Purpose |
|---|---|
| `spam_classifier.py` | Main program (cleans text, trains Naive Bayes / Logistic Regression / SVM, evaluates, predicts) |
| `spam.csv` | Dataset with columns `v1` (ham/spam) and `v2` (message text) |
| `requirements.txt` | Python libraries to install |
| `generate_sample_dataset.py` | Script that created the demo `spam.csv` (optional) |
| `README.md` | These instructions |

## IMPORTANT: about the included spam.csv

The `spam.csv` in this package is a **synthetic demo dataset** (950 template-generated
messages: 700 ham, 250 spam, including some email-style messages). It is **not** the
UCI SMS Spam Collection. It lets the project run immediately, but because the messages
are template-based, the scores on it are unrealistically high and must **not** be
reported as your project's results.

For your report, use the real dataset:

1. Open https://www.kaggle.com/uciml/sms-spam-collection-dataset and log in (free account).
2. Click Download, unzip, and you get `spam.csv`.
3. Copy it into this folder and replace the demo `spam.csv`.
4. Run the program again. Record the real output in Sections 21 and 23 of your report.

The program reads both files the same way (columns `v1` and `v2`).

## Steps to run in VS Code

1. **Install Python** 3.9 or later from python.org (tick "Add Python to PATH" on Windows).
2. **Install the VS Code Python extension** (Extensions icon, search "Python", Install).
3. **Open this folder in VS Code:** File > Open Folder, and choose the folder that contains
   `spam_classifier.py` and `spam.csv`.
4. **Open a terminal:** Terminal > New Terminal.
5. **(Recommended) Create a virtual environment:**
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS / Linux: `python3 -m venv venv` then `source venv/bin/activate`
   If VS Code asks to use the new environment, click Yes.
6. **Install the libraries:** `pip install -r requirements.txt`
7. **Run the program:** `python spam_classifier.py`
   (or open the file and click the Run triangle at the top right).
8. **Close each chart window** (confusion matrix, then keyword chart) so the program continues.
9. **Type a message** at `Message:` to get Spam or Ham. Type `quit` to stop.

Output files created in this folder: `spam_model.joblib`, `tfidf_vectorizer.joblib`,
`confusion_matrix.png`, `spam_keywords.png`.

## Fixing the FileNotFoundError

The program now looks for `spam.csv` in the same folder as `spam_classifier.py`, no matter
which folder the terminal is in. If you still see "dataset file not found", the file is
missing from that folder or is named differently (for example `spam (1).csv` or
`spam.csv.csv`). Rename it to exactly `spam.csv`. Turn on "File name extensions" in Windows
Explorer to check.

## Other common problems

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in the same terminal and environment you run the program from. |
| Warning about NLTK stopwords | Connect to the internet and run `python -m nltk.downloader stopwords`. The program still runs with a small built-in list. |
| `could not find the label and text columns` | The CSV must have columns `v1` (ham/spam) and `v2` (text). |
| Wrong Python used by VS Code | Press Ctrl+Shift+P, choose "Python: Select Interpreter", and pick the one with your `venv`. |
