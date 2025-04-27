import re
import string
import unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import pdfminer.settings
import pdfminer.high_level

# Configure pdfminer
pdfminer.settings.STRICT = False

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ---------- PDF Text Extraction ----------
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as fp:
        return pdfminer.high_level.extract_text(fp)

# ---------- Normalization Functions ----------
def remove_non_ascii(words):
    return [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') for word in words]

def to_lowercase(words):
    return [word.lower() for word in words]

def remove_punctuation(words):
    return [re.sub(r'[^\w\s]', '', word) for word in words if re.sub(r'[^\w\s]', '', word) != '']

def replace_numbers(words):
    p = inflect.engine()
    return [p.number_to_words(word) if word.isdigit() else word for word in words]

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]

def stem_words(words):
    stemmer = LancasterStemmer()
    return [stemmer.stem(word) for word in words]

def lemmatize_verbs(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos='v') for word in words]

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = lemmatize_verbs(words)
    return words

# ---------- KMP ALGORITHM ----------
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
    lps = [0] * M
    j = 0

    computeLPSArray(pat, M, lps)

    i = 0
    found = False
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print(f"Found pattern '{''.join(pat)}' at index {i - j}")
            j = lps[j - 1]
            found = True

        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    if not found:
        print(f"Pattern '{''.join(pat)}' not found.")

def computeLPSArray(pat, M, lps):
    length = 0
    i = 1
    lps[0] = 0

    while i < M:
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

# ---------- Main Pipeline ----------
def process_pdf(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    expanded_text = contractions.fix(raw_text)
    tokenized_words = word_tokenize(expanded_text)
    normalized_words = normalize(tokenized_words)
    return normalized_words

# ---------- Entry Point ----------
if __name__ == "__main__":
    # Replace with the correct path to your resume PDF
    pdf_path = r"C:\Users\aswan\Downloads\resume.pdf"

    final_words = process_pdf(pdf_path)
    normalized_text = ' '.join(final_words)

    print("Token list:", final_words)
    print("Normalized Text:", normalized_text)

    # Example search patterns
    # Example search patterns
    # Example search patterns
search_terms = [
        
    "python", "flask", "django", "react", "node.js", "machine learning",
    "sql", "mongodb", "aws", "docker", "kubernetes", "java", "c++", "html",
    "css", "javascript", "linux", "git", "rest api", "graphql", "ai",
    "cloud computing", "dsa", "devops", "angular", "vue.js", "swift", "ruby", "php",
    "tensorflow", "pytorch", "jupyter", "big data", "hadoop", "scala",
    "apache spark", "nlp", "data science", "deep learning", "reinforcement learning", "internet of things",
    "xgboost", "keras", "scikit-learn", "opencv", "computer vision", "tableau",
    "power bi", "sql server", "nosql", "etl", "fastapi", "jupyter notebook", 
    "google colab", "eclipse ide", "latex", "ms office", "c", "cyber security", "iot", "graphic design",
    "go", "typescript", "rust", "bootstrap", "tailwind css", "next.js", "express.js",
    "jenkins", "github actions", "firebase", "oracle", "redis",
    "jest", "selenium", "postman", "api testing", "unit testing",
    "vscode", "intellij idea", "jira", "notion",
    "figma", "ui/ux design", "system design", "agile", "scrum" ]
found_keywords = []

for term in search_terms:
    if term in final_words:
        print(f"Found keyword '{term}'")
        found_keywords.append(term)
    else:
        print(f"Keyword '{term}' not found.")

# Write found keywords to a file
with open("found_keywords.txt", "w") as f:
    for keyword in found_keywords:
        f.write(keyword + "\n")

print("\nFound keywords saved to 'found_keywords.txt'")


