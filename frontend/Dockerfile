# Imagem base
FROM node:20-alpine

# Diretório de trabalho
WORKDIR /app

# Copiar package.json e instalar dependências
COPY package*.json ./
RUN npm install

# Copiar o restante do código
COPY . .

# Expor porta e rodar com hot reload
EXPOSE 5173
CMD ["npm", "run", "dev"]
