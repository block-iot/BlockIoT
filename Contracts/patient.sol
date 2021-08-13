pragma solidity >=0.4.16;

contract {{patient}} {
    
    //Return data from python functions
    uint time;
    string config = "";
    string specs = "";
    address patient;
    //For communicating commands to delegator
    string[] the_event;

    //Patient Related Dictionaries
    mapping(string => string) details;
    string[] keys;
    string[] values;

    //Connecting devices to the patient
    //device_key => [data,analysis_function]
    mapping(string => string[]) device_data;
    string[] device_key;
    mapping(string => bool) repeat;

    mapping(string => uint) medical_data;
    string[] medical_key;
    
    mapping(string => string) patient_consent_data;
    mapping(string => string[]) patient_consent_relatives;

    function return_type() public pure returns (string memory) {
        return "patient";
    }
    
    function get_config() public view returns (string memory) {
        return config;
    }

    function set_config(string memory _config) public returns (bool) {
        config = _config;
        return true;
    }

    function set_device_data(string memory _device_key,string memory data, string memory analysis_function) public returns (bool) {
        if (repeat[_device_key] == true){
            device_data[_device_key] = [data,analysis_function,""];
        }
        else{
            repeat[_device_key] = true;
            device_key.push(_device_key);
            device_data[_device_key] = [data,analysis_function,""];
        }
        return true;
    }

    function get_device_data(string memory _device_key) public view returns (string[] memory) {
        return device_data[_device_key];
        //return device_key.length;
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
    function get_device_length() public view returns (uint) {
        return device_key.length;
    }

    function clear_event() public returns (bool) {
        for (uint i = 0; i < the_event.length; i++){
            the_event[i] = "";
        }
        return true;
    }
    
    function create_devices(string memory pt_key) public returns (bool){
        the_event.push("::retel_import general_imports");
        the_event.push("::retel_import deploy");
        the_event.push("::retel_import register_instance");
        the_event.push("::str_config = contract.functions.get_config().call()");
        the_event.push("::config = ast.literal_eval(str_config)");
        the_event.push("::if check_config(config) == False: print('wtf')");
        the_event.push("::patient_key = '");
        the_event.push(pt_key);
        the_event.push("'");
        the_event.push("::register_init_device(config,patient_key,contract_data,contract)");
        the_event.push("::contract.functions.clear_event().transact()");
    }

    function step1() public returns (bool){
       for (uint i = 0; i < device_key.length ; i++){
           the_event.push("::retel_import adherence");
           the_event.push("::retel_import general_imports");
           the_event.push("::device_data = ");
           the_event.push(device_data[device_key[i]][0]);
           the_event.push("::report = ");
           the_event.push(device_data[device_key[i]][1]);
           the_event.push("(device_data,'");
           the_event.push(specs);
           the_event.push("')");
           the_event.push("::contract.functions.");
           the_event.push(device_data[device_key[i]][1]);
           the_event.push("(report[0],report[1]).transact()");
       }
       return true;
    }
    function adherence(string[] memory keys,uint[] memory values) public returns (bool){
        //Data is data * 100!
        medical_key = keys;
        for (uint i = 0; i < keys.length; i ++){
            medical_data[keys[i]] = values[i];
        }
        if (send_alert_patient() == true){
            the_event.push("::print('Sample Alert to to Patient Sent!')");
        }
        if (send_alert_physician() == true){
            the_event.push("::print('Sample Alert to Physician Sent!')");
        }
        return true;
    }
    function send_alert_patient() public returns (bool){
        //Needs to be more sophisticated
        if (medical_data["7-day-limit"] == 1){
            return true;
        }
        else{
            return false;
        }
    }
    function send_alert_physician() public returns (bool){
        //Needs to be more sophisticated
        if (medical_data["30-day-limit"] == 1){
            return true;
        }
        else{
            return false;
        }
    }
}