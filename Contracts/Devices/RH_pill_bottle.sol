pragma solidity >=0.4.16;

contract {{device}} {
    //Return data from python functions
    string data;
    string ipfs_hash;
    address patient;
    string str_patient;
    address device;
    string str_device;
    uint scheduled = 0;
    
    //For communicating commands to delegator
    string[] the_event;

    //Device Related Dictionaries
    mapping(string => string) details;
    string[] keys;
    string[] values;

    function return_type() public pure returns (string memory) {
        return "device";
    }

    function set_data(string memory _data) public returns (bool) {
        data = _data;
        return true;
    }

    function get_data() public view returns (string memory) {
        return data;
    }

    function set_details(string memory key, string memory value) public returns (bool) {
        details[key] = value;
        keys.push(key);
        values.push(value);
        return true;
    }

    function get_detail_keys() public view returns (string[] memory) {
        return keys;
    }

    function get_detail_values() public view returns (string[] memory) {
        return values;
    }

    function get_event(uint index) public view returns (string memory) {
        return the_event[index];
    }

    function get_event_length() public view returns (uint) {
        return the_event.length;
    }

    function clear_event() public returns (bool) {
        for (uint i = 0; i < the_event.length; i++){
            the_event[i] = "";
        }
        return true;
    }

    function set_hash(string memory value) public returns (bool) {
        ipfs_hash = value;
        return true;
    }
    
    function get_hash() public view returns (string memory) {
        return ipfs_hash;
    }

    function step1() public returns (bool){
        //Init: Schedule step 1 to run routinely
        if (scheduled == 0){
            the_event.push("::retel_import general_imports");
            the_event.push("::schedule,2,");
            the_event.push(str_device);
            scheduled = 1;
        }
        //Get data from api
        the_event.push("::retel_import parse");
        the_event.push("::retel_import general_imports");
        the_event.push("::device_data = ripplehealth(\'");
        the_event.push(details['url']);
        the_event.push("\')");
        //Send data to patient.sol
        the_event.push("::patient_contract.functions.set_device_data(device_key,device_data,'adherence').transact()");
        //Clear events and move to step 2
        the_event.push("::contract.functions.clear_event().transact()");
        the_event.push("::patient_contract.functions.step1().transact()");
        publish_data();
        return true;
    }
    function step2() public returns (bool){
        return true;

    }
    function publish_data() public returns (bool){
        the_event.push("::retel_import general_imports");
        //Get data from api
        the_event.push("::retel_import parse");
        the_event.push("::retel_import general_imports");
        the_event.push("::retel_import publish");
        the_event.push("::device_data = ripplehealth(\'");
        the_event.push(details['url']);
        the_event.push("\')");
        the_event.push("::publish_data(device_data,\'");
        the_event.push(details["medication_name"]);
        the_event.push("\',\'");
        the_event.push(details["dosage"]);
        the_event.push("\')");
        return true;
    }

    function set_patient_addr(address _a,string memory key) public{
        patient = _a;
        str_patient = key;
    }

    function set_device_addr(address _a,string memory key) public{
        device = _a;
        str_device = key;
    }
    
    function get_device_addr() public returns (address) {
        return device;
    }

    function get_patient_addr() public returns (string memory) {
        return str_patient;
    }
}