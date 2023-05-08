
from flask import Flask, request, render_template, redirect, url_for
import os
import pyodbc
import uuid
import time
from datetime import datetime
from Constants import connString

from InoculationModel import InoculationModel
from InspectionModel import InspectionModel
from InspectionInChargeModel import InspectionInChargeModel
from InspectionReviewerModel import InspectionReviewerModel
from PackingModel import PackingModel
from PackingInChargeModel import PackingInChargeModel
from PackingReviewerModel import PackingReviewerModel
from ProductionModel import ProductionModel
from ProductionInChargeModel import ProductionInChargeModel
from ProductionReviewerModel import ProductionReviewerModel
from RoleModel import RoleModel
from UsersModel import UsersModel




app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""
role_object = None
message = ""
msgType = ""
uploaded_file_name = ""

def initialize():
    global message, msgType
    message = ""
    msgType = ""

def process_role(option_id):

    
    if option_id == 0:
        if role_object.canInoculation == False:
            return False
        
    if option_id == 1:
        if role_object.canInspection == False:
            return False
        
    if option_id == 2:
        if role_object.canInspectionInCharge == False:
            return False
        
    if option_id == 3:
        if role_object.canInspectionReviewer == False:
            return False
        
    if option_id == 4:
        if role_object.canPacking == False:
            return False
        
    if option_id == 5:
        if role_object.canPackingInCharge == False:
            return False
        
    if option_id == 6:
        if role_object.canPackingReviewer == False:
            return False
        
    if option_id == 7:
        if role_object.canProduction == False:
            return False
        
    if option_id == 8:
        if role_object.canProductionInCharge == False:
            return False
        
    if option_id == 9:
        if role_object.canProductionReviewer == False:
            return False
        
    if option_id == 10:
        if role_object.canRole == False:
            return False
        
    if option_id == 11:
        if role_object.canUsers == False:
            return False
        

    return True



@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")

@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid, role_object
    emailid = request.form["emailid"]
    password = request.form["password"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + password + "' AND isActive = 1";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template("Login.html", processResult="Invalid Credentials")
    user_id = row[0]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template("Login.html", processResult="Invalid Role")

    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7], row2[8], row2[9], row2[10], row2[11], row2[12], row2[13])

    return render_template("Dashboard.html")


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template("ChangePassword.html", msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template("ChangePassword.html", msg="New Password and Confirm Password are NOT same")

    conn2 = pyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE Users SET password = '" + newPassword + "' WHERE emailid = '" + emailid + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    return render_template("Dashboard.html")


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)


@app.route("/InoculationListing")
def Inoculation_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInoculation = process_role(0)

    if canInoculation == False:
        message = "You Don't Have Permission to Access Inoculation"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = InoculationModel.get_all()

    return render_template("InoculationListing.html", records=records)

@app.route("/InoculationOperation")
def Inoculation_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInoculation = process_role(0)

    if not canInoculation:
        message = "You Don't Have Permission to Access Inoculation"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = InoculationModel("", "")

    Inoculation = InoculationModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = InoculationModel.get_by_id(unique_id)

    return render_template("InoculationOperation.html", row=row, operation=operation, Inoculation=Inoculation, )

@app.route("/ProcessInoculationOperation", methods=["POST"])
def process_Inoculation_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canInoculation = process_role(0)
    if not canInoculation:
        message = "You Don't Have Permission to Access Inoculation"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = InoculationModel("", "")

    if operation != "Delete":
       obj.inoculationID = request.form['inoculationID']
       obj.productionBatchNo = request.form['productionBatchNo']
       obj.vaccineRecipientName = request.form['vaccineRecipientName']
       obj.inoculationDateTime = request.form['inoculationDateTime']
       obj.vaccineRecipientAadharNo = request.form['vaccineRecipientAadharNo']
       obj.vaccineRecipientAddress = request.form['vaccineRecipientAddress']
       obj.vaccineRecipientCity = request.form['vaccineRecipientCity']
       obj.vaccineRecipientState = request.form['vaccineRecipientState']
       obj.vaccineRecipientPincode = request.form['vaccineRecipientPincode']
       obj.vaccineRecipientCountry = request.form['vaccineRecipientCountry']
       obj.vaccineRecipientDob = request.form['vaccineRecipientDob']
       obj.inoculationDose = request.form['inoculationDose']
       obj.inoculationDepartment = request.form['inoculationDepartment']
       obj.inoculationDoctorName = request.form['inoculationDoctorName']
       obj.inoculationDoctorNumber = request.form['inoculationDoctorNumber']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.inoculationID = request.form["inoculationID"]
        obj.update(obj)

    if operation == "Delete":
        inoculationID = request.form["inoculationID"]
        obj.delete(inoculationID)


    return redirect(url_for("Inoculation_listing"))
                    
@app.route("/InspectionListing")
def Inspection_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspection = process_role(1)

    if canInspection == False:
        message = "You Don't Have Permission to Access Inspection"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = InspectionModel.get_all()

    return render_template("InspectionListing.html", records=records)

@app.route("/InspectionOperation")
def Inspection_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspection = process_role(1)

    if not canInspection:
        message = "You Don't Have Permission to Access Inspection"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = InspectionModel("", "")

    Inspection = InspectionModel.get_all()
    inspectionInCharge_list = InspectionInChargeModel.get_name_id()
    inspectionReviewer_list = InspectionReviewerModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = InspectionModel.get_by_id(unique_id)

    return render_template("InspectionOperation.html", row=row, operation=operation, Inspection=Inspection, inspectionInCharge_list = inspectionInCharge_list,inspectionReviewer_list = inspectionReviewer_list)

@app.route("/ProcessInspectionOperation", methods=["POST"])
def process_Inspection_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canInspection = process_role(1)
    if not canInspection:
        message = "You Don't Have Permission to Access Inspection"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = InspectionModel("", "")

    if operation != "Delete":
       obj.inspectionID = request.form['inspectionID']
       obj.productionBatchNo = request.form['productionBatchNo']
       obj.dosageForm = request.form['dosageForm']
       obj.inspectionDateTime = request.form['inspectionDateTime']
       obj.specification = request.form['specification']
       obj.inspectionStandards = request.form['inspectionStandards']
       obj.inspectionEquipments = request.form['inspectionEquipments']
       obj.inspectionObservations = request.form['inspectionObservations']
       obj.inspectionCalculations = request.form['inspectionCalculations']
       obj.inspectionResults = request.form['inspectionResults']
       obj.inspectionInChargeID = request.form['inspectionInChargeID']
       obj.inspectionReviewerID = request.form['inspectionReviewerID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.inspectionID = request.form["inspectionID"]
        obj.update(obj)

    if operation == "Delete":
        inspectionID = request.form["inspectionID"]
        obj.delete(inspectionID)


    return redirect(url_for("Inspection_listing"))
                    
@app.route("/InspectionInChargeListing")
def InspectionInCharge_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspectionInCharge = process_role(2)

    if canInspectionInCharge == False:
        message = "You Don't Have Permission to Access InspectionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = InspectionInChargeModel.get_all()

    return render_template("InspectionInChargeListing.html", records=records)

@app.route("/InspectionInChargeOperation")
def InspectionInCharge_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspectionInCharge = process_role(2)

    if not canInspectionInCharge:
        message = "You Don't Have Permission to Access InspectionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = InspectionInChargeModel("", "")

    InspectionInCharge = InspectionInChargeModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = InspectionInChargeModel.get_by_id(unique_id)

    return render_template("InspectionInChargeOperation.html", row=row, operation=operation, InspectionInCharge=InspectionInCharge, )

@app.route("/ProcessInspectionInChargeOperation", methods=["POST"])
def process_InspectionInCharge_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canInspectionInCharge = process_role(2)
    if not canInspectionInCharge:
        message = "You Don't Have Permission to Access InspectionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = InspectionInChargeModel("", "")

    if operation != "Delete":
       obj.inspectionInChargeID = request.form['inspectionInChargeID']
       obj.inspectionInChargeName = request.form['inspectionInChargeName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.inspectionInChargeID = request.form["inspectionInChargeID"]
        obj.update(obj)

    if operation == "Delete":
        inspectionInChargeID = request.form["inspectionInChargeID"]
        obj.delete(inspectionInChargeID)


    return redirect(url_for("InspectionInCharge_listing"))
                    
@app.route("/InspectionReviewerListing")
def InspectionReviewer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspectionReviewer = process_role(3)

    if canInspectionReviewer == False:
        message = "You Don't Have Permission to Access InspectionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = InspectionReviewerModel.get_all()

    return render_template("InspectionReviewerListing.html", records=records)

@app.route("/InspectionReviewerOperation")
def InspectionReviewer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canInspectionReviewer = process_role(3)

    if not canInspectionReviewer:
        message = "You Don't Have Permission to Access InspectionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = InspectionReviewerModel("", "")

    InspectionReviewer = InspectionReviewerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = InspectionReviewerModel.get_by_id(unique_id)

    return render_template("InspectionReviewerOperation.html", row=row, operation=operation, InspectionReviewer=InspectionReviewer, )

@app.route("/ProcessInspectionReviewerOperation", methods=["POST"])
def process_InspectionReviewer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canInspectionReviewer = process_role(3)
    if not canInspectionReviewer:
        message = "You Don't Have Permission to Access InspectionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = InspectionReviewerModel("", "")

    if operation != "Delete":
       obj.inspectionReviewerID = request.form['inspectionReviewerID']
       obj.inspectionReviewerName = request.form['inspectionReviewerName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.inspectionReviewerID = request.form["inspectionReviewerID"]
        obj.update(obj)

    if operation == "Delete":
        inspectionReviewerID = request.form["inspectionReviewerID"]
        obj.delete(inspectionReviewerID)


    return redirect(url_for("InspectionReviewer_listing"))
                    
@app.route("/PackingListing")
def Packing_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPacking = process_role(4)

    if canPacking == False:
        message = "You Don't Have Permission to Access Packing"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = PackingModel.get_all()

    return render_template("PackingListing.html", records=records)

@app.route("/PackingOperation")
def Packing_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPacking = process_role(4)

    if not canPacking:
        message = "You Don't Have Permission to Access Packing"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = PackingModel("", "")

    Packing = PackingModel.get_all()
    packingInCharge_list = PackingInChargeModel.get_name_id()
    packingReviewer_list = PackingReviewerModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = PackingModel.get_by_id(unique_id)

    return render_template("PackingOperation.html", row=row, operation=operation, Packing=Packing, packingInCharge_list = packingInCharge_list,packingReviewer_list = packingReviewer_list)

@app.route("/ProcessPackingOperation", methods=["POST"])
def process_Packing_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canPacking = process_role(4)
    if not canPacking:
        message = "You Don't Have Permission to Access Packing"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = PackingModel("", "")

    if operation != "Delete":
       obj.packingID = request.form['packingID']
       obj.productionBatchNo = request.form['productionBatchNo']
       obj.packingBatchNo = request.form['packingBatchNo']
       obj.packingDateTime = request.form['packingDateTime']
       obj.packingForm = request.form['packingForm']
       obj.packingMaterials = request.form['packingMaterials']
       obj.packingEquipment = request.form['packingEquipment']
       obj.abnormalRecord = request.form['abnormalRecord']
       obj.inspectionReport = request.form['inspectionReport']
       obj.investigationReport = request.form['investigationReport']
       obj.actualWeight = request.form['actualWeight']
       obj.packingInchargeID = request.form['packingInchargeID']
       obj.packingReviewerID = request.form['packingReviewerID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.packingID = request.form["packingID"]
        obj.update(obj)

    if operation == "Delete":
        packingID = request.form["packingID"]
        obj.delete(packingID)


    return redirect(url_for("Packing_listing"))
                    
@app.route("/PackingInChargeListing")
def PackingInCharge_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPackingInCharge = process_role(5)

    if canPackingInCharge == False:
        message = "You Don't Have Permission to Access PackingInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = PackingInChargeModel.get_all()

    return render_template("PackingInChargeListing.html", records=records)

@app.route("/PackingInChargeOperation")
def PackingInCharge_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPackingInCharge = process_role(5)

    if not canPackingInCharge:
        message = "You Don't Have Permission to Access PackingInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = PackingInChargeModel("", "")

    PackingInCharge = PackingInChargeModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = PackingInChargeModel.get_by_id(unique_id)

    return render_template("PackingInChargeOperation.html", row=row, operation=operation, PackingInCharge=PackingInCharge, )

@app.route("/ProcessPackingInChargeOperation", methods=["POST"])
def process_PackingInCharge_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canPackingInCharge = process_role(5)
    if not canPackingInCharge:
        message = "You Don't Have Permission to Access PackingInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = PackingInChargeModel("", "")

    if operation != "Delete":
       obj.packingInChargeID = request.form['packingInChargeID']
       obj.packingInChargeName = request.form['packingInChargeName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.packingInChargeID = request.form["packingInChargeID"]
        obj.update(obj)

    if operation == "Delete":
        packingInChargeID = request.form["packingInChargeID"]
        obj.delete(packingInChargeID)


    return redirect(url_for("PackingInCharge_listing"))
                    
@app.route("/PackingReviewerListing")
def PackingReviewer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPackingReviewer = process_role(6)

    if canPackingReviewer == False:
        message = "You Don't Have Permission to Access PackingReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = PackingReviewerModel.get_all()

    return render_template("PackingReviewerListing.html", records=records)

@app.route("/PackingReviewerOperation")
def PackingReviewer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canPackingReviewer = process_role(6)

    if not canPackingReviewer:
        message = "You Don't Have Permission to Access PackingReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = PackingReviewerModel("", "")

    PackingReviewer = PackingReviewerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = PackingReviewerModel.get_by_id(unique_id)

    return render_template("PackingReviewerOperation.html", row=row, operation=operation, PackingReviewer=PackingReviewer, )

@app.route("/ProcessPackingReviewerOperation", methods=["POST"])
def process_PackingReviewer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canPackingReviewer = process_role(6)
    if not canPackingReviewer:
        message = "You Don't Have Permission to Access PackingReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = PackingReviewerModel("", "")

    if operation != "Delete":
       obj.packingReviewerID = request.form['packingReviewerID']
       obj.packingReviewerName = request.form['packingReviewerName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.packingReviewerID = request.form["packingReviewerID"]
        obj.update(obj)

    if operation == "Delete":
        packingReviewerID = request.form["packingReviewerID"]
        obj.delete(packingReviewerID)


    return redirect(url_for("PackingReviewer_listing"))
                    
@app.route("/ProductionListing")
def Production_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProduction = process_role(7)

    if canProduction == False:
        message = "You Don't Have Permission to Access Production"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductionModel.get_all()

    return render_template("ProductionListing.html", records=records)

@app.route("/ProductionOperation")
def Production_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProduction = process_role(7)

    if not canProduction:
        message = "You Don't Have Permission to Access Production"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductionModel("", "")

    Production = ProductionModel.get_all()
    productionInCharge_list = ProductionInChargeModel.get_name_id()
    print("productionInCharge_list", len(productionInCharge_list))
    productionReviewer_list = ProductionReviewerModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductionModel.get_by_id(unique_id)

    return render_template("ProductionOperation.html", row=row, operation=operation, Production=Production, productionInCharge_list = productionInCharge_list,productionReviewer_list = productionReviewer_list)

@app.route("/ProcessProductionOperation", methods=["POST"])
def process_Production_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProduction = process_role(7)
    if not canProduction:
        message = "You Don't Have Permission to Access Production"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductionModel("", "")

    if operation != "Delete":
       obj.productionID = request.form['productionID']
       obj.companyName = request.form['companyName']
       obj.vaccineName = request.form['vaccineName']
       obj.productionBatchNo = request.form['productionBatchNo']
       obj.productionDateTime = request.form['productionDateTime']
       obj.rawMaterials = request.form['rawMaterials']
       obj.auxiliaryMaterials = request.form['auxiliaryMaterials']
       obj.productionEquipmentParameters = request.form['productionEquipmentParameters']
       obj.abnormalRecord = request.form['abnormalRecord']
       obj.investigationReport = request.form['investigationReport']
       obj.expiryDateTime = request.form['expiryDateTime']
       obj.actualWeight = request.form['actualWeight']
       obj.productionInchargeID = request.form['productionInchargeID']
       obj.productionReviewerID = request.form['productionReviewerID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.productionID = request.form["productionID"]
        obj.update(obj)

    if operation == "Delete":
        productionID = request.form["productionID"]
        obj.delete(productionID)


    return redirect(url_for("Production_listing"))
                    
@app.route("/ProductionInChargeListing")
def ProductionInCharge_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionInCharge = process_role(8)

    if canProductionInCharge == False:
        message = "You Don't Have Permission to Access ProductionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductionInChargeModel.get_all()

    return render_template("ProductionInChargeListing.html", records=records)

@app.route("/ProductionInChargeOperation")
def ProductionInCharge_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionInCharge = process_role(8)

    if not canProductionInCharge:
        message = "You Don't Have Permission to Access ProductionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductionInChargeModel("", "")

    ProductionInCharge = ProductionInChargeModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductionInChargeModel.get_by_id(unique_id)

    return render_template("ProductionInChargeOperation.html", row=row, operation=operation, ProductionInCharge=ProductionInCharge, )

@app.route("/ProcessProductionInChargeOperation", methods=["POST"])
def process_ProductionInCharge_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProductionInCharge = process_role(8)
    if not canProductionInCharge:
        message = "You Don't Have Permission to Access ProductionInCharge"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductionInChargeModel("", "")

    if operation != "Delete":
       obj.productionInChargeID = request.form['productionInChargeID']
       obj.productionInChargeName = request.form['productionInChargeName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.productionInChargeID = request.form["productionInChargeID"]
        obj.update(obj)

    if operation == "Delete":
        productionInChargeID = request.form["productionInChargeID"]
        obj.delete(productionInChargeID)


    return redirect(url_for("ProductionInCharge_listing"))
                    
@app.route("/ProductionReviewerListing")
def ProductionReviewer_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionReviewer = process_role(9)

    if canProductionReviewer == False:
        message = "You Don't Have Permission to Access ProductionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = ProductionReviewerModel.get_all()

    return render_template("ProductionReviewerListing.html", records=records)

@app.route("/ProductionReviewerOperation")
def ProductionReviewer_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canProductionReviewer = process_role(9)

    if not canProductionReviewer:
        message = "You Don't Have Permission to Access ProductionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = ProductionReviewerModel("", "")

    ProductionReviewer = ProductionReviewerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = ProductionReviewerModel.get_by_id(unique_id)

    return render_template("ProductionReviewerOperation.html", row=row, operation=operation, ProductionReviewer=ProductionReviewer, )

@app.route("/ProcessProductionReviewerOperation", methods=["POST"])
def process_ProductionReviewer_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canProductionReviewer = process_role(9)
    if not canProductionReviewer:
        message = "You Don't Have Permission to Access ProductionReviewer"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = ProductionReviewerModel("", "")

    if operation != "Delete":
       obj.productionReviewerID = request.form['productionReviewerID']
       obj.productionReviewerName = request.form['productionReviewerName']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.productionReviewerID = request.form["productionReviewerID"]
        obj.update(obj)

    if operation == "Delete":
        productionReviewerID = request.form["productionReviewerID"]
        obj.delete(productionReviewerID)


    return redirect(url_for("ProductionReviewer_listing"))
                    
@app.route("/RoleListing")
def Role_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(10)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RoleModel.get_all()

    return render_template("RoleListing.html", records=records)

@app.route("/RoleOperation")
def Role_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(10)

    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RoleModel("", "")

    Role = RoleModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RoleModel.get_by_id(unique_id)

    return render_template("RoleOperation.html", row=row, operation=operation, Role=Role, )

@app.route("/ProcessRoleOperation", methods=["POST"])
def process_Role_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRole = process_role(10)
    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RoleModel("", "")

    if operation != "Delete":
       obj.roleID = request.form['roleID']
       obj.roleName = request.form['roleName']
       obj.canRole = 0 
       if request.form.get("canRole") != None : 
              obj.canRole = 1       
       obj.canUsers = 0 
       if request.form.get("canUsers") != None : 
              obj.canUsers = 1       
       obj.canInoculation = 0 
       if request.form.get("canInoculation") != None : 
              obj.canInoculation = 1       
       obj.canInspection = 0 
       if request.form.get("canInspection") != None : 
              obj.canInspection = 1       
       obj.canInspectionInCharge = 0 
       if request.form.get("canInspectionInCharge") != None : 
              obj.canInspectionInCharge = 1       
       obj.canInspectionReviewer = 0 
       if request.form.get("canInspectionReviewer") != None : 
              obj.canInspectionReviewer = 1       
       obj.canPacking = 0 
       if request.form.get("canPacking") != None : 
              obj.canPacking = 1       
       obj.canPackingInCharge = 0 
       if request.form.get("canPackingInCharge") != None : 
              obj.canPackingInCharge = 1       
       obj.canPackingReviewer = 0 
       if request.form.get("canPackingReviewer") != None : 
              obj.canPackingReviewer = 1       
       obj.canProduction = 0 
       if request.form.get("canProduction") != None : 
              obj.canProduction = 1       
       obj.canProductionInCharge = 0 
       if request.form.get("canProductionInCharge") != None : 
              obj.canProductionInCharge = 1       
       obj.canProductionReviewer = 0 
       if request.form.get("canProductionReviewer") != None : 
              obj.canProductionReviewer = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.roleID = request.form["roleID"]
        obj.update(obj)

    if operation == "Delete":
        roleID = request.form["roleID"]
        obj.delete(roleID)


    return redirect(url_for("Role_listing"))
                    
@app.route("/UsersListing")
def Users_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(11)

    if canUsers == False:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UsersModel.get_all()

    return render_template("UsersListing.html", records=records)

@app.route("/UsersOperation")
def Users_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(11)

    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UsersModel("", "")

    Users = UsersModel.get_all()
    role_list = RoleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UsersModel.get_by_id(unique_id)

    return render_template("UsersOperation.html", row=row, operation=operation, Users=Users, role_list = role_list)

@app.route("/ProcessUsersOperation", methods=["POST"])
def process_Users_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUsers = process_role(11)
    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UsersModel("", "")

    if operation != "Delete":
       obj.userID = request.form['userID']
       obj.userName = request.form['userName']
       obj.emailid = request.form['emailid']
       obj.password = request.form['password']
       obj.contactNo = request.form['contactNo']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       obj.roleID = request.form['roleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.userID = request.form["userID"]
        obj.update(obj)

    if operation == "Delete":
        userID = request.form["userID"]
        obj.delete(userID)


    return redirect(url_for("Users_listing"))
                    


import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM Inoculation WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM Inoculation WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM Inoculation WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    if blocksCreated != 0:
        connx = pyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM Inoculation WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        if dbrowx:
            uniqueID = dbrowx[18]
            conny = pyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM Inoculation WHERE sequenceNumber < '" + str(uniqueID) + "' ORDER BY sequenceNumber DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM Inoculation WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[18])

        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE Inoculation SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE sequenceNumber = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM Inoculation WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM Inoculation ORDER BY sequenceNumber DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = InoculationModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11],dbrow[12],dbrow[13],dbrow[14],dbrow[15],dbrow[16],dbrow[17],dbrow[18])
        records.append(row)
    return render_template('BlockChainReport.html', records=records)         

            

 
if __name__ == "__main__":
    app.run()

                    