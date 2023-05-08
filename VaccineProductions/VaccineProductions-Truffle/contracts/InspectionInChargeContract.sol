    pragma solidity >=0.4.22 <0.9.0;
        contract InspectionInChargeContract {
        string public inspectionInChargeID;
        string public inspectionInChargeName;
        bool public isActive;


        function perform_transactions(string memory _inspectionInChargeID, string memory _inspectionInChargeName, bool _isActive) public{
           inspectionInChargeID = _inspectionInChargeID;
            inspectionInChargeName = _inspectionInChargeName;
            isActive = _isActive;

        }

    }
