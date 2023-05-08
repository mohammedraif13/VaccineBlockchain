pragma solidity >=0.4.22 <0.9.0;
    contract InspectionReviewerContract {
    string public inspectionReviewerID;
	string public inspectionReviewerName;
	bool public isActive;
	
    
    function perform_transactions(string memory _inspectionReviewerID, string memory _inspectionReviewerName, bool _isActive) public{
       inspectionReviewerID = _inspectionReviewerID;
		inspectionReviewerName = _inspectionReviewerName;
		isActive = _isActive;
		
    }
        
}
