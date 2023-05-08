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

class InspectionInChargeModel:
    def __init__(self, inspectionInChargeID = '',inspectionInChargeName = '',isActive = False):
        self.inspectionInChargeID = inspectionInChargeID
        self.inspectionInChargeName = inspectionInChargeName
        self.isActive = isActive



    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InspectionInCharge ORDER BY inspectionInChargeName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InspectionInChargeModel(dbrow[0],dbrow[1],dbrow[2])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT inspectionInChargeID, inspectionInChargeName FROM InspectionInCharge  WHERE isActive = 1  ORDER BY inspectionInChargeName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InspectionInChargeModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InspectionInCharge WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = InspectionInChargeModel(dbrow[0],dbrow[1],dbrow[2])
        cursor.close()
        conn.close()
        return record

    @staticmethod
    def insert(obj):
        obj.inspectionInChargeID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO InspectionInCharge (inspectionInChargeID,inspectionInChargeName,isActive) VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (obj.inspectionInChargeID,obj.inspectionInChargeName,obj.isActive))
        cursor.close()
        conn.close()


        w3 = Web3(HTTPProvider('http://localhost:7545'))


        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/InspectionInChargeContract.json'
        deployed_contract_address = Constants.inspection_in_charge_contract

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]

        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        accounts = w3.eth.accounts


        tx_hash = contract.functions.perform_transactions(obj.inspectionInChargeID, obj.inspectionInChargeName, bool(obj.isActive)).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE InspectionInCharge SET inspectionInChargeName = ?,isActive = ? WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1,  (obj.inspectionInChargeName,obj.isActive,obj.inspectionInChargeID))
        cursor.close()
        conn.close()

    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM InspectionInCharge WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

