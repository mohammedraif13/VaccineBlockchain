const Inspection = artifacts.require("InspectionContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Inspection);
        };
        