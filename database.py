import pymongo
class Database:
    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb://localhost:27016/")
        self.db = self.conn["lotery"]
        
    def insert_result(self,result):
        print('within insert_result-2')
        results = self.db.results_t
        result_id = results.insert_one(result).inserted_id
        print("Inserted: ",result_id)