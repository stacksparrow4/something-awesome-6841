FROM node:18-alpine

WORKDIR /app

COPY site/package.json site/package-lock.json ./
RUN npm ci

COPY site/ ./

COPY ./discordbot/index.js /root/bot.js

EXPOSE 3000

CMD node .
