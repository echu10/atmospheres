from pymongo import MongoClient


class DataStore(object):
    DEFAULT_DATABASE = "CSC868"
    DEFAULT_COLLECTION = "tweets"

    def __init__(self, database=DEFAULT_DATABASE,collection=DEFAULT_COLLECTION):
        self.client = MongoClient()
        self.db = self.client[database]
        self.collection = self.db[collection]

    def text_regex_query(self, regex):
        """ returns one document from db whose text field matches regex """
        query = {}
        query["text"] = {"$regex":regex}
        return self.collection.find_one(query)

    def get_N_results(self, regex, n):
        """ returns N results from the db whose text field matches regex """
        query = {}
        query["text"] = {"$regex":regex}
        cursor = self.collection.find(query)

        res = [cursor.next() for i in range(n)]
        return res

    def write(self, data):
        """ writes data to db """
        self.collection.insert(data)

    def read(self):
        """reads data from db"""
        self.collection.find()  

    def get_sentiment_count(self, sentiment_type, zipcode, start_time, end_time): 
        
        condition = { 
                          'sentiment' : sentiment_type,
                          'created_at' : {'$gt': start_time, '$lt' : end_time},
                    }
        
        if(zipcode):
            condition["zipcode"] = zipcode

        sentiment_count = self.collection.find(condition).count()

        return sentiment_count

    def close(self):
        self.client.close()

# def main():
#     db = DataStore()
#     import datetime;
#     import pdb; pdb.set_trace()
#     result = db.get_sentiment_count("positive", "94105", datetime.datetime.now() - datetime.timedelta(days=10), datetime.datetime.now())
#     print result

if __name__ == "__main__":
    main()