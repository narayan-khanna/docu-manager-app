FROM node:22

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Serve with static server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
