        pragma solidity >=0.4.22 <0.9.0;
        import "./InspectionContract.sol";

        interface Vaccine {

            function totalSupply() external view returns (uint256);
            function balanceOf(address account) external view returns (uint256);
            function transfer(address to, uint256 amount) external returns (bool);
            function allowance(address owner, address spender) external view returns (uint256);
            function approve(address spender, uint256 amount) external returns (bool);
            function transferFrom(address from, address to, uint256 amount) external returns (bool);
        }

        contract InoculationContract {
            string public inoculationID;
            string public productionBatchNo;
            string public vaccineRecipientName;
            uint256 public inoculationDateTime;
            string public vaccineRecipientAadharNo;
            string public vaccineRecipientAddress;
            string public vaccineRecipientCity;
            string public vaccineRecipientState;
            string public vaccineRecipientPincode;
            string public vaccineRecipientCountry;
            uint256 public vaccineRecipientDob;
            string public inoculationDose;
            string public inoculationDepartment;
            string public inoculationDoctorName;
            string public inoculationDoctorNumber;


            uint256 public gas;
            function check_strict() external {
                    gas = gasleft();
                    require(999999999999999999 > 1);
                    gas -= gasleft();
                }
            function check_non_strict() external {
                    gas = gasleft();
                    require(999999999999999999 >= 1);
                    gas -= gasleft();
                }
            function calculate_gas_1(uint x) public {
                gas = gasleft();
                require(x == 0 && x < 1 );
                gas -= gasleft();
            }
            function calculate_gas_2(uint x) public {
                    gas = gasleft();
                    require(x == 0);
                    require(x < 1);
                    gas -= gasleft();
                }

                function perform_transactions(string memory _inoculationID, string memory _productionBatchNo, string memory _vaccineRecipientName,  string memory _inoculationDose, string memory _inoculationDepartment, string memory _inoculationDoctorName, string memory _inoculationDoctorNumber) public{
               inoculationID = _inoculationID;
                productionBatchNo = _productionBatchNo;
                vaccineRecipientName = _vaccineRecipientName;
                inoculationDose = _inoculationDose;
                inoculationDepartment = _inoculationDepartment;
                inoculationDoctorName = _inoculationDoctorName;
                inoculationDoctorNumber = _inoculationDoctorNumber;

            }
        uint8 resultA = 0;
            uint256 resultB = 0;

            function UseUint() external returns (uint256) {
                uint256 selectedRange = 50;
                for (uint256 i = 0; i < selectedRange; i++) {
                    resultB += 1;
                }
                return resultB;
            }

            function UseUInt8() external returns (uint8) {
                uint8 selectedRange = 50;
                for (uint8 i = 0; i < selectedRange; i++) {
                    resultA += 1;
                }
                return resultA;
            }

        }
