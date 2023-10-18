import pymongo
class Database:
    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb://localhost:27016/")
        self.db = self.conn["lotery"]
        
    def insert_result(self,result):
        results = self.db.results_t
        result_id = results.insert_one(result).inserted_id
        if result_id :
            return 'Successfully'
        else :
            return 'Failed'
        
    def find_results(self, id, name_lotery):
        c_results = self.db.results_t
        dict_query = {"lotery":name_lotery, "raffle_id":id}
        results = c_results.find_one(dict_query)
        return results