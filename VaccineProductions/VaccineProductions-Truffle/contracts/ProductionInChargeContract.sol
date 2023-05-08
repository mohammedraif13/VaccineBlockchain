    pragma solidity >=0.4.22 <0.9.0;
        contract ProductionInChargeContract {
        string public productionInChargeID;
        string public productionInChargeName;
        bool public isActive;


        function perform_transactions(string memory _productionInChargeID, string memory _productionInChargeName, bool _isActive) public{
           productionInChargeID = _productionInChargeID;
            productionInChargeName = _productionInChargeName;
            isActive = _isActive;

        }

    }
