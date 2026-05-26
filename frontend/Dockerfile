FROM node:20-alpine
WORKDIR /app
ENV PATH=/app/node_modules/.bin:$PATH
COPY package*.json ./
# RUN npm ci
# After frontend and backend are merged together, we should use the above line
RUN npm install
COPY . .
ENV NODE_ENV=development
ENV CHOKIDAR_USEPOLLING=true
EXPOSE 5173
CMD ["npm", "run", "dev"]
