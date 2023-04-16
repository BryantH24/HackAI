import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const bull = (
  <Box
    component="span"
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

export default function Indicator(props) {
  return (
    <Card sx={{ minWidth: 100 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          Current ELS
        </Typography>
        <Typography variant="h2" component="div">
          {props.data[props.data.length-1].score}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          0 - 4: Low Predicted Engagement
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          4 - 8: Medium Predicted Engagement
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          8 - 10: High Predicted Engagement
        </Typography>
        {/* <Typography variant="body2">
          well meaning and kindly.
          <br />
          {'"a benevolent smile"'}
        </Typography> */}
      </CardContent>
      {/* <CardActions>
        <Button size="small">Learn More</Button>
      </CardActions> */}
    </Card>
  );
}