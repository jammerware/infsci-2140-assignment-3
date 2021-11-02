from Classes.Document import Document
from Classes.Query import Query
from IndexingWithWhoosh.MyIndexReader import MyIndexReader

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader: MyIndexReader):
        self.indexReader = ixReader

        # eyeball mu at the average document length
        # self.mu = (self.indexReader.get_collection_length() / self.indexReader.total_doc_count()) * 1.9
        self.mu = 530
        print('estimated mu at', self.mu)

    def get_smoothed_prior(self, docNo, doc_length, postings, term_probability, mu):
        count_in_doc = 0 if docNo not in postings else postings[docNo]
        
        numerator = count_in_doc + (mu * term_probability)
        denominator = doc_length + mu

        return numerator / denominator

    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query: Query, topN, smoothing='dirichlet'):        
        query_content = []
        for token in query.queryContent:
            if self.indexReader.contains_token(token):
                query_content.append(token)

        # retrieve docs containing any query term
        docs = self.indexReader.get_docs_by_tokens(query_content)

        # for each term in each doc, compute the smoothed prior probability of each 
        results = []

        # pre-cache posting lists and term probabilities for speed
        postings = {}
        term_probabilities = {}

        for token in query.queryContent:
            postings[token] = self.indexReader.getPostingList(token)
            term_probabilities[token] = self.indexReader.get_token_probability(token)

        # iterate through docs and score each for each term
        # summing the scores for each term, i guess?
        for doc in docs:
            score = 0
            doc_length = self.indexReader.getDocLength(doc.docnum)

            for token in query_content:
                score += self.get_smoothed_prior(doc.docnum, doc_length, postings[token], term_probabilities[token], self.mu)

            results.append({
                'docId': doc.docnum,
                'docNo': doc['doc_no'],
                'score': score,
                'hit': doc
            })

        # sort results by score
        results = sorted(results, key = lambda x: x['score'], reverse=True)
        
        # trim top results and project to Document
        top_results = results[:topN]
        max_score = top_results[0]['score']
        min_score = top_results[-1]['score']
        print('maxmin', max_score, min_score)
        print('range', max_score - min_score)

        return [Document(docId=r['docId'], docNo=r['docNo'], score=r['score']) for r in top_results]