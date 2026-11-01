import {useEffect, useState} from 'react'

import './App.css'
import Garden from "./components/Garden.jsx";
import MyPlants from './components/MyPlants.jsx';
import RollForm from './components/RollInput.jsx';

const API_URL = "http://127.0.0.1:8001"

function App() {
  const [plants,setPlants] = useState([])
  const [adoptedBy, setAdoptedBy] = useState("")

  useEffect(() => {
    fetch(API_URL + "/plants")
        .then((response) => response.json())
        .then((data) => setPlants(data));
  }, []);

  return <>
    <Garden plants={plants}/>
    <h1>My Plants</h1>
    <RollForm setAdoptedBy={setAdoptedBy}/>
    <MyPlants plants ={plants} adopted_by={adoptedBy} />
  </>
}

export default App
