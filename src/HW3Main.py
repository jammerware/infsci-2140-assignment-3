import datetime
import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery


startTime = datetime.datetime.now()

# read the index generated from H2MainWhoosh.py
index = MyIndexReader.MyIndexReader("trectext")

# create the retrieval model
search = QueryRetreivalModel.QueryRetrievalModel(index)

# create a query extractor and load the queries from topics.txt
extractor = ExtractQuery.ExtractQuery()
queries = extractor.getQuries()

# loop through the queries and get their results
for query in queries:
    print(query.topicId, "\t", query.queryContent)
    results = search.retrieveQuery(query, 20)
    rank = 1
    # for result in results:
    #     print(query.getTopicId(), " Q0 ", result.getDocNo(), ' ', rank, " ", result.getScore(), " MYRUN",)

endTime = datetime.datetime.now()
print("load index & retrieve the token running time: ", endTime - startTime)
