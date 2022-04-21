import spacy
from scipy import spatial
from spacy.matcher import PhraseMatcher
import numpy as np


# spacy english model (large)
nlp = spacy.load('en_core_web_lg')

### prepare test steps from file
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
    
    
dictionary = find_dictionary("example.feature")
doc = nlp(str(dictionary))
print(doc)


def createKeywordsVectors(keyword, nlp):
    doc = nlp(keyword)  # convert to document object

    return doc.vector


# method to find cosine similarity
def cosineSimilarity(vect1, vect2):
    # return cosine distance
    return 1 - spatial.distance.cosine(vect1, vect2)


# method to find similar words
def getSimilarWords(keyword, nlp):
    similarity_list = []

    keyword_vector = createKeywordsVectors(keyword, nlp)

    for tokens in nlp.vocab:
        if (tokens.has_vector):
            if (tokens.is_lower):
                if (tokens.is_alpha):
                    similarity_list.append((tokens, cosineSimilarity(keyword_vector, tokens.vector)))

    similarity_list = sorted(similarity_list, key=lambda item: -item[1])
    similarity_list = similarity_list[:30]
    

    top_similar_words = [item[0].text for item in similarity_list]

    top_similar_words = top_similar_words[:7]
    top_similar_words.append(keyword)

    for token in nlp(keyword):
        top_similar_words.insert(0, token.lemma_)

    for words in top_similar_words:
        if words.endswith("s"):
            top_similar_words.append(words[0:len(words)-1])

    top_similar_words = list(set(top_similar_words))

    # top_similar_words = [words for words in top_similar_words if enchant_dict.check(words) == True]

    return top_similar_words

  
keywords = 'find'
similar_keywords = getSimilarWords(keywords, nlp)
print(similar_keywords)

found_words = search_for_keyword(similar_keywords, doc, nlp)
print("znalezione: ")
print(found_words)


def spacy_similarity(word, topn=10):
    word = nlp.vocab[str(word)]
    queries = [
      w for w in word.vocab if w.is_lower == word.is_lower and np.count_nonzero(w.vector)]
    by_similarity = sorted(queries, key=lambda w: w.similarity(word), reverse=True)
    return [(w.lower_) for w in by_similarity[:topn+1] if w.lower_ != word.lower_]


print(spacy_similarity(keywords))


### BEST results
def spacy_most_similar(word, topn=30):
    ms = nlp.vocab.vectors.most_similar(
    nlp(word).vector.reshape(1,nlp(word).vector.shape[0]), n=topn)
    words = [nlp.vocab.strings[w].lower() for w in ms[0][0]]
    
    return set(words)

words = spacy_most_similar(keywords)
print(words)

