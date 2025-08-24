FROM node:20-alpine

WORKDIR /workspace/app/frontend

COPY app/frontend/package*.json ./
RUN npm ci

COPY app/frontend ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
