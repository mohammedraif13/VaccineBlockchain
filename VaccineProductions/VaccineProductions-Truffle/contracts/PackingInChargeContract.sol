pragma solidity >=0.4.22 <0.9.0;
    contract PackingInChargeContract {
    string public packingInChargeID;
	string public packingInChargeName;
	bool public isActive;
	
    
    function perform_transactions(string memory _packingInChargeID, string memory _packingInChargeName, bool _isActive) public{
       packingInChargeID = _packingInChargeID;
		packingInChargeName = _packingInChargeName;
		isActive = _isActive;
		
    }
        
}
