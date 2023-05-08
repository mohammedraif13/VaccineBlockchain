pragma solidity >=0.4.22 <0.9.0;
    contract UsersContract {
    int public userID;
	string public userName;

	
    
    function perform_transactions(int _userID, string memory _userName) public{
       userID = _userID;
		userName = _userName;

		
    }
        
}
