from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from spacy.matcher import PhraseMatcher
from scipy import spatial
import spacy

#### Solution with fetching synonyms from page

nlp = spacy.load('en_core_web_lg')

#### almost working version 
def search_for_keyword(keywords, doc_obj, nlp):
    phrase_matcher = PhraseMatcher(nlp.vocab)
    
    phrase_list = [nlp.make_doc(text) for text in keywords]
    print(phrase_list)
    phrase_matcher.add("Text Extractor", None, *phrase_list)

    matched_items = phrase_matcher(doc_obj)
    
    matched_text = []
    for match_id, start, end in matched_items:
        text = nlp.vocab.strings[match_id]
        span = doc_obj[start: end]
        matched_text.append(span.sent.text)
    return matched_text

def find_synonym(string):
    """ Function to find synonyms for a string"""
    try:
        # Remove whitespace before and after word and use underscore between words
        stripped_string = string.strip()
        fixed_string = stripped_string.replace(" ", "_")
        print(f"{fixed_string}:")
        # Set the url using the amended string
        my_url = f'https://thesaurus.plus/thesaurus/{fixed_string}'
        # Open and read the HTMLz
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        # Parse the html into text
        page_soup = soup(page_html, "html.parser")
        word_boxes = page_soup.find("ul", {"class": "list paper"})
        results = word_boxes.find_all("div", "list_item")
        # Iterate over results and print
        result_list = []
        for result in results:
            print(result.text)
            result_list.append(result.text.strip())
        result_list.append(fixed_string)
        print(result_list)
        return result_list
    except HTTPError:
        if "_" in fixed_string:
            print("Phrase not found! Please try a different phrase.")

        else:
            print("Word not found! Please try a different word.")


def find_dictionary(path):
    dictionary = ""
    with open(path, "r") as f2:
        data = f2.readlines()
        for x in data:
            x = x.rstrip().lstrip()
            if "@" not in x and "Scenario" not in x and "Feature" not in x and x.strip() and (x.startswith("When") or x.startswith("Given") or x.startswith("Then") or x.startswith("And")):
                x = x.replace("When ", "").replace("Then ", "").replace("And ", "").replace("Given ", "").replace("\n","")
                dictionary = dictionary + x + ". "
    return dictionary

if __name__ == "__main__":
    dictionary = find_dictionary("example.feature")
    doc = nlp(dictionary)
    for senc in doc.sents:
        print(senc)
    found = find_synonym("find")
    matched = search_for_keyword(found, doc, nlp)
    print(matched)
    
    
    
    
