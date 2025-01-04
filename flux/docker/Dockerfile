# Utilizziamo l'immagine Node.js ufficiale come base
FROM node:16-alpine

# Impostiamo la working directory all'interno del container
WORKDIR /usr/src/app

# Copiamo il file package.json per installare le dipendenze
COPY package*.json ./

# Installiamo le dipendenze
RUN npm install

# Copiamo il resto del codice sorgente
COPY . .

# Esponiamo la porta 3000 per il nostro server
EXPOSE 3000

# Comandi da eseguire quando il container viene avviato
CMD [ "node", "index.js" ]