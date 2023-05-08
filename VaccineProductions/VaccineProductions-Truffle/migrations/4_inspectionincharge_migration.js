const InspectionInCharge = artifacts.require("InspectionInChargeContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(InspectionInCharge);
        };
        