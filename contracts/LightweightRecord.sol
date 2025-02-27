// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

contract LightweightRecord {
    address public immutable admin;

    constructor() {
        admin = msg.sender;
    }

    struct Record {
        uint256 record_id;
        bytes32 data_hash;
        string ipfs_hash;
    }


    mapping(uint256 => Record) public records;

    uint256 public recordCount;

    function addRecord(
        uint256 _record_id,
        string[] memory _fields,
        string memory _ipfs_hash
    ) public {
        recordCount++;
        bytes32 _data_hash = 0x0;
        for (uint256 i = 0; i < _fields.length; i++) {
            _data_hash = keccak256(abi.encodePacked(_data_hash, keccak256(bytes(_fields[i]))));
        }

        records[_record_id] = Record(_record_id, _data_hash, _ipfs_hash);
    }

    function getRecord(uint256 _record_id) public view returns (Record memory) {
        return records[_record_id];
    }

    function getRecordIPFSHash(uint256 _record_id) public view returns (Record memory) {
        require(recordExists(_record_id), "Record does not exist");
        return records[_record_id];
    }


    function verifyRecord(uint256 _record_id, string[] memory _fields) public view returns (bool) {
        require(recordExists(_record_id), "Record does not exist");
        bytes32 computed_hash = 0x0;
        for (uint256 i = 0; i < _fields.length; i++) {
            computed_hash = keccak256(abi.encodePacked(computed_hash, keccak256(bytes(_fields[i]))));
        }
        return records[_record_id].data_hash == computed_hash;
    }


    function deleteRecord(uint256 _record_id) public {
        require(recordExists(_record_id), "Doctor does not exist");
        recordCount--;
        delete records[_record_id];
    }


    function recordExists(uint256 _record_id) internal view returns (bool) {
        return records[_record_id].record_id != 0;
    }
}
