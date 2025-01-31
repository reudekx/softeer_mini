import PlayerDashboard from './components/PlayerDashboard';
import sampleData from './data/sample-data.json';

function App() {
  return (
    <div className="container mx-auto py-8">
      <PlayerDashboard data={sampleData} />
    </div>
  );
}

export default App;