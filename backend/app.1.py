from flask import Flask, request, Response
#from pyspark.sql import SparkSession
#from pyspark import SparkContext
from pymongo import MongoClient
import json
from bson.json_util import dumps

import numpy as np
import random
import pickle
import tensorflow as tf
from input import DataInputTest, DataInput
from model import Model
from collections import OrderedDict

# Init global variables
tf.app.flags.DEFINE_integer('hidden_units', 128, 'Number of hidden units in each layer')
tf.app.flags.DEFINE_integer('num_blocks', 1, 'Number of blocks in each attention')
tf.app.flags.DEFINE_integer('num_heads', 8, 'Number of heads in each attention')
tf.app.flags.DEFINE_float('dropout', 0.0, 'Dropout probability(0.0: no dropout)')
tf.app.flags.DEFINE_float('regulation_rate', 0.00005, 'L2 regulation rate')

tf.app.flags.DEFINE_integer('itemid_embedding_size', 64, 'Item id embedding size')
tf.app.flags.DEFINE_integer('cateid_embedding_size', 64, 'Cate id embedding size')

tf.app.flags.DEFINE_boolean('concat_time_emb', True, 'Concat time-embedding instead of Add')

# Training parameters
tf.app.flags.DEFINE_boolean('from_scratch', True, 'Romove model_dir, and train from scratch, default: False')
tf.app.flags.DEFINE_string('model_dir', 'save_path', 'Path to save model checkpoints')
tf.app.flags.DEFINE_string('optimizer', 'sgd', 'Optimizer for training: (adadelta, adam, rmsprop,sgd*)')
tf.app.flags.DEFINE_float('learning_rate', 1.0, 'Learning rate')
tf.app.flags.DEFINE_float('max_gradient_norm', 5.0, 'Clip gradients to this norm')

tf.app.flags.DEFINE_integer('train_batch_size', 32, 'Training Batch size')
tf.app.flags.DEFINE_integer('test_batch_size', 128, 'Testing Batch size')
tf.app.flags.DEFINE_integer('max_epochs', 10, 'Maximum # of training epochs')

tf.app.flags.DEFINE_integer('display_freq', 100, 'Display training status every this iteration')
tf.app.flags.DEFINE_integer('eval_freq', 1000, 'Display training status every this iteration')

# Runtime parameters
tf.app.flags.DEFINE_string('cuda_visible_devices', '0', 'Choice which GPU to use')
tf.app.flags.DEFINE_float('per_process_gpu_memory_fraction', 0.0, 'Gpu memory use fraction, 0.0 for allow_growth=True')

FLAGS = tf.app.flags.FLAGS
config = OrderedDict(sorted(FLAGS.__flags.items()))


for k, v in config.items():
    config[k] = v.value
config['user_count'] = 192403
config['item_count'] = 63001
config['cate_count'] = 801
class Inference(object):

    def __init__(self, data):
        self.data = data

        with open('cate_list.pkl', 'rb') as f:
            self.cate_list = pickle.load(f)

        random.seed(1234)
        np.random.seed(1234)
        tf.set_random_seed(1234)


    def proc_time_emb(self, hist_t, cur_t):
        gap = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096])
        hist_t = [cur_t - i + 1 for i in hist_t]
        hist_t = [np.sum(i >= gap) for i in hist_t]
        return hist_t

    def convert_data(self, data):
        reviewerID = data[0]['reviewerID']
        pos_list = []
        tim_list = []
        result = []

        for i in range(len(data)):
            tim_list.append(data[i]['unixReviewTime'] // 3600 // 24)
            pos_list.append(data[i]['asin'])

        hist_i = pos_list[:-1]
        hist_t = self.proc_time_emb(tim_list[:-1], tim_list[-2])

        for i in range(config['item_count']):
            result.append((reviewerID, hist_i, hist_t, i, 1))

        return result

    def inference(self, data):
        converted_data = self.convert_data(data)
        with tf.Session() as sess:
            meta_path = './save_path/atrank-815240.meta'
            saver = tf.train.import_meta_graph(meta_path)
            saver.restore(sess, "./save_path/atrank-815240")
            print('model restored')

            # whether it's training or not
            # is_training = tf.placeholder(tf.bool, [])
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            datainput = DataInput(converted_data, config['item_count'])
            max_asin = []
            modelobj = Model(config,self.cate_list)
            for _, uij in datainput:
                logit = modelobj.inference(sess,uij)
        # top 10 asin IDs
                for i in range(10):
                    max_asin.append(np.argmax(logit))
                    logit[max_asin[i]] = -1

            return max_asin

application = Flask(__name__)
#application.config["APPLICATION_ROOT"]="/flask"
@application.route('/')
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
    # need to know the type of var 'actions'
    print(actions)
    rec_class = Inference(actions)
    # modelobj = Model(config,rec_class.cate_list)
    rec = rec_class.inference(actions)
    return rec
    # pass
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


# @application.route('/api/user',methods=["POST"])
# @application.route('/api/user/<user_id>',methods=["GET","PUT"])
# @application.route('/api/cart/<user_id>',methods=["GET","DELETE"])
if __name__ == "__main__":
    application.run(host='127.0.0.1')
