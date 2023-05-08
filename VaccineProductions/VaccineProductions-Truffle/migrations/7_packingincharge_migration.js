const PackingInCharge = artifacts.require("PackingInChargeContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(PackingInCharge);
        };
        