# Use an official Node runtime as a parent image
FROM node:14-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install all the dependencies
RUN npm install

# Pass in the API URL as a build arg
ARG REACT_APP_API_BASE_URL
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

# Copy all files in the current directory to our image
COPY . .

# Build the app
RUN npm run build

# Use a minimal alpine image to hold our compiled javascript code
FROM nginx:1.20-alpine

# Copy build files from builder
COPY --from=build /app/build /usr/share/nginx/html

# Copy the nginx.conf file, if it is in the same directory
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 in the container
EXPOSE 80

# Start the app
CMD ["nginx", "-g", "daemon off;"]