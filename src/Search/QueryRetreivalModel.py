from Classes.Query import Query
from IndexingWithWhoosh.MyIndexReader import MyIndexReader

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader: MyIndexReader):
        self.indexReader = ixReader
        return


    def get_prior(self, doc, token, smoothing):
        doc_length = self.indexReader.getDocLength(doc)
        count_in_doc = len(self.indexReader.getPostingList(token))

        if smoothing == 'laplace':
            return 0

    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query: Query, topN, smoothing='dirichlet'):
        priors = {}
        
        # retrieve docs containing any query term
        docs = self.indexReader.get_docs_by_tokens(query.getQueryContent())

        # for each term in each doc, compute the smoothed prior probability of each
        for doc in docs:
            for token in query.queryContent:
                self.get_prior()