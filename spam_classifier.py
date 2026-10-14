# spam_classifier.py
# Email Spam Classifier - Internship Project
# Student: A Ganesh
#
# Flow: load data -> clean text -> train/test split -> TF-IDF ->
#       train 3 models -> evaluate -> save best model -> predict new text
#
# The script finds spam.csv in the SAME FOLDER AS THIS FILE, so it works no
# matter which folder your terminal is currently in.

import re
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

# ---------------- Settings ----------------
BASE_DIR = Path(__file__).resolve().parent      # folder that contains this script
DATASET_PATH = BASE_DIR / 'spam.csv'
MODEL_FILE = BASE_DIR / 'spam_model.joblib'
VECTORIZER_FILE = BASE_DIR / 'tfidf_vectorizer.joblib'
CONFUSION_FILE = BASE_DIR / 'confusion_matrix.png'
KEYWORDS_FILE = BASE_DIR / 'spam_keywords.png'
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Used only if the NLTK stopword list cannot be downloaded (for example, no internet).
FALLBACK_STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'of', 'at', 'by', 'for', 'with',
    'about', 'to', 'from', 'in', 'on', 'off', 'up', 'down', 'out', 'over', 'under',
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'him',
    'his', 'she', 'her', 'it', 'its', 'they', 'them', 'their', 'this', 'that',
    'these', 'those', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'not',
    'no', 'as', 'what', 'which', 'who', 'when', 'where', 'how', 'all', 'any',
}


def load_stopwords():
    """Load the English stopword list from NLTK (download it if needed)."""
    try:
        nltk.download('stopwords', quiet=True)  # needs internet the first time
        return set(stopwords.words('english'))
    except Exception:
        print('Warning: NLTK stopwords not available. Using a small built-in list.')
        print('         To fix: run  python -m nltk.downloader stopwords')
        print()
        return FALLBACK_STOPWORDS


STOP_WORDS = load_stopwords()
STEMMER = PorterStemmer()


def load_dataset(path):
    """Read the CSV file and return a clean DataFrame with label and text."""
    path = Path(path)
    if not path.exists():
        print('ERROR: dataset file not found.')
        print(f'  Expected location: {path}')
        print('  Put spam.csv in the same folder as spam_classifier.py.')
        print('  (See README.md for how to get the real dataset.)')
        sys.exit(1)

    df = pd.read_csv(path, encoding='latin-1')
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Accept the Kaggle column names (v1, v2) and a few common alternatives.
    label_col = next((c for c in ['v1', 'label', 'category', 'class'] if c in df.columns), None)
    text_col = next((c for c in ['v2', 'text', 'message', 'sms', 'email'] if c in df.columns), None)
    if label_col is None or text_col is None:
        print('ERROR: could not find the label and text columns in spam.csv.')
        print(f'  Columns found: {list(df.columns)}')
        print('  Expected: v1 (ham/spam) and v2 (message text).')
        sys.exit(1)

    df = df[[label_col, text_col]]
    df.columns = ['label', 'text']
    df = df.dropna().drop_duplicates()          # remove empty and repeated rows
    df['label'] = df['label'].astype(str).str.strip().str.lower()
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    df = df.dropna(subset=['label_num'])
    df['label_num'] = df['label_num'].astype(int)

    if df['label_num'].nunique() < 2:
        print('ERROR: the dataset must contain both ham and spam messages.')
        sys.exit(1)
    if len(df) < 2000:
        print(f'Note: this dataset has only {len(df)} messages, so it is a small demo set.')
        print('      Use the real SMS Spam Collection for results in your report.')
        print()
    return df


def clean_text(text):
    """Lowercase, keep letters only, remove stopwords, apply stemming."""
    text = str(text).lower()
    text = re.sub(r'[^a-z]', ' ', text)      # replace non-letters with space
    words = text.split()
    words = [STEMMER.stem(w) for w in words if w not in STOP_WORDS]
    return ' '.join(words)


def evaluate_model(name, model, X_test, y_test):
    """Predict on test data and return the metrics and predictions."""
    y_pred = model.predict(X_test)
    metrics = {
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, zero_division=0),
        'Recall': recall_score(y_test, y_pred, zero_division=0),
        'F1-score': f1_score(y_test, y_pred, zero_division=0),
    }
    return metrics, y_pred


def plot_confusion_matrix(y_test, y_pred, model_name):
    """Draw and save the confusion matrix as a heatmap."""
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    plt.xlabel('Predicted label')
    plt.ylabel('Actual label')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.tight_layout()
    plt.savefig(CONFUSION_FILE)
    plt.show()                               # close the window to continue


def plot_spam_keywords(model, vectorizer, top_n=15):
    """Show the words that push a message most strongly toward Spam."""
    words = np.array(vectorizer.get_feature_names_out())
    if hasattr(model, 'coef_'):              # Logistic Regression and SVM
        scores = model.coef_[0]
    else:                                    # Naive Bayes
        scores = model.feature_log_prob_[1] - model.feature_log_prob_[0]
    top = np.argsort(scores)[-top_n:]
    plt.figure(figsize=(7, 5))
    plt.barh(words[top], scores[top], color='firebrick')
    plt.xlabel('Spam indicator score')
    plt.title(f'Top {top_n} Spam-Indicating Words (stemmed)')
    plt.tight_layout()
    plt.savefig(KEYWORDS_FILE)
    plt.show()                               # close the window to continue


def predict_message(text, model, vectorizer):
    """Return (label, confidence) for one new message."""
    cleaned = clean_text(text)
    if not cleaned:                          # nothing useful left after cleaning
        return None, None
    features = vectorizer.transform([cleaned])
    pred = int(model.predict(features)[0])
    label = 'Spam' if pred == 1 else 'Ham'
    confidence = None
    if hasattr(model, 'predict_proba'):      # LinearSVC has no probabilities
        confidence = model.predict_proba(features)[0][pred]
    return label, confidence


def main():
    # 1. Load data
    df = load_dataset(DATASET_PATH)
    print('Dataset loaded. Messages per class:')
    print(df['label'].value_counts().to_string())
    print()

    # 2. Preprocess text
    df['clean_text'] = df['text'].apply(clean_text)

    # 3. Train/test split (80/20, same spam ratio in both parts)
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df['clean_text'], df['label_num'],
        test_size=TEST_SIZE, random_state=RANDOM_STATE,
        stratify=df['label_num'])

    # 4. TF-IDF vectorization (fit on training data only)
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    # 5. Train the three algorithms
    models = {
        'Naive Bayes': MultinomialNB(),
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'SVM (LinearSVC)': LinearSVC(),
    }
    results, trained, predictions = [], {}, {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        metrics, y_pred = evaluate_model(name, model, X_test, y_test)
        results.append(metrics)
        trained[name] = model
        predictions[name] = y_pred

    # 6. Compare models
    results_df = pd.DataFrame(results).set_index('Model')
    print('Model comparison on the test set:')
    print(results_df.round(4).to_string())
    print()
    ranked = results_df.sort_values(['F1-score', 'Precision'], ascending=False)
    best_name = ranked.index[0]
    best_model = trained[best_name]
    print(f'Best model (by F1-score): {best_name}')
    print()
    print(classification_report(y_test, predictions[best_name],
                                target_names=['Ham', 'Spam']))

    # 7. Visualizations
    plot_confusion_matrix(y_test, predictions[best_name], best_name)
    plot_spam_keywords(best_model, vectorizer)

    # 8. Save model and vectorizer
    joblib.dump(best_model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print(f'Saved: {MODEL_FILE.name} and {VECTORIZER_FILE.name}')
    print()

    # 9. Real-time prediction
    print('Enter an email or message to check (type quit to exit).')
    while True:
        try:
            message = input('Message: ').strip()
        except EOFError:
            break
        if message.lower() == 'quit':
            break
        label, confidence = predict_message(message, best_model, vectorizer)
        if label is None:
            print('Not enough meaningful text to classify. Try a longer message.')
        elif confidence is None:
            print(f'Prediction: {label}')
        else:
            print(f'Prediction: {label} (confidence {confidence * 100:.1f}%)')
        print()


if __name__ == '__main__':
    main()
