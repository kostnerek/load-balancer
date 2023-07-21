# Use the official Node.js LTS (Long Term Support) image as the base image
FROM node:14-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install --only=development

# Copy the rest of the application source code to the container
COPY . .

# Expose the port that the Nest.js application is listening on
EXPOSE 3000

# Start the Nest.js application with nodemon for hot-reload
CMD ["npm", "run", "start:dev"]
