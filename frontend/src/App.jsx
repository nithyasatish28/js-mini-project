import {useEffect, useState} from 'react'

import './App.css'
import Garden from "./components/Garden.jsx";

const API_URL = "http://127.0.0.1:8001"

function App() {
  const [plants,setPlants] = useState([])

  useEffect(() => {
    fetch(API_URL + "/plants")
        .then((response) => response.json())
        .then((data) => setPlants(data));
  }, []);

  return <>
    <Garden plants={plants}/>
    <plants plants ={plants} adopted_by={adopted_by} />
  </>
}

export default App
