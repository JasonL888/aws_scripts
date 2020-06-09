#!/Users/jasonlau/anaconda/bin/python
import boto3
import time
import threading
import json
import sys

debug=False

class readThread(threading.Thread):
    def __init__(self, threadID, name, client, streamName, shardId, delay=30):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client = client
        self.streamName = streamName
        self.shardId = shardId
        self.delay = delay

    def run(self):
        print("%s:readShard:%s\n" % (self.name,self.shardId))
        shardIteratorJson = self.client.get_shard_iterator(StreamName=self.streamName,ShardId=self.shardId,ShardIteratorType='LATEST')
        if debug:
            print("%s:shardIterator:%s\n" % (self.name,shardIteratorJson))
        shardIterator = shardIteratorJson['ShardIterator']
        while shardIterator != "null":
            rec = self.client.get_records(ShardIterator=shardIterator)
            if debug:
                print("%s:rec:%s\n" % (self.name,rec))
            if (len(rec['Records']) > 0):
                data = rec['Records'][0]['Data']
                if debug:
                    print("%s:data:%s\n" % (self.name,data))
                json_data_str = json.loads(data)
                json_data_obj = json.loads(json_data_str)
                print("%s:mac:%s serial:%s ip:%s" % (self.name, json_data_obj["device"]["macAddress"], json_data_obj["device"]["serialNumber"], json_data_obj["device"]["extIpAddress"]))

                seqno = rec['Records'][0]['SequenceNumber']
                print("%s:seqno:%s" % (self.name, seqno))


                arrtime = rec['Records'][0]['ApproximateArrivalTimestamp']
                print("%s:approx_arrival:%s" % (self.name, arrtime))

                print("%s:json:%s\n" % (self.name, json_data_obj))
            else:
                print("%s:no data\n" % self.name)
            shardIterator = rec['NextShardIterator']
            time.sleep(self.delay)


def connectKinesis(client):
    streams = client.list_streams()
    print("streams:%s\n" % streams)
    streamName = streams['StreamNames'][0]
    print("streamName:%s\n" % streamName)
    shards = client.list_shards(StreamName=streamName)
    if debug:
        print("shards:%s" % shards)
        print("Num of shards:%d\n" % len(shards['Shards']))
    return(streamName, shards)


if __name__ == "__main__":
    env = 'prod'
    profileName = 'prod_profile'
    if len(sys.argv) == 2:
        env = str(sys.argv[1])
        if env == 'stage':
            profileName = 'stage_profile'
    print("profileName:%s" % profileName)
    session = boto3.Session(profile_name=profileName)
    client = session.client('kinesis')
    (streamName, shards) = connectKinesis(client)
    for i in range(len(shards['Shards'])):
        thread1 = readThread(0, "Thread-%d" % i, client, streamName, shards['Shards'][i]['ShardId'], 10)
        thread1.start()

    print("Exiting Main Thread")
