import twint
import sys
import json

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
         { "name": "id",        "type": "long" },
         { "name": "tweet",     "type": "string" },
         { "name": "datetime",  "type": "long" },
         { "name": "username",  "type": "string" },
         { "name": "user_id",   "type": "long" },
         { "name": "hashtags",  "type": {"type": "array", "items": "string"} }
   ]
}
"""

key_schema_str = """
{
   "namespace": "my.test",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

kafka_broker = 'broker:9092'
schema_registry = 'http://schema_registry:8081'

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)

producer = AvroProducer({
    'bootstrap.servers': kafka_broker,
    'schema.registry.url': schema_registry
    }, default_key_schema=key_schema, default_value_schema=value_schema)


module = sys.modules["twint.storage.write"]

def Json(obj, config):
    tweet = obj.__dict__
    print(tweet)
    producer.produce(topic='tweets10', value=tweet, key={"name": "Key"})
    producer.flush()

module.Json = Json

c = twint.Config()
c.Search = "neo4j OR \"graph database\" OR \"graph databases\" OR graphdb OR graphconnect OR @neoquestions OR @Neo4jDE OR @Neo4jFr OR neotechnology"
c.Store_json = True
c.Custom["user"] = ["id", "tweet", "user_id", "username", "hashtags", "mentions"]
c.User_full = True
c.Output = "tweets.json"
c.Since = "2019-05-20"
c.Hide_output = True

twint.run.Search(c)
