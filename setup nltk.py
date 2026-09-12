"""
NLTK Setup Script
Downloads required NLTK data packages

Author: Manas Baiswar
"""

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download all required NLTK data packages"""
    
    packages = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger',
        'maxent_ne_chunker',
        'words'
    ]
    
    print("Downloading NLTK data packages...")
    print("=" * 50)
    
    for package in packages:
        try:
            print(f"Downloading {package}...", end=" ")
            nltk.download(package, quiet=True)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print("=" * 50)
    print("NLTK setup completed!")

if __name__ == '__main__':
    download_nltk_data()
