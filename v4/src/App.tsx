import './App.css'
import './game.jsx'
import AddCo2Button from './components/AddCo2Button';

function App() {
  return (
    <div id="gameContainer">
      <div id="dungeonMap"></div>
      <div id="statsContainer">
        <div id="resourceLevels">
          <div id="waterLevel">Water: <span>0</span></div>
          <div id="oxygenLevel">Oxygen: <span>0</span></div>
          <div id="carbonDioxideLevel">CO2: <span>0</span></div>
        </div>
        <div id="populationLevels">
          <div id="algaePopulation">Algae Population: <span>0</span></div>
          <div id="mushroomPopulation">Mushroom Population: <span>0</span></div>
        </div>
      </div>
      <AddCo2Button />
    </div>
  )
}

export default App
