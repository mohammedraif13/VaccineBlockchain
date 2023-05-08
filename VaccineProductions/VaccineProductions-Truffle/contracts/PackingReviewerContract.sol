pragma solidity >=0.4.22 <0.9.0;
    contract PackingReviewerContract {
    string public packingReviewerID;
	string public packingReviewerName;
	bool public isActive;
	
    
    function perform_transactions(string memory _packingReviewerID, string memory _packingReviewerName, bool _isActive) public{
       packingReviewerID = _packingReviewerID;
		packingReviewerName = _packingReviewerName;
		isActive = _isActive;
		
    }
        
}
