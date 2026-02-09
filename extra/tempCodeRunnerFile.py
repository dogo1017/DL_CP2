from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression # A good starting model for text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import wikipedia
from word2number import w2n
import requests
from bs4 import BeautifulSoup
