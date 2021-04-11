import './App.css';

// Import components
import ImageWindow from './components/imageWindow';
import HistorySidebar from './components/historySidebar'
import Login from './components/login'

// Other items lower on the priorities list
//import RoboticStatusBar from './components/roboticStatusBar'
// Make history panel and login sidebar collapsable

function App() {
  return (
    <div className="d-flex flex-row justify-content-between ">
      <div className="p-0"><HistorySidebar /></div>
      <div className="p-5"><ImageWindow /></div>
      <div className="p-0"><Login /></div>
    </div>
  );
}

export default App;
