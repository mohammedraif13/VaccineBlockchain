const ProductionInCharge = artifacts.require("ProductionInChargeContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(ProductionInCharge);
        };
        