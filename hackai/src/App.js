import './App.css';
import Graph from './Graph.js';
import Header from './Header.js';
import PlayList from './PlayList.js';
import TwitterInput from './TwitterInput.js';
import Indicator from './Indicator.js';
import Footer from './Footer.js';

function App() {
  const data = [{ msg: "Slam jammers!", time: "8:00" }, { msg: "Testing a really long potential tweet that could span multiple lines, sometimes with emojis and at's to very specific people, such as Lebron James, Karl Anthony Townes, or Michael Jordan, even though he is retired, because he is a current owner of an NBA franchise.", time: "8:02" }, { msg: "LeBum...LeWashed...LeChoking", time: "8:05" }];
  return (
    <div className="App" style={{ "background-color": "#B8C4CA", "display": "block", "overflow": "auto", "height": "100vfh",}}>
      
      <Header></Header>
      <div style={{height: "75%"}}>
      <Graph></Graph>
      </div>
      <div style={{ width: "30%", margin: "1%", padding: "1%", display: 'flex', float: 'left', outline: '#B8C4CA solid 5px', backgroundColor: "white"}}>
        <TwitterInput>
        </TwitterInput>
      </div>
      <div style={{ width: "18%", margin: "1%", marginLeft:"3%", padding: "1%", display: 'flex', float:'left', outline: '#B8C4CA solid 5px', backgroundColor: "white"}}>
      <Indicator></Indicator>

      </div>

      <div style={{ width: "42%", margin: "1%", padding: "1%", display: 'flex', float: 'right', outline: '#B8C4CA solid 5px', backgroundColor: "white"}}>
        <PlayList data={data} title={"Generated Tweets"}>
        </PlayList>
      </div>
      {/* <hr style={{ width: "30%", margin: "1%"}}></hr> */}
      {/* <Footer></Footer> */}

    </div >
  );
}

export default App;