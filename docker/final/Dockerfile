# Step 1:
FROM node:16

# Step 2
WORKDIR /usr/src/app

# Step 3
RUN git clone http://github.com/happyrina/docker-publish
WORKDIR docker-publish/worldcup
RUN npm install

# Step 4
EXPOSE 8000

# Step 5
CMD ["node", "app.js"]
