from scipy.sparse import lil_matrix
from scipy.sparse.linalg import svds
import numpy as np
from numpy import linalg as LA

from typing import List, Tuple
from backend.classes.Article import Article
from backend.classes.Text import Text


class SearchStruct:
    def __init__(self, articles: List[Article]):
        """
        - Creates dictionary of words based on Articles list
        - updates their representation as bag_of_words
        - creates matrix word X article, scales it by IDF and normalizes it
        """
        self.articles = articles
        self.dictionary = self.create_dictionary()
        self.matrix = self.texts_to_matrix()
        self.scale_by_IDF()
        self.matrix = self.normalize(self.matrix)
        self.noiseless_matrixes = {}  # cached (up to 5) svd-processed matrixes

    def create_dictionary(self):
        """
        creates dictionary of all words which appear in articles
        :return: dictionary {"word": idx, ...}
        """
        words_set = set()
        for article in self.articles:
            words_set = words_set.union(set(article.text.words))
        dictionary = {}
        idx = 0
        for word in words_set:
            dictionary[word] = idx
            idx += 1
        return dictionary

    def texts_to_matrix(self):
        """ joins all BOWs into a single matrix """
        BOWs = []
        for article in self.articles:
            BOWs.append(article.text.convert_to_BOW(self.dictionary))
            article.text = None  # free memory for optimization
        return np.array(BOWs, dtype=float).transpose()

    def scale_by_IDF(self):
        N = self.matrix.shape[1]
        IDF = np.log2(N / np.count_nonzero(self.matrix, axis=1))  # / logN/nw, nw-nr of documents in which word exists
        for i in range(len(self.dictionary)):
            self.matrix[i] *= IDF[i]

    def normalize(self, matrix):
        return matrix / LA.norm(matrix, axis=0)

    def search(self, query_text: str, top_k=1, lra_k=None) -> List[Tuple[Article, float]]:
        """
        finds @top_k matches for given @query_text
        :param lra_k: if set, uses SVD and low rank approximation by @lra_k eigenvalues
        :return: list of tuples: (Article, correlation)
        """
        query = Text(query_text)
        query.convert_to_BOW(self.dictionary)
        query.normalize_BOW()

        if lra_k is None:
            mx = self.matrix
        else:
            if lra_k not in self.noiseless_matrixes.keys():  # try to find cached matrix
                if len(self.noiseless_matrixes) > 5:  # clear cache
                    self.noiseless_matrixes = {}
                self.noiseless_matrixes[lra_k] = self.normalize(self.remove_noise(lra_k))
            mx = self.noiseless_matrixes[lra_k]

        products = np.zeros(mx.shape[1])  # dot product used as probability measure
        for c in range(mx.shape[1]):
            products[c] = np.dot(mx[:, c], query.BOW)

        best_articles_at = np.argpartition(products, -top_k)[-top_k:]
        results = [(self.articles[idx], products[idx]) for idx in best_articles_at]
        results = sorted(results, key=lambda res: res[1], reverse=True)

        print(f"searched phrase : {query_text}") # additional console print
        for res in results:
            print(f"{res[0]}\n correlation: {res[1]}")

        return results

    def remove_noise(self, k=10):
        """
        calculates svd and low-rank app. of sparse matrix
        :return: low rank approximation of self.matrix with first k single values
        """
        mx = lil_matrix(self.matrix)
        u, s, vt = svds(mx, k=k, which='LM')
        s1 = np.diag(s)
        lrapp = u@s1@vt
        return lrapp

    def __str__(self):
        return f"SearchStruct with {len(self.articles)} indexed articles"

