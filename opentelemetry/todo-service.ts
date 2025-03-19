import start from './tracer';
const meter = start('todo-service');
import express from 'express';
import axios from 'axios';
import { ValueType } from '@opentelemetry/api';

const app = express();

import Redis from "ioredis";
const redis = new Redis({host:'redis'});


// 2. Creazione dell'Histogram con unità di misura corretta
const httpCallDuration = meter.createHistogram('http_call_duration', {
    description: 'Duration of HTTP requests in milliseconds',
    unit: 'ms',

    // Configurazione specifica per gli histogram
  valueType: ValueType.INT // o 'DOUBLE' a seconda dei casi
  });


// Esempio: contatore delle richieste
const requestCounter = meter.createCounter('http_requests_total', {
  description: 'Total number of HTTP requests',
});

// Simula richieste
setInterval(() => {
  requestCounter.add(1);
  console.log('Request counted!');
}, 3000);




// 3. Middleware corretto
app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = Date.now() - start;
      
      httpCallDuration.record(duration, {
        method: req.method,
        route: req.route?.path || req.path,
        status_code: res.statusCode.toString(), // Prometheus richiede stringhe come valori
      });
    });
  
    next();
  });

  const sleep = (time:number)=>{return new Promise((resolve)=>{setTimeout(resolve,time)})};


app.get('/todos', async (req, res) => {
    const user = await axios.get('http://auth:8080/auth');
    const todoKeys = await redis.keys('todo:*');
    const todos: any = [];
    for (let i = 0; i < todoKeys.length; i++) {
        const todoItem = await redis.get(todoKeys[i])
        if (todoItem) {
            todos.push(JSON.parse(todoItem));
        }
    }

    if(req.query['slow']){
        await sleep(1000);
    }

    if(req.query['fail']){
        console.error('Really bad error!');
        res.sendStatus(500);
    }

    res.json({ todos, user:user.data });
})

app.listen(8080, () => {
    console.log('service is up and running!');
})


async function init() {
    await Promise.all([
        redis.set('todo:1', JSON.stringify({ name: 'Install OpenTelemetry SDK' })),
        redis.set('todo:2', JSON.stringify({ name: 'Deploy OpenTelemetry Collector' })),
        redis.set('todo:3', JSON.stringify({ name: 'Configure sampling rule' })),
        redis.set('todo:4', JSON.stringify({ name: 'You are OpenTelemetry master!' }))]
    );
}
init();