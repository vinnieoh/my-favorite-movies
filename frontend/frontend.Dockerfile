# Base image
FROM node:18-alpine

# Set the working directory
WORKDIR /src

# Copy package.json and package-lock.json
COPY ./frontend/package.json ./frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the project files
COPY ./frontend .

# Build the Vite.js project
RUN npm run build

# Expose the port
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev"]
