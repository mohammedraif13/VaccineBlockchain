pragma solidity >=0.4.22 <0.9.0;
    contract InspectionContract {
    string public inspectionID;
	string public productionBatchNo;
	string public dosageForm;

	string public inspectionInChargeID;
	string public inspectionReviewerID;
	
    
    function perform_transactions(string memory _inspectionID, string memory _productionBatchNo, string memory _dosageForm, string memory _inspectionInChargeID, string memory _inspectionReviewerID) public{
       inspectionID = _inspectionID;
		productionBatchNo = _productionBatchNo;
		dosageForm = _dosageForm;

		inspectionInChargeID = _inspectionInChargeID;
		inspectionReviewerID = _inspectionReviewerID;
		
    }
        
}
