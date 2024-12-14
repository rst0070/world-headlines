# Use the official Node.js image as the base image
FROM node:22.12-alpine

WORKDIR /app
COPY . .

# Set environment variables
ARG NODE_ENV
ARG BACKEND_API_URL
ENV NODE_ENV=${NODE_ENV}
ENV BACKEND_API_URL=${BACKEND_API_URL} 
# Build
RUN npm install
RUN npm run build
# Expose the port the app runs on
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]