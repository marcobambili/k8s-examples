
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';


import { NodeSDK } from '@opentelemetry/sdk-node';
import { Resource } from '@opentelemetry/resources';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

import { SEMRESATTRS_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
import { resourceFromAttributes } from '@opentelemetry/resources';


function start(serviceName: string) {


  
// Configurazione OpenTelemetry
const metricExporter = new OTLPMetricExporter();
const metricReader = new PeriodicExportingMetricReader({
  exporter: metricExporter,
  exportIntervalMillis: 5000,
});

const meterProvider = new MeterProvider({
  readers: [metricReader],
});

const meter = meterProvider.getMeter('my-node-app');


//const resource = resourceFromAttributes({
 //   [SEMRESATTRS_SERVICE_NAME]: 'api-service',
//});
    
  
          
    const traceExporter = new OTLPTraceExporter({
        url: 'http://jaeger:4318/v1/traces',
    });

    const sdk = new NodeSDK({
        traceExporter,
        serviceName: serviceName,
        instrumentations: [getNodeAutoInstrumentations()],
        resource: resourceFromAttributes({
            [SEMRESATTRS_SERVICE_NAME]: 'api-service',
            'author': 'Marco Bambili',
        }),
        
    });


    sdk.start();

    return meter;
}

export default start