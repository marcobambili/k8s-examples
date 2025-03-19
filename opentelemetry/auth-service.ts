import start from './tracer';
start('auth-service');
import opentelemetry from '@opentelemetry/api';


import express from 'express';
const app = express();

const { trace } = require('@opentelemetry/api');



app.get('/auth',(req,res)=>{
    res.json({username: 'Michael Haberman'})
  
    // Ottieni lo span attivo
const activeSpan = trace.getActiveSpan();

if (activeSpan) {
  // Imposta gli attributi usando setAttributes
  activeSpan.setAttributes({
    username: 'Michael Attrb'
  });
}


})

app.listen(8080, () => {
    console.log('service is up and running!');
})