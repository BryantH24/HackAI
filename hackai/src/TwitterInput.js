import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

function TwitterInput(){
return (
    <div>
      <h2 className="mb-6 text-center text-3xl font-extrabold text-gray-900">
        Your Tweet
      </h2>
      <TextField
          id="outlined-multiline-static"
          label="Multiline"
          multiline
          rows={9}
          defaultValue=""
          style={{width: '130%'}}
        />
      <Button variant="contained" style={{margin: "8%", marginLeft:"30%"}}>Send Tweet</Button>
      </div>
  )
 }
 
 export default TwitterInput; 