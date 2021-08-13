pragma solidity >=0.4.16;

contract {{physician}} {
    string[] the_event;
    string config = "";

    mapping(string => string) details;
    string[] keys;
    string[] values;

    mapping(string => string[]) patients;
    string[] pt_keys;
    string[] pt_values;

    function return_type() public pure returns (string memory) {
        return "physician";
    }

    function initalize() public returns (bool){
        create_patient();
        the_event.push("::contract.functions.clear_event().transact()");
        return true;
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

    function get_config() public view returns (string memory) {
        return config;
    }

    function set_config(string memory _config) public returns (bool) {
        config = _config;
        return true;
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

    function create_patients(string memory key) public returns (bool) {
        patients[key] = [""];
        pt_keys.push(key);
        return true;
    }

    function get_patient_keys() public view returns (string[] memory) {
        return pt_keys;
    }

    function get_patient_values() public view returns (string[] memory) {
        return pt_values;
    }

    function create_patient() public returns (bool){
        the_event.push("::retel_import general_imports");
        the_event.push("::retel_import deploy");
        the_event.push("::retel_import register_instance");
        the_event.push("::str_config = contract.functions.get_config().call()");
        the_event.push("::config = ast.literal_eval(str_config)");
        the_event.push("::if check_config(config) == False: exit(0)");
        the_event.push("::register_init_patient(config,contract_data,contract)");
        return true;
    }
}