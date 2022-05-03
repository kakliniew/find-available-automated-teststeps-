import spacy
from scipy import spatial
from spacy.matcher import PhraseMatcher
import numpy as np

class NlpProcessing:
    
    def __init__(self, path):
        self.nlp = spacy.load('en_core_web_lg')
        dictionary = self.__find_dictionary(path)
        self.doc = self.nlp(str(dictionary))
        

    ### prepare test steps from file
    def __find_dictionary(self, path):
        dictionary = ""
        with open(path, "r") as f2:
            data = f2.readlines()
            for x in data:
                x = x.rstrip().lstrip()
                if "@" not in x and "Scenario" not in x and "Feature" not in x and x.strip() and (x.startswith("When") or x.startswith("Given") or x.startswith("Then") or x.startswith("And")):
                    x = x.replace("When ", "").replace("Then ", "").replace("And ", "").replace("Given ", "").replace("\n","")
                    dictionary = dictionary + x + ". "
        return dictionary



    def __search_for_keyword(self, keywords):
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        
        phrase_list = [self.nlp.make_doc(text) for text in keywords]
        print(phrase_list)
        phrase_matcher.add("Text Extractor", None, *phrase_list)

        matched_items = phrase_matcher(self.doc)
        
        matched_text = []
        for match_id, start, end in matched_items:
            text = self.nlp.vocab.strings[match_id]
            span = self.doc[start: end]
            matched_text.append(span.sent.text)
        return matched_text


    ### BEST results
    def __spacy_most_similar(self, word, topn=50):
        ms = self.nlp.vocab.vectors.most_similar(
        self.nlp(word).vector.reshape(1,self.nlp(word).vector.shape[0]), n=topn)
        words = [self.nlp.vocab.strings[w].lower() for w in ms[0][0]]
        
        return set(words)

    


    def find_steps_in_doc_from_keywords(self, keywords):
        found_results = []
        for keyword in keywords:
            similar_words = self.__spacy_most_similar(keyword)
            found_steps = self.__search_for_keyword(similar_words)
            if found_steps:
                found_results.append(found_steps)
        return found_results
    
   
        
    

    # def createKeywordsVectors(keyword, nlp):
    #     doc = nlp(keyword)  # convert to document object

    #     return doc.vector


    # # method to find cosine similarity
    # def cosineSimilarity(vect1, vect2):
    #     # return cosine distance
    #     return 1 - spatial.distance.cosine(vect1, vect2)


    # # method to find similar words
    # def getSimilarWords(keyword, nlp):
    #     similarity_list = []

    #     keyword_vector = createKeywordsVectors(keyword, nlp)

    #     for tokens in nlp.vocab:
    #         if (tokens.has_vector):
    #             if (tokens.is_lower):
    #                 if (tokens.is_alpha):
    #                     similarity_list.append((tokens, cosineSimilarity(keyword_vector, tokens.vector)))

    #     similarity_list = sorted(similarity_list, key=lambda item: -item[1])
    #     similarity_list = similarity_list[:30]
        

    #     top_similar_words = [item[0].text for item in similarity_list]

    #     top_similar_words = top_similar_words[:7]
    #     top_similar_words.append(keyword)

    #     for token in nlp(keyword):
    #         top_similar_words.insert(0, token.lemma_)

    #     for words in top_similar_words:
    #         if words.endswith("s"):
    #             top_similar_words.append(words[0:len(words)-1])

    #     top_similar_words = list(set(top_similar_words))

    #     # top_similar_words = [words for words in top_similar_words if enchant_dict.check(words) == True]

    #     return top_similar_words

    
    
    # similar_keywords = getSimilarWords(keywords, nlp)
    # print(similar_keywords)




    # def spacy_similarity(self, word, topn=30):
    #     word = self.nlp.vocab[str(word)]
    #     queries = [
    #     w for w in word.vocab if w.is_lower == word.is_lower and np.count_nonzero(w.vector)]
    #     by_similarity = sorted(queries, key=lambda w: w.similarity(word), reverse=True)
    #     return [(w.lower_) for w in by_similarity[:topn+1] if w.lower_ != word.lower_]


    # # print(spacy_similarity(keywords))
