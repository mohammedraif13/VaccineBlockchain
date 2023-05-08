    pragma solidity >=0.4.22 <0.9.0;
        contract RoleContract {
        int public roleID;
        string public roleName;
        bool public canRole;
        bool public canUsers;
        bool public canInoculation;
        bool public canInspection;
        bool public canPacking;
        bool public canProduction;



        function perform_transactions(int _roleID, string memory _roleName, bool _canRole, bool _canUsers, bool _canInoculation, bool _canInspection,  bool _canPacking,  bool _canProduction) public{
           roleID = _roleID;
            roleName = _roleName;
            canRole = _canRole;
            canUsers = _canUsers;
            canInoculation = _canInoculation;
            canInspection = _canInspection;

            canPacking = _canPacking;

            canProduction = _canProduction;


        }

    }
