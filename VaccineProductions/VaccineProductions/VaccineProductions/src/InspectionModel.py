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
        
class InspectionModel:
    def __init__(self, inspectionID = '',productionBatchNo = '',dosageForm = '',inspectionDateTime = None,specification = '',inspectionStandards = '',inspectionEquipments = '',inspectionObservations = '',inspectionCalculations = '',inspectionResults = '',inspectionInChargeID = '',inspectionReviewerID = '',inspectionInChargeModel = None,inspectionReviewerModel = None):
        self.inspectionID = inspectionID
        self.productionBatchNo = productionBatchNo
        self.dosageForm = dosageForm
        self.inspectionDateTime = inspectionDateTime
        self.specification = specification
        self.inspectionStandards = inspectionStandards
        self.inspectionEquipments = inspectionEquipments
        self.inspectionObservations = inspectionObservations
        self.inspectionCalculations = inspectionCalculations
        self.inspectionResults = inspectionResults
        self.inspectionInChargeID = inspectionInChargeID
        self.inspectionReviewerID = inspectionReviewerID
        self.inspectionInChargeModel = inspectionInChargeModel
        self.inspectionReviewerModel = inspectionReviewerModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Inspection ORDER BY productionBatchNo"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InspectionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT inspectionID, productionBatchNo FROM Inspection  ORDER BY productionBatchNo"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InspectionModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Inspection WHERE inspectionID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = InspectionModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
        cursor.close()
        conn.close()
        return record


    @staticmethod
    def insert(obj):
        obj.inspectionID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Inspection (inspectionID,productionBatchNo,dosageForm,inspectionDateTime,specification,inspectionStandards,inspectionEquipments,inspectionObservations,inspectionCalculations,inspectionResults,inspectionInChargeID,inspectionReviewerID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.inspectionID,obj.productionBatchNo,obj.dosageForm,datetime.datetime.strptime(obj.inspectionDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.specification,obj.inspectionStandards,obj.inspectionEquipments,obj.inspectionObservations,obj.inspectionCalculations,obj.inspectionResults,obj.inspectionInChargeID,obj.inspectionReviewerID))
        cursor.close()
        conn.close()


        w3 = Web3(HTTPProvider('http://localhost:7545'))


        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/InspectionContract.json'
        deployed_contract_address = Constants.inspection_contract_address

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]

        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        accounts = w3.eth.accounts


        tx_hash = contract.functions.perform_transactions(obj.inspectionID, obj.productionBatchNo, obj.dosageForm, obj.inspectionInChargeID, obj.inspectionReviewerID).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Inspection SET productionBatchNo = ?,dosageForm = ?,inspectionDateTime = ?,specification = ?,inspectionStandards = ?,inspectionEquipments = ?,inspectionObservations = ?,inspectionCalculations = ?,inspectionResults = ?,inspectionInChargeID = ?,inspectionReviewerID = ? WHERE inspectionID = ?"
        cursor.execute(sqlcmd1,  (obj.productionBatchNo,obj.dosageForm,datetime.datetime.strptime(obj.inspectionDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.specification,obj.inspectionStandards,obj.inspectionEquipments,obj.inspectionObservations,obj.inspectionCalculations,obj.inspectionResults,obj.inspectionInChargeID,obj.inspectionReviewerID,obj.inspectionID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Inspection WHERE inspectionID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

