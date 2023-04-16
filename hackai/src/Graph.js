import React, { useState, useEffect } from "react";
import PlayList from './PlayList.js';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Line } from 'react-chartjs-2';
import { getTableBodyUtilityClass } from "@mui/material";
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

String.prototype.toHHMMSS = function () {
  var sec_num = parseInt(this, 10); // don't forget the second param
  var hours   = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours   < 10) {hours   = "0"+hours;}
  if (minutes < 10) {minutes = "0"+minutes;}
  if (seconds < 10) {seconds = "0"+seconds;}
  return hours+':'+minutes+':'+seconds;
}


function LineGraph() {
  var [body, setBody] = useState([]);
  var [count, setCount] = useState(0);
  var time = new Date();
  useEffect(() => {
    // body.push({score:Math.random()*10, time:time.toString()}); 
    const interval = setInterval(() => {
      time = new Date();
      body.push({score:Math.random()*10, time:time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds()});
      count += 1;  
      setBody(body);
      setCount(count); 
      if (body.length > 40){
        body.shift(); 
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);


  console.log(body); 
  const data = [{msg: "Dunk", time: "8:00"},{msg: "Turnover", time: "8:02"}, {msg: "LeBum sat out", time: "8:05"}]; 

  return (
    <div style={{ width: '100%', overflow: 'hidden' }}>
      <div style={{ width: "50%", margin: "1%", padding: "1%", float: 'left', display: 'flex', backgroundColor: "white", outline: '#B8C4CA solid 5px' }}>
        <Line
          data={{
            // x-axis label values
            labels: body.map((value) =>value.time),
            datasets: [
              {
                label: "ElongatedSocialMetric",
                // y-axis data plotting values
                data: body.map((value) =>value.score),
                fill: true,
                borderWidth: 4,
                backgroundColor: "rgb(0, 43, 92)",
                borderColor: 'rgb(0, 83, 188)',
                responsive: false
              },
            ],
          }}
          options={{ maintainAspectRatio: true , animation:false}}
        />
      </div>

      <div style={{ width: "42%", margin: "1%", padding: "1%", display: 'flex', float: 'right', outline: '#B8C4CA solid 5px', backgroundColor: "white"}}>
        <PlayList data={data} title={"Game Play Feed"} textAlign="center"></PlayList>
      </div>
    </div>
  );
}

export default LineGraph;