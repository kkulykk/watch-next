FROM node:16-alpine

WORKDIR /app

COPY . .

# Install dependencies.
RUN npm install

# Default port used by serve is 3000
EXPOSE 3000

# For now start the app in development mode
CMD [ "npm", "run", "serve" ]
