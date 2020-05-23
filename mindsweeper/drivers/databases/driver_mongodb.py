import pymongo


class MongoDB:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['mindsweeper']

    def count(self, collection, query):
        return self.db[collection].count_documents(query)

    def exists(self, collection, query):
        return self.count(collection, query) > 0

    def exists_by_id(self, collection, id_num):
        query = {'_id': id_num}
        return self.exists(collection, query)

    def upsert_user(self, msg):
        user = {
            '_id': msg['userId'],
            'datetime': msg['datetime'],
            'username': msg['data']['username'],
            'birthday': msg['data']['birthday'],
            'gender': msg['data']['gender'],
        }
        query = {'_id': msg['userId']}
        values = {'$set': user}
        self.db['users'].update_one(query, values, upsert=True)

    def upsert_sweep(self, msg):
        sweep_id = f"sw{msg['userId']}{msg['datetime']}"
        sweep = {
            '_id': sweep_id,
            'userId': msg['userId'],
            'datetime': msg['datetime'],
            'sweepStart': msg['data']['sweepStart'],
            'sweepEnd': msg['data']['sweepEnd'],
            'numOfSnapshots': msg['data']['numOfSnapshots']
        }
        query = {'_id': sweep_id}
        values = {'$set': sweep}
        self.db['sweeps'].update_one(query, values, upsert=True)

    def upsert_snapshot(self, msg):
        snapshot_id = f"ss{msg['userId']}{msg['datetime']}"
        snapshot = {
            '_id': snapshot_id,
            'userId': msg['userId'],
            'datetime': msg['datetime'],
            'format': msg['data']['format']
        }
        query = {'_id': snapshot_id}
        values = {'$set': snapshot}
        self.db['snapshots'].update_one(query, values, upsert=True)

    def upsert_result(self, msg):
        snapshot_id = f"ss{msg['userId']}{msg['datetime']}"
        self.upsert_snapshot(msg)
        query = {'_id': snapshot_id}
        del msg['data']['format']
        values = {'$set': {f"results.{msg['type']}": msg['data']}}
        self.db['snapshots'].update_one(query, values, upsert=True)

    def find(self, collection, query, projection=None):
        return self.db[collection].find(query, projection)

    def find_one(self, collection, query, projection=None):
        return self.db[collection].find_one(query, projection)
