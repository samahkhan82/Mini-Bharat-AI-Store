FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --silent || npm install
COPY . .
RUN npm run build
CMD ["npm","run","preview","--","--port","5173"]
