from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDBConnector:
    def __init__(self, connection_string: str):
        self.db = None
        try:
            self.client = MongoClient(connection_string)
            # Optional: Trigger connection test
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB")
        except ConnectionFailure as e:
            print(f"❌ Connection failed: {e}")
            raise

    def load_database(self, database_name: str):
        self.db = self.client[database_name]

    def list_collections(self):
        return self.db.list_collection_names()

    def get_collection_schema_sample(self, collection_name, limit=5):
        collection = self.db[collection_name]
        return list(collection.find().limit(limit))

    def get_database_names(self):
        return self.client.list_database_names()

    def get_collection_stats(self, collection_name):
        return self.db.command("collstats", collection_name)

    def get_server_info(self):
        return self.client.server_info()

    def close_connection(self):
        self.client.close()
        print("🔌 MongoDB connection closed")


# if __name__ == "__main__":
#     from os import getenv
#     user = getenv('DB_USER')
#     password = getenv('DB_PASSWORD')
#
#     conn = MongoDBConnector(user, password)
#
#     print("📦 Databases:", conn.get_database_names())
#     conn.load_database('sample_mflix')
#
#     collections = conn.list_collections()
#
#     print("📂 Collections:", collections)
#
#     for col in collections:
#         print(f"\n🔍 Sample docs from '{col}':")
#         for doc in conn.get_collection_schema_sample(col, limit=2):
#             print(doc)

    # client = MongoClient(conn_str)
    #
    # # Ping to confirm connection
    # client.admin.command("ping")
    # print("✅ Connected!")
    #
    # # List all databases
    # db_names = client.list_database_names()
    # print("📦 Databases available in your cluster:")
    # for db in db_names:
    #     print("-", db)

    # db_name = "your_database"
    #
    # mongo = MongoDBConnector(conn_str, db_name)
    #
    # print("📦 Databases:", mongo.get_database_names())
    # print("📂 Collections:", mongo.list_collections())
    # print("📝 Sample Docs from 'your_collection':", mongo.get_collection_schema_sample("your_collection"))
    # print("📊 Stats:", mongo.get_collection_stats("your_collection"))
    # print("🖥️ Server Info:", mongo.get_server_info())
    #
    # mongo.close_connection()
