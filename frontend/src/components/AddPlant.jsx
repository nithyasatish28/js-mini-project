import {useState} from "react";

const API_URL = "http://127.0.0.1:8001";


function AddPlant({setPlants}){
    const [name,setName] = useState("")
    const [type,setType] = useState("succulent")
    const [location,setLocation] = useState("")
    const [water,setWater] = useState(1)

    function handleName(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setName(e.target.value);
    }

    function handleType(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setType(e.target.value);

    }
    function handleLocation(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setLocation(e.target.value);
    }
    function handleWater(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setWater(e.target.value);
    }

    function addPlant(){
        let query = `?name=${name}&type=${type}&location=${location}&water_every_days=${water}`;
        fetch(API_URL + `/plants` + query, {
            method: "POST"

        })
            .then((response) => response.json())
            .then(() => {
                return fetch(API_URL + "/plants");// fetching the updated list of plants

            })
            .then((response) => response.json())
            .then((data) => setPlants(data))

    }

    function handleSubmit(e) {
        e.preventDefault(); // Prevents the page from refreshing on form submit
        addPlant()
    }

    return <>
        <form onSubmit={handleSubmit}>
            <label>Name:
                <input
                    type="text"
                    value={name}
                    onChange={handleName}
                />
            </label>

            <label>type:
                <select name="type" value={type} onChange={handleType}>
                    <option value="succulent">succulent</option>
                    <option value="flowering">flowering</option>
                    <option value="herb">herb</option>
                    <option value="indoor">indoor</option>
                    <option value="tree">tree</option>
                </select>

            </label>
            <label>location:
                <input
                    type="text"
                    value={location}
                    onChange={handleLocation}
                />
            </label>
            <label>water every days:
                <input
                    type="number"
                    value={water}
                    onChange={handleWater}
                    min="1"
                    max="14"
                />
            </label>
            <button type='submit'>Add</button>
        </form>

    </>
}

export default AddPlant