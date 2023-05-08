pragma solidity >=0.4.22 <0.9.0;
    contract PackingContract {
    string public packingID;
	string public productionBatchNo;
	string public packingBatchNo;

	string public packingInchargeID;
	string public packingReviewerID;
	
    
    function perform_transactions(string memory _packingID, string memory _productionBatchNo, string memory _packingBatchNo,  string memory _packingInchargeID, string memory _packingReviewerID) public{
       packingID = _packingID;
		productionBatchNo = _productionBatchNo;
		packingBatchNo = _packingBatchNo;

		packingInchargeID = _packingInchargeID;
		packingReviewerID = _packingReviewerID;
		
    }
        
}
