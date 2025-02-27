// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

contract BasicRecord {
    address public immutable admin;
    
    constructor() {
        admin = msg.sender;
    }
    
    struct Record {
        uint256 record_id;
        string[] fields;
    }
    
    mapping(uint256 => Record) public records;
    
    uint256 public recordCount;

    function addRecord(
        uint256 _record_id,
        string[] memory _fields
    ) public {
        recordCount++;
        records[_record_id] = Record(_record_id, _fields);
    }

    function getRecord(uint256 _record_id) public view returns (Record memory) {
        return records[_record_id];
    }

    function deleteRecord(uint256 _record_id) public {
        require(records[_record_id].record_id != 0, "Record does not exist");
        recordCount--;
        delete records[_record_id];
    }
}