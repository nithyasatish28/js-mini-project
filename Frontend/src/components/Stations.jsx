import {useState, useEffect} from 'react';

function Stations() {
    const [stations, setStations] = useState([]);
    const [selectedStation, setSelectedStation] = useState(null);
    const [rollNumber, setRollNumber] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    function fetchStations() {
        fetch(apiUrl + '/stations')
            .then(response => response.json())
            .then(data => setStations(data))
    }

    useEffect(() => {
        fetchStations();
    }, [apiUrl]);


}

export default Stations;