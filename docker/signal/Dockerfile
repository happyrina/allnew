#Base Images
FROM iojs:onbuild 

#action
COPY ./sig_test.js ./sig_test.js
COPY ./package.json ./package.json

#port
EXPOSE 8000

#exec 
ENTRYPOINT ["node","sig_test"]
