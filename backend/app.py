from flask import Flask, request
from pyspark.sql import SparkSession
from pyspark import SparkContext

application = Flask(__name__)
#application.config["APPLICATION_ROOT"]="/flask"
@application.route('/')
def test_index():
	return "<h>Hello World</h>"
@application.route('/api/bestseller?start=<cursor_start>&end=<cursor_end>')
def get_bestseller(self, cursor_start, cursor_end):
	pass
@application.route('/api/behavior', methods=["POST"])
def post_behavior():
	data = request.get_json()
	spark = SparkSession\
			.builder\
			.appName('writeBehavior')\
			.master("spark://")\
			.getOrCreate()
	# maybe try local

	# go data through model
	# maybe not use pyspark to store

	# convert json to rdd
	behavior = spark.read.json(sc.parallelize([data]))
	#.rdd
	# write to mongodb
	behavior.write.format('**').mode('append').save()
	pass
	# GET use pyspark to query
@application.route('/api/commodity/<commodity_id>')
def get_commodity_detail(commodity_id):
	# still pyspark
	#return "hello"+commodity_id
	spark = SparkSession\
			.builder\
			.appName('readCommodity')\
			.master("spark://")\
			.getOrCreate()
	# maybe try local

	# specify the uri, db and collection to read
	pipeline = "{'$match':{'commodity_id',"+commodity_id+"}}"
	df = spark.read.format("**")\
			.option('uri','mongodb://IP_ADDR/recommendation.commodity')\
			.option('pipeline',pipeline)\
			.load()
	return df.toJSON()
	# pass

# @application.route('/api/user',methods=["POST"])
# @application.route('/api/user/<user_id>',methods=["GET","PUT"])
# @application.route('/api/cart/<user_id>',methods=["GET","DELETE"])
if __name__ == "__main__":
	application.run(host='0.0.0.0')
