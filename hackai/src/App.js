import React, { useState, useEffect } from "react";
import './App.css';
import Graph from './Graph.js';
import Header from './Header.js';
import PlayList from './PlayList.js';
import TwitterInput from './TwitterInput.js';
import Indicator from './Indicator.js';
import Footer from './Footer.js';

function App() {
  const data = [{ msg: "Slam jammers!", time: "8:00" }, { msg: "Testing a really long potential tweet that could span multiple lines, sometimes with emojis and at's to very specific people, such as Lebron James, Karl Anthony Townes, or Michael Jordan, even though he is retired, because he is a current owner of an NBA franchise.", time: "8:02" }, { msg: "LeBum...LeWashed...LeChoking", time: "8:05" }];
  var [body, setBody] = useState([]);
  var [count, setCount] = useState([]);
  if (body.length === 0){
    body.push({msg: "Lebron James dunks", generated: "Lebron james with the slam!", score:7, time: 123})
    setBody(body); 
  }
  
  useEffect(() => {
    // body.push({score:Math.random()*10, time:time.toString()}); 
    const interval = setInterval(() => {
      count += 1;
      setCount(count);
      if (body.length > 4) {
        body.shift();
      }
      fetch("http://127.0.0.1:5000").then(
        response => response.json()
      ).then(data => {
        body.push(data);
        setBody(data);
        console.log(body)
      }
      );
      console.log(count); 

    }, 10000);

    return () => clearInterval(interval);
  }, []);
  return (
    <div className="App" style={{ "background-color": "#B8C4CA", "display": "block", "overflow": "auto", "height": "100vfh", }}>

      <Header></Header>
      <div style={{ height: "75%" }}>
        <Graph data={body}></Graph>
      </div>
      <div style={{ width: "30%", margin: "1%", padding: "1%", display: 'flex', float: 'left', outline: '#B8C4CA solid 5px', backgroundColor: "white" }}>
        <TwitterInput>
        </TwitterInput>
      </div>
      <div style={{ width: "18%", margin: "1%", marginLeft: "3%", padding: "1%", display: 'flex', float: 'left', outline: '#B8C4CA solid 5px', backgroundColor: "white" }}>
        <Indicator data={body}></Indicator>

      </div>

      <div style={{ width: "42%", margin: "1%", padding: "1%", display: 'flex', float: 'right', outline: '#B8C4CA solid 5px', backgroundColor: "white" }}>
        <PlayList data={body} title={"Generated Tweets"} generated={true}>
        </PlayList>
      </div>
      {/* <hr style={{ width: "30%", margin: "1%"}}></hr> */}
      {/* <Footer></Footer> */}

    </div >
  );
}

export default App;
