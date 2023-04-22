FROM node:16-alpine

WORKDIR /app

COPY . .

# Install dependencies.
RUN yarn install && yarn cache clean

# Default port used by serve is 3000
EXPOSE 3000

# For now start the app in development mode
CMD [ "yarn", "serve" ]
