from flask import Flask, request, Response, jsonify
#from pyspark.sql import SparkSession
#from pyspark import SparkContext
from pymongo import MongoClient
import json
from bson.json_util import dumps
import sys
sys.path.append('../atrank')
from inference import Inference

application = Flask(__name__)
#application.config["APPLICATION_ROOT"]="/flask"
@application.route('/api')
def test_index():
    return "<h>Hello World</h>"
@application.route('/api/bestseller')
def get_bestseller():
    start = request.args.get("start")
    limit = request.args.get("limit")
    # using spark session
    '''
    spark = SparkSession\
            .builder\
            .appName('getBestSeller')\
            .master("spark://")\
            .getOrCreate()
    pipeline = "{'$match':{'salesRank.Electronic','$gt: "+str(start)+", $lt: "+str(start+limit)+"'}}"
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option('uri','mongodb://IP_ADDR/recommendation.commodity')\
            .option('pipeline',pipeline)\
            .load()
    return df.toJSON()
    '''
    # using pymongo
    client = MongoClient('localhost',27017)
    collection = client.recommendation.bestitems
    result = collection.find(skip=int(start)-1,limit=int(limit)).sort("sales_rank.Electronics",1)
    res = dumps(result)
    # result: pymongo.cursor.Cursor object, need to transfer to json
    return Response(res,mimetype='application/json')

@application.route('/api/behavior', methods=["POST"])
def post_behavior():
    actions = request.get_json()
    infer_obj = Inference(actions)
    max_asin = infer_obj.inference(actions)
    return jsonify(max_asin)
    # using spark
    '''
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
    # behavior = spark.read.json(sc.parallelize([data]))
    behavior = spark.read.json(data)
    #.rdd
    # write to mongodb
    behavior.write.format('com.mongodb.spark.sql.DefaultSource').mode('append').save()
    pass
    # GET use pyspark to query
    '''

@application.route('/api/commodity/<int:commodity_id>')
def get_commodity_detail(commodity_id):
    # use spark
    '''
    #return "hello"+commodity_id
    spark = SparkSession\
            .builder\
            .appName('readCommodity')\
            .master("spark://")\
            .getOrCreate()
    # maybe try local

    # specify the uri, db and collection to read
    pipeline = "{'$match':{'commodity_id','"+str(commodity_id)+"'}}"
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option('uri','mongodb://IP_ADDR/recommendation.commodity')\
            .option('pipeline',pipeline)\
            .load()
    return df.toJSON()
    # pass
    '''
    # use pymongo
    client = MongoClient('localhost',27017)
    collection = client.recommendation.itemdata
    result = collection.find_one({"commodity_id":commodity_id})
    res = dumps(result)
    return res

@application.route('/api/cart/<int:user_id>', methods=["GET","PUT"])
def cart_info(user_id):
    client = MongoClient('localhost',27017)
    collection = client.recommendation.cart
    if request.method=='GET':
        get_cart = collection.find({"user_id":user_id})
        return dumps(get_cart)
    else:
        patch = request.get_json()
        collection.update({"user_id":user_id},{"$set":{"cart":patch["cart"]}})
        return ('',200)
# @application.route('/api/user',methods=["POST"])
# @application.route('/api/user/<user_id>',methods=["GET","PUT"])
if __name__ == "__main__":
    application.run(host='127.0.0.1')
