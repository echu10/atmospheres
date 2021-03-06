from bson.code import Code
from atmospheres.db.datastore import DataStore
from atmospheres.resources.sentiment import Sentiment, Sentiments
from atmospheres.ingestion.utils import get_mongo_reader


class SentimenetAgrregator(object):
	"""
	This class exposes various methods to return aggregated data from datastore
	"""
	def __init__(self, app=None):
		if app:
			self.db = app.db
		else:
			self.db = get_mongo_reader()

		

	def get_sentiment(self, zipcode, start_time, end_time):
		"""
		This method returns the aggregated sentiment information for a particular zipcode.
		"""
		postive_sentiment_count = self.db.find( { "zipcode" : zipcode, 
									  "sentiment" : postive,
						      		  "created_at" : {"$gt": start_time, "$lt" : end_time} } ).count()
		negative_sentiment_count = self.db.find( { "zipcode" : zipcode, 
									  "sentiment" : negative,
						      		  "created_at" : {"$gt": start_time, "$lt" : end_time} } ).count()
		return Sentiment(zipcode, postive_zip_count, negative_zip_count, start_time, end_time)

	def get_sentiments(self, zipcodes, start_time, end_time):
		"""
		This method returns the aggregated list of sentiments for provided zipcodes.
		"""
		zipcode_sentiment_map =  {}
		for zipcode in zipcodes:
			positive_sentiment_count = self.db.find( { "zipcode" : zipcode, 
									  "sentiment" : postive,
						      		  "created_at" : {"$gt": start_time, "$lt" : end_time} } ).count()
			negative_sentiment_count = self.db.find( { "zipcode" : zipcode, 
									  "sentiment" : negative,
						      		  "created_at" : {"$gt": start_time, "$lt" : end_time} } ).count()
			zipcode_sentiment_map[zipcode] = {
				"positive_sentiment_count": positive_sentiment_count,
				"negative_sentiment_count": negative_sentiment_count,
			}
		return Sentiments(zipcode_sentiment_map, start_time, end_time)	

	def get_zipcodes(self, sentiment_type, percentage): 
		"""
		This method returns list of zipcodes whose sentiment count is higher than the given percentage
		for particular sentiment(positive, negative).
		"""
		zipcode_sentiment_list =  []
		reducer = Code("""
               		   function(obj, prev){
                       		prev.count++;
                	   }
              		   """)
		# group by taken from http://api.mongodb.org/python/current/examples/aggregation.html
		total_zipcode = self.db.group(key={"zipcode": 1}, condition={}, initial={"count": 0}, reduce=reducer)
		total_sentiment = self.db.group(key={"zipcode": 1}, condition={"sentiments": sentiment_type}, initial={"count": 0}, reduce=reducer)

		# zip(item1, item2) e.g lst1 = [1,2,3]; lst2= [4,5,7]; zip(lst1, lst2) will return [(1,4), (2,5), (3,7)]
		zipped = zip(total_sentiment, total_zipcode)
		for item in zipped:
			result = item[0]["count"]*100/item[1]["count"]
			if result > percentage:
				zipcode_sentiment_list.append(zipcode)

		return zipcode_sentiment_list


	def get_sentiment_count(self, sentimen_type, zipcode,start_time, end_time):	
		"""
		This method returns the number of sentiment count for particular type of sentiment for a specific zipcode
		"""
		sentiment_count = self.db.get_sentiment_count(sentimen_type, zipcode, start_time, end_time)
		
		return sentiment_count



			
			