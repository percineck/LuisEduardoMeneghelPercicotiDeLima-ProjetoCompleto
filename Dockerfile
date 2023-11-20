FROM node:lts-bullseye-slim AS build
WORKDIR /app
COPY package.json ./
COPY . .
RUN npm install
RUN npm install -g @angular/cli
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist/LuisEduardoMeneghelPercicotiDeLima_Atividade-07 /usr/share/nginx/html
#docker build . -t agenda.image
#docker run -p 80:80 --network=bridge -e TZ=America/Sao_Paulo --restart=always --name agenda.container -d agenda.image