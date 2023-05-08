import pickle

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
        
class InoculationModel:
    def __init__(self, inoculationID = '',productionBatchNo = '',vaccineRecipientName = '',inoculationDateTime = None,vaccineRecipientAadharNo = '',vaccineRecipientAddress = '',vaccineRecipientCity = '',vaccineRecipientState = '',vaccineRecipientPincode = '',vaccineRecipientCountry = '',vaccineRecipientDob = None,inoculationDose = '',inoculationDepartment = '',inoculationDoctorName = '',inoculationDoctorNumber = '',isBlockChainGenerated = False,prevHash = '',hash = '',sequenceNumber = 0):
        self.inoculationID = inoculationID
        self.productionBatchNo = productionBatchNo
        self.vaccineRecipientName = vaccineRecipientName
        self.inoculationDateTime = inoculationDateTime
        self.vaccineRecipientAadharNo = vaccineRecipientAadharNo
        self.vaccineRecipientAddress = vaccineRecipientAddress
        self.vaccineRecipientCity = vaccineRecipientCity
        self.vaccineRecipientState = vaccineRecipientState
        self.vaccineRecipientPincode = vaccineRecipientPincode
        self.vaccineRecipientCountry = vaccineRecipientCountry
        self.vaccineRecipientDob = vaccineRecipientDob
        self.inoculationDose = inoculationDose
        self.inoculationDepartment = inoculationDepartment
        self.inoculationDoctorName = inoculationDoctorName
        self.inoculationDoctorNumber = inoculationDoctorNumber
        self.isBlockChainGenerated = isBlockChainGenerated
        self.prevHash = prevHash
        self.hash = hash
        self.sequenceNumber = sequenceNumber
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Inoculation ORDER BY inoculationDoctorName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InoculationModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT inoculationID, inoculationDoctorName FROM Inoculation  ORDER BY inoculationDoctorName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = InoculationModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Inoculation WHERE inoculationID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = InoculationModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18])
        cursor.close()
        conn.close()
        return record

    @staticmethod
    def proof_of_voting(obj, start=10, end=100):
        tx_dictionary = {}
        w3 = Web3(HTTPProvider('http://localhost:7545'))

        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/InoculationContract.json'
        deployed_contract_address = contract_address

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]

        if start == end:
            for x in range(start, end):
                block = w3.eth.getBlock(x, True)
                for transaction in block.transactions:
                    if transaction['to'] == contract_address or transaction['from'] == contract_address:
                        with open("transactions.pkl", "wb") as f:
                            hashStr = transaction['hash'].hex()
                            tx_dictionary[hashStr] = transaction
                            pickle.dump(tx_dictionary, f)
                        f.close()
                pending_transactions = w3.provider.make_request("parity_pendingTransactions", [])
                gas_prices = []
                gases = []
                for tx in pending_transactions["result"[:10]]:
                    gas_prices.append(int((tx["gasPrice"]), 16))
                    gases.append(int((tx["gas"]), 16))

        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        accounts = w3.eth.accounts

        secx = int(datetime.datetime.strptime(obj.inoculationDateTime, '%Y-%m-%dT%H:%M').timestamp())
        print(obj.inoculationDateTime)
        dob = int(datetime.datetime.strptime(obj.inoculationDateTime, '%Y-%m-%dT%H:%M').timestamp())
        tx_hash = contract.functions.perform_transactions(obj.inoculationID, obj.productionBatchNo,
                                                          obj.vaccineRecipientName, obj.inoculationDose,
                                                          obj.inoculationDepartment, obj.inoculationDoctorName,
                                                          obj.inoculationDoctorNumber).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    @staticmethod
    def insert(obj):
        obj.inoculationID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Inoculation (inoculationID,productionBatchNo,vaccineRecipientName,inoculationDateTime,vaccineRecipientAadharNo,vaccineRecipientAddress,vaccineRecipientCity,vaccineRecipientState,vaccineRecipientPincode,vaccineRecipientCountry,vaccineRecipientDob,inoculationDose,inoculationDepartment,inoculationDoctorName,inoculationDoctorNumber,isBlockChainGenerated,prevHash,hash) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.inoculationID,obj.productionBatchNo,obj.vaccineRecipientName,datetime.datetime.strptime(obj.inoculationDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.vaccineRecipientAadharNo,obj.vaccineRecipientAddress,obj.vaccineRecipientCity,obj.vaccineRecipientState,obj.vaccineRecipientPincode,obj.vaccineRecipientCountry,datetime.datetime.strptime(obj.vaccineRecipientDob.replace('T', ' '), '%Y-%m-%d'),obj.inoculationDose,obj.inoculationDepartment,obj.inoculationDoctorName,obj.inoculationDoctorNumber,obj.isBlockChainGenerated,obj.prevHash,obj.hash))
        cursor.close()
        conn.close()
        InoculationModel.proof_of_voting(obj)


        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Inoculation SET productionBatchNo = ?,vaccineRecipientName = ?,inoculationDateTime = ?,vaccineRecipientAadharNo = ?,vaccineRecipientAddress = ?,vaccineRecipientCity = ?,vaccineRecipientState = ?,vaccineRecipientPincode = ?,vaccineRecipientCountry = ?,vaccineRecipientDob = ?,inoculationDose = ?,inoculationDepartment = ?,inoculationDoctorName = ?,inoculationDoctorNumber = ?,isBlockChainGenerated = ?,prevHash = ?,hash = ? WHERE inoculationID = ?"
        cursor.execute(sqlcmd1,  (obj.productionBatchNo,obj.vaccineRecipientName,datetime.datetime.strptime(obj.inoculationDateTime.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.vaccineRecipientAadharNo,obj.vaccineRecipientAddress,obj.vaccineRecipientCity,obj.vaccineRecipientState,obj.vaccineRecipientPincode,obj.vaccineRecipientCountry,datetime.datetime.strptime(obj.vaccineRecipientDob.replace('T', ' '), '%Y-%m-%d'),obj.inoculationDose,obj.inoculationDepartment,obj.inoculationDoctorName,obj.inoculationDoctorNumber,obj.isBlockChainGenerated,obj.prevHash,obj.hash,obj.inoculationID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Inoculation WHERE inoculationID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

