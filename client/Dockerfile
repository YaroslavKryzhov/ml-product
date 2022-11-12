FROM node:15.14.0-alpine as front-build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM nginx:1.16.0-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=front-build /app/build /usr/share/nginx/html
EXPOSE 80
COPY nginx.conf /etc/nginx/conf.d/think-client.conf