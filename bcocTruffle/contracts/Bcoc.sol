pragma solidity >=0.4.22 <0.6.0;

contract Bcoc {
    
    //mapper function for registration
    
    mapping (string => address) private userAddress;
    mapping (string => string) private userHash;
    
    //mapper function for createEvidence
    
    mapping (string => address) private evidenceOwner;
    mapping (string => string) private evidenceIpfsHash;
    
    function registration(string memory _userID, address _walletAddress, string memory _userIpfsHash) public {
        userAddress[_userID] = _walletAddress;
        userHash[_userID] = _userIpfsHash;
    }
    
    function login (string memory _userID) view public returns (string memory, address) {
        string memory _userIpfsHash = userHash[_userID];
        address _userWalletAddress = userAddress[_userID];
        return (_userIpfsHash, _userWalletAddress);
    }
    
    function createEvidence(string memory _evidenceID, string memory _evidenceIpfsHash) public {
        evidenceOwner[_evidenceID] = msg.sender;
        evidenceIpfsHash[_evidenceID] = _evidenceIpfsHash;
    }
    
    function transferEvidence(string memory _evidenceID, string memory _newOwnerID) public returns (bool) {
        require(evidenceOwner[_evidenceID] == msg.sender);
        address currentOwnerAddress = userAddress[_newOwnerID];
        evidenceOwner[_evidenceID] = currentOwnerAddress;
        return true;
    }
    
    function getEvidence(string memory _evidenceID) view public returns (string memory) {
        require(evidenceOwner[_evidenceID] == msg.sender);
        string memory evidenceHash = evidenceIpfsHash[_evidenceID];
        return evidenceHash;
    }
}
