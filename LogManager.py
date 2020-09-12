from config import mongoClient
SearchDB = mongoClient['SearchDB']

# Log Manager Class and Methods used to save and fetch User Search History
class LogManager:
    
    collection = None 
    document = None 
    
    def __init__(self,collection,document=None):
        self.document = document
        if self.collection == "" or self.collection is None:
            self.collection = SearchDB[collection]
        else:
            raise AttributeError("'collection' cannot be empty or None.")
    
    # Save Search History 
    def save(self):
        # Document to be saved here
        if self.document is not None:
            res = self.collection.insert_one(self.document)
            return res
        else:
            raise AttributeError("'None' cannot be created in mongo .")
    
    
    # Fetch last 5 searches from MongoDB having given keyword for author
    def get_recent(self,keyword,author):
        print(keyword)
        keyword = ".*{}.*".format(keyword)
        query = {
            "search": {
                "$regex": keyword,
                "$options" :'i'
                },
            "author": author 
        }
        documents = self.collection.find(
            query
            
        ).sort([("timestamp", -1)]).limit(5)
        return documents
        
        
        
        
