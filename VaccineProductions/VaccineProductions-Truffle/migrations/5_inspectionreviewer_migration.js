const InspectionReviewer = artifacts.require("InspectionReviewerContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(InspectionReviewer);
        };
        