import StationList from "./components/StationList";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";
import "./styles/app.css";

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>Campus Umbrella Sharing</h1>
        <p>Borrow anywhere. Return anywhere.</p>
      </header>

      <main>
        <StationList />

        <div className="sections">
          <MyUmbrella />
          <AddStation />
        </div>
      </main>
    </div>
  );
}

export default App;
