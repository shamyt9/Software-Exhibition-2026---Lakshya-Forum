from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["aicmdss"]   # This is your database name

# All your collections
users_col        = db["users"]
complaints_col   = db["complaints"]
transactions_col = db["transactions"]
predictions_col  = db["ai_predictions"]
risks_col        = db["risk_assessments"]
firs_col         = db["firs"]
freezes_col      = db["bank_freezes"]
logs_col         = db["audit_logs"]

print("MongoDB connected successfully!")