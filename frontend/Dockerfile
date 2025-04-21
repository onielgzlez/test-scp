FROM node:lts-alpine

WORKDIR /app

# Instalar pnpm globalmente
RUN npm install -g pnpm

# Copiar solo los archivos esenciales antes de instalar dependencias
COPY package.json ./

# Instalar dependencias dentro del contenedor
RUN pnpm install --ignore-scripts

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto 3000
EXPOSE 3000

# Ejecutar la aplicación
CMD ["sh", "/app/entrypoint.sh"]