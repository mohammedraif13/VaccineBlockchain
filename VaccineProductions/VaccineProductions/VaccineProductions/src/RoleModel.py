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
        
class RoleModel:
    def __init__(self, roleID = 0,roleName = '',canRole = False,canUsers = False,canInoculation = False,canInspection = False,canInspectionInCharge = False,canInspectionReviewer = False,canPacking = False,canPackingInCharge = False,canPackingReviewer = False,canProduction = False,canProductionInCharge = False,canProductionReviewer = False):
        self.roleID = roleID
        self.roleName = roleName
        self.canRole = canRole
        self.canUsers = canUsers
        self.canInoculation = canInoculation
        self.canInspection = canInspection
        self.canInspectionInCharge = canInspectionInCharge
        self.canInspectionReviewer = canInspectionReviewer
        self.canPacking = canPacking
        self.canPackingInCharge = canPackingInCharge
        self.canPackingReviewer = canPackingReviewer
        self.canProduction = canProduction
        self.canProductionInCharge = canProductionInCharge
        self.canProductionReviewer = canProductionReviewer
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Role ORDER BY roleName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RoleModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT roleID, roleName FROM Role  ORDER BY roleName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = RoleModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Role WHERE roleID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = RoleModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.roleID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Role (roleName,canRole,canUsers,canInoculation,canInspection,canInspectionInCharge,canInspectionReviewer,canPacking,canPackingInCharge,canPackingReviewer,canProduction,canProductionInCharge,canProductionReviewer) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.roleName,obj.canRole,obj.canUsers,obj.canInoculation,obj.canInspection,obj.canInspectionInCharge,obj.canInspectionReviewer,obj.canPacking,obj.canPackingInCharge,obj.canPackingReviewer,obj.canProduction,obj.canProductionInCharge,obj.canProductionReviewer))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/RoleContract.json'
        deployed_contract_address = Constants.role_contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        print(obj.roleID, obj.roleName, bool(obj.canRole), bool(obj.canUsers),bool(obj.canInoculation),bool(obj.canInspection),bool(obj.canPacking),bool(obj.canProduction))
        tx_hash = contract.functions.perform_transactions(1, obj.roleName, bool(obj.canRole), bool(obj.canUsers),bool(obj.canInoculation),bool(obj.canInspection),bool(obj.canPacking),bool(obj.canProduction)).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Role SET roleName = ?,canRole = ?,canUsers = ?,canInoculation = ?,canInspection = ?,canInspectionInCharge = ?,canInspectionReviewer = ?,canPacking = ?,canPackingInCharge = ?,canPackingReviewer = ?,canProduction = ?,canProductionInCharge = ?,canProductionReviewer = ? WHERE roleID = ?"
        cursor.execute(sqlcmd1,  (obj.roleName,obj.canRole,obj.canUsers,obj.canInoculation,obj.canInspection,obj.canInspectionInCharge,obj.canInspectionReviewer,obj.canPacking,obj.canPackingInCharge,obj.canPackingReviewer,obj.canProduction,obj.canProductionInCharge,obj.canProductionReviewer,obj.roleID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Role WHERE roleID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

