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

@application.route('/api/bestseller')
def get_bestseller():
    start = request.args.get("start")
    limit = request.args.get("limit")
    
    # using spark session
    spark = SparkSession\
            .builder\
            .appName('getBestSeller')\
            .master("local")\
            .getOrCreate()
    pipeline = "{'$match':{'salesRank.Electronic','$gt: "+str(start)+", $lt: "+str(start+limit)+"'}}"
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option('uri','mongodb://127.0.0.1/recommendation.commodity')\
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
    '''
    
@application.route('/api/behavior', methods=["POST"])
def post_behavior():
    actions = request.get_json()
    infer_obj = Inference(actions)
    item_list = infer_obj.inference(actions)
    spark = SparkSession\
            .builder\
            .appName('writeBehavior')\
            .master('local')\
            .getOrCreate()
    sc = SparkContext()
    data = spark.read.json(sc.parallelize(actions))
    data.write.format('com.mongodb.spark.sql.DefaultSource').mode('append').save()
    return json.dumps({"recommendation":str(item_list)})

@application.route('/api/commodity/<int:commodity_id>')
def get_commodity_detail(commodity_id):
    # use spark
    spark = SparkSession\
            .builder\
            .appName('readCommodity')\
            .master("local")\
            .getOrCreate()
    pipeline = "{'$match':{'commodity_id','"+str(commodity_id)+"'}}"
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
            .option('uri','mongodb://127.0.0.1/recommendation.commodity')\
            .option('pipeline',pipeline)\
            .load()
    return df.toJSON()
    '''
    # use pymongo
    client = MongoClient('localhost',27017)
    collection = client.recommendation.itemdata
    result = collection.find_one({"commodity_id":commodity_id})
    res = dumps(result)
    return res
    '''

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

@application.route('/api/commodity', methods=["POST"])
def create_commodity():
    commodity = request.get_json()
    client = MongoClient('localhost',27017)
    collection = client.recommendation.itemdata
    collection.insertOne(commodity)
    return ('',200)
@application.route('/api/commodity/<int:commodity_id>',methods=["PUT","DELETE"])
def update_delete_item(commodity_id):
    client = MongoClient('localhost',27017)
    collection = client.recommendation.itemdata
    if request.method=='PUT':
        collection.updateOne({"commodity_id":commodity_id},request.get_json)
        return ('',200)
    else:
        collection.deleteOne({"commodity_id":commodity_id})
        return ('',200)

@application.route('/api/user',methods=["POST"])
def create_user():
    client = MongoClient('localhost',27017)
    collection = client.recommendation.user
    collection.insertOne(request.get_json())
    return ('',200)
@application.route('/api/user/<user_id>',methods=["GET","PUT","DELETE"])
def manipulate_user(user_id):
    client = MongoClient('localhost',27017)
    collection = client.recommendation.user
    if request.method=='GET':
        return dumps(collection.findOne({"user_id":user_id}))
    elif request.method=='PUT':
        user_info = request.get_json()
        collection.updateOne({"user_id":user_id},user_info)
        return ('',200)
    else:
        collection.deleteOne({"user_id":user_id})
        return ('',200)
if __name__ == "__main__":
    application.run(host='127.0.0.1')
