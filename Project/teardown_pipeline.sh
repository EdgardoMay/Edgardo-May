#!/bin/bash

set -e

echo "🧹 Apagando y limpiando el entorno ETL..."

# 1. Detener y eliminar contenedores
docker compose down --volumes --remove-orphans

# 2. Eliminar volúmenes persistentes manuales si quedaron activos
echo "🗑️ Eliminando volúmenes huérfanos (si existen)..."
docker volume rm $(docker volume ls -qf dangling=true) 2>/dev/null || true

# 3. Eliminar imágenes creadas (opcional)
# docker image prune -af

# 4. Confirmación
echo "✅ Entorno limpio. Puedes reconstruir con ./setup_pipeline.sh"
