import Grid from '@mui/material/Grid';

import * as React from 'react';

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';

import ListItemText from '@mui/material/ListItemText';

import Typography from '@mui/material/Typography';



function PlayList(props) {
    // console.log(props);  
    return (
        <Grid item xs={1} md={1}>
            <Typography sx={{ mt: 1, mb: 1 }} variant="h6" component="div" textAlign='center'>
                {props.title}
            </Typography>
            <List dense="false">
                {props.data?.map((play) => {
                    return (
                        <ListItem>
                            <ListItemText
                                primary={(props.generated) ? play.generated: play.msg}
                                secondary={play.time}
                            />
                        </ListItem>)
                }
                )}
            </List>
        </Grid>
    );
}


export default PlayList; 
