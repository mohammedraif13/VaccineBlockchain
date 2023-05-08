const Inoculation = artifacts.require("InoculationContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Inoculation);
        };
        