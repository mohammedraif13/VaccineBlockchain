from Constants import connString
import pyodbc
import datetime
import uuid
import time
import Constants    
from Constants import contract_address
from web3 import Web3, HTTPProvider
import json
import pprint
        
class PackingReviewerModel:
    def __init__(self, packingReviewerID = '',packingReviewerName = '',isActive = False):
        self.packingReviewerID = packingReviewerID
        self.packingReviewerName = packingReviewerName
        self.isActive = isActive
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM PackingReviewer ORDER BY packingReviewerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = PackingReviewerModel(dbrow[0],dbrow[1],dbrow[2])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT packingReviewerID, packingReviewerName FROM PackingReviewer  WHERE isActive = 1  ORDER BY packingReviewerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = PackingReviewerModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM PackingReviewer WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = PackingReviewerModel(dbrow[0],dbrow[1],dbrow[2])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.packingReviewerID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO PackingReviewer (packingReviewerID,packingReviewerName,isActive) VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (obj.packingReviewerID,obj.packingReviewerName,obj.isActive))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/PackingReviewerContract.json'
        deployed_contract_address = Constants.packing_reviewer_contract
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.packingReviewerID, obj.packingReviewerName, bool(obj.isActive)).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE PackingReviewer SET packingReviewerName = ?,isActive = ? WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1,  (obj.packingReviewerName,obj.isActive,obj.packingReviewerID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM PackingReviewer WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

