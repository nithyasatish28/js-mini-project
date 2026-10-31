
import{useState , useEffect} from "react";
import StationList from "./components/StationList";

const API_URL = "http://127.0.0.1:8001";

function App(){

  const [stations , setStations] = useState([]);
  // we can reload data
  const [Available , setAvailable] = useState({station:[],total:0});
 
 useEffect(()=>{
 fetch(API_URL + "/stations")
 .then((response) => response.json())
 .then((data) => setStations(data )) ;

 fetch(API_URL + "/available")
  .then((response) = response.json())
  .then((data) => setAvailable(data));
 } , []);

function  umbrellasAvailable(id){
  fetch(API_URL = "/Available/add"+id+"/1" , {
  
  })
  .then((response) => response.json())
  .then((data) => setAvailable(data));
}

return(
  <>
  <p> {Available.items.length}</p>
  <StationList stations={stations} onRefresh={umbrellasAvailable}/>
  </>
);
}
export default App;


