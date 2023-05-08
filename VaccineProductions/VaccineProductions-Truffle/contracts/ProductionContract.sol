pragma solidity >=0.4.22 <0.9.0;
    contract ProductionContract {
    string public productionID;
	string public companyName;
	string public vaccineName;
	string public productionBatchNo;



    function perform_transactions(string memory _productionID, string memory _companyName, string memory _vaccineName, string memory _productionBatchNo) public{
       productionID = _productionID;
		companyName = _companyName;
		vaccineName = _vaccineName;
		productionBatchNo = _productionBatchNo;


    }

}
