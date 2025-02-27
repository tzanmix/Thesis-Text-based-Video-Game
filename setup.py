import subprocess
try:
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    print("Η εγκατάσταση ήταν επιτυχής.")
except subprocess.CalledProcessError:
    print("Αποτυχία. Ελέγξτε αν το pip είναι εγκαταστημένο.")

#####
import nltk
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger") 