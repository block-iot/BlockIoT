pragma solidity >=0.4.16;

contract auAtORgtVjE0pGTFxEuV9 {
    //Return data from python functions
    string data;
    string ipfs_hash;
    address patient;
    string str_patient;
    address device;
    string str_device;
    uint scheduled = 1;
    
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
            the_event.push("schedule.every(10).seconds.do(contract.functions.step1().transact())");
            scheduled = 1;
        }

        //Get data from api
        the_event.push("::last = ripplehealth(\'");
        the_event.push(details['url']);
        the_event.push("\')");
        //Send data to patient.sol
        the_event.push("::patient_contract.functions.set_device_data(device_key,last,'adherence').transact()");
        //Clear events and move to step 2
        the_event.push("::contract.functions.clear_event().transact()");
        the_event.push("::contract.functions.step2().transact()");
        the_event.push("::patient_contract.functions.step1().transact()");
        return true;
    }
    function step2() public returns (bool){
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

    function send_data() public returns (bool){
        (bool success, bytes memory data) = patient.delegatecall(abi.encodeWithSignature("set_data(string memory)", data));
        //require(patient.call(bytes4(keccak256("set_data(string)")),data));
        return success;
    }

    // function self_destruct() public returns (bool){
    //     self destruct 
    // }

    // function send patient data() public returns (bool){
    //     return [patient_alerts,patient_device_pointers,physician_pointers,graph_data]
    // }

    // function initialize(patient_data){

    // }
}