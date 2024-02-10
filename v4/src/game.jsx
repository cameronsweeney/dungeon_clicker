import React from 'react';
import { useSelector } from 'react-redux';

const DungeonMap = () => {
  <div id="dungeonMap">
    {/* Dungeon map rendering logic here */}
  </div>
}

const StatsContainer = () => {
  const resources = useSelector(state => state.resources);
  
  <div id="statsContainer">
    <div id="resourceLevels">
      <div id="waterLevel">Water: <span>{resources.water}</span></div>
      <div id="oxygenLevel">Oxygen: <span>{resources.oxygen}</span></div>
      <div id="carbonDioxideLevel">CO2: <span>{resources.carbonDioxide}</span></div>
    </div>
  </div>
}

const PopulationLevels = () => {
  const populations = useSelector(state => state.populations);

  <div id="populationLevels">
    <div id="algaePopulation">Algae Population: <span>{populations.algae}</span></div>
    <div id="mushroomPopulation">Mushroom Population: <span>{populations.mushroom}</span></div>
</div>
}

const DungeonGame = () => {
  return (
    <div id="gameContainer">
      <DungeonMap />
      <StatsContainer />
      <PopulationLevels />
    </div>
  );
};

export default DungeonGame;
