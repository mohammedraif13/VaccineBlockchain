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
        
class PackingModel:
    def __init__(self, packingID = '',productionBatchNo = '',packingBatchNo = '',packingDateTime = None,packingForm = '',packingMaterials = '',packingEquipment = '',abnormalRecord = '',inspectionReport = '',investigationReport = '',actualWeight = 0,packingInchargeID = '',packingReviewerID = '',packingInchargeModel = None,packingReviewerModel = None):
        self.packingID = packingID
        self.productionBatchNo = productionBatchNo
        self.packingBatchNo = packingBatchNo
        self.packingDateTime = packingDateTime
        self.packingForm = packingForm
        self.packingMaterials = packingMaterials
        self.packingEquipment = packingEquipment
        self.abnormalRecord = abnormalRecord
        self.inspectionReport = inspectionReport
        self.investigationReport = investigationReport
        self.actualWeight = actualWeight
        self.packingInchargeID = packingInchargeID
        self.packingReviewerID = packingReviewerID
        self.packingInchargeModel = packingInchargeModel
        self.packingReviewerModel = packingReviewerModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Packing ORDER BY productionBatchNo"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = PackingModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT packingID, vaccineRecipientName FROM Packing  ORDER BY vaccineRecipientName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = PackingModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Packing WHERE packingID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = PackingModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.packingID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Packing (packingID,productionBatchNo,packingBatchNo,packingDateTime,packingForm,packingMaterials,packingEquipment,abnormalRecord,inspectionReport,investigationReport,actualWeight,packingInchargeID,packingReviewerID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.packingID,obj.productionBatchNo,obj.packingBatchNo,datetime.datetime.strptime(obj.packingDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.packingForm,obj.packingMaterials,obj.packingEquipment,obj.abnormalRecord,obj.inspectionReport,obj.investigationReport,obj.actualWeight,obj.packingInchargeID,obj.packingReviewerID))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/PackingContract.json'
        deployed_contract_address = Constants.packing_contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.packingID, obj.productionBatchNo, obj.packingBatchNo, obj.packingInchargeID, obj.packingReviewerID).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Packing SET productionBatchNo = ?,packingBatchNo = ?,packingDateTime = ?,packingForm = ?,packingMaterials = ?,packingEquipment = ?,abnormalRecord = ?,inspectionReport = ?,investigationReport = ?,actualWeight = ?,packingInchargeID = ?,packingReviewerID = ? WHERE packingID = ?"
        cursor.execute(sqlcmd1,  (obj.productionBatchNo,obj.packingBatchNo,datetime.datetime.strptime(obj.packingDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.packingForm,obj.packingMaterials,obj.packingEquipment,obj.abnormalRecord,obj.inspectionReport,obj.investigationReport,obj.actualWeight,obj.packingInchargeID,obj.packingReviewerID,obj.packingID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Packing WHERE packingID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

