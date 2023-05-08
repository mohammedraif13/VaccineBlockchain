pragma solidity >=0.4.22 <0.9.0;
    contract ProductionReviewerContract {
    string public productionReviewerID;
	string public productionReviewerName;
	bool public isActive;
	
    
    function perform_transactions(string memory _productionReviewerID, string memory _productionReviewerName, bool _isActive) public{
       productionReviewerID = _productionReviewerID;
		productionReviewerName = _productionReviewerName;
		isActive = _isActive;
		
    }
        
}
