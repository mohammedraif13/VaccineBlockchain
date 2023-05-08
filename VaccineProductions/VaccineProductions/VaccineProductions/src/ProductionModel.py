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
        
class ProductionModel:
    def __init__(self, productionID = '',companyName = '',vaccineName = '',productionBatchNo = '',productionDateTime = None,rawMaterials = '',auxiliaryMaterials = '',productionEquipmentParameters = '',abnormalRecord = '',investigationReport = '',expiryDateTime = None,actualWeight = 0,productionInchargeID = '',productionReviewerID = '',productionInchargeModel = None,productionReviewerModel = None):
        self.productionID = productionID
        self.companyName = companyName
        self.vaccineName = vaccineName
        self.productionBatchNo = productionBatchNo
        self.productionDateTime = productionDateTime
        self.rawMaterials = rawMaterials
        self.auxiliaryMaterials = auxiliaryMaterials
        self.productionEquipmentParameters = productionEquipmentParameters
        self.abnormalRecord = abnormalRecord
        self.investigationReport = investigationReport
        self.expiryDateTime = expiryDateTime
        self.actualWeight = actualWeight
        self.productionInchargeID = productionInchargeID
        self.productionReviewerID = productionReviewerID
        self.productionInchargeModel = productionInchargeModel
        self.productionReviewerModel = productionReviewerModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Production ORDER BY vaccineName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT productionID, vaccineName FROM Production  ORDER BY vaccineName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = ProductionModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Production WHERE productionID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = ProductionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.productionID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Production (productionID,companyName,vaccineName,productionBatchNo,productionDateTime,rawMaterials,auxiliaryMaterials,productionEquipmentParameters,abnormalRecord,investigationReport,expiryDateTime,actualWeight,productionInchargeID,productionReviewerID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.productionID,obj.companyName,obj.vaccineName,obj.productionBatchNo,datetime.datetime.strptime(obj.productionDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.rawMaterials,obj.auxiliaryMaterials,obj.productionEquipmentParameters,obj.abnormalRecord,obj.investigationReport,datetime.datetime.strptime(obj.expiryDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.actualWeight,obj.productionInchargeID,obj.productionReviewerID))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/ProductionContract.json'
        deployed_contract_address = Constants.production_contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.productionID, obj.companyName, obj.vaccineName, obj.productionBatchNo, ).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Production SET companyName = ?,vaccineName = ?,productionBatchNo = ?,productionDateTime = ?,rawMaterials = ?,auxiliaryMaterials = ?,productionEquipmentParameters = ?,abnormalRecord = ?,investigationReport = ?,expiryDateTime = ?,actualWeight = ?,productionInchargeID = ?,productionReviewerID = ? WHERE productionID = ?"
        cursor.execute(sqlcmd1,  (obj.companyName,obj.vaccineName,obj.productionBatchNo,datetime.datetime.strptime(obj.productionDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.rawMaterials,obj.auxiliaryMaterials,obj.productionEquipmentParameters,obj.abnormalRecord,obj.investigationReport,datetime.datetime.strptime(obj.expiryDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.actualWeight,obj.productionInchargeID,obj.productionReviewerID,obj.productionID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Production WHERE productionID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

