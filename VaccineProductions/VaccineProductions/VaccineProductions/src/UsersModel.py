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

class UsersModel:
    def __init__(self, userID = 0,userName = '',emailid = '',password = '',contactNo = '',isActive = False,roleID = 0,roleModel = None):
        self.userID = userID
        self.userName = userName
        self.emailid = emailid
        self.password = password
        self.contactNo = contactNo
        self.isActive = isActive
        self.roleID = roleID
        self.roleModel = roleModel



    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Users ORDER BY userName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = UsersModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT userID, userName FROM Users  WHERE isActive = 1  ORDER BY userName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = UsersModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM Users WHERE userID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = UsersModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6])
        cursor.close()
        conn.close()
        return record

    @staticmethod
    def insert(obj):

        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO Users (userName,emailid,password,contactNo,isActive,roleID) VALUES(?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.userName,obj.emailid,obj.password,obj.contactNo,obj.isActive,obj.roleID))
        cursor.close()
        conn.close()


        w3 = Web3(HTTPProvider('http://localhost:7545'))


        compiled_contract_path = '../../../VaccineProductions-Truffle/build/contracts/UsersContract.json'
        deployed_contract_address = Constants.users_contract_address

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]

        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        accounts = w3.eth.accounts


        tx_hash = contract.functions.perform_transactions(1, obj.userName).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE Users SET userName = ?,emailid = ?,password = ?,contactNo = ?,isActive = ?,roleID = ? WHERE userID = ?"
        cursor.execute(sqlcmd1,  (obj.userName,obj.emailid,obj.password,obj.contactNo,obj.isActive,obj.roleID,obj.userID))
        cursor.close()
        conn.close()

    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM Users WHERE userID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

