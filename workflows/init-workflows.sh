#!/bin/bash
set -e

echo "🚀 Starting n8n import workflows..."

# Check if we have workflow files to import
if [ -f "/home/node/.n8n/workflows/n8n_workflow.json" ]; then
  echo "📥 Importing workflow from /home/node/.n8n/workflows/n8n_workflow.json"
  n8n import:workflow --input=/home/node/.n8n/workflows/n8n_workflow.json
fi

# Importar credenciales si existen
if [ -f "/home/node/.n8n/workflows/auth.json" ]; then
  echo "🔑 Importing credentials from /home/node/.n8n/workflows/auth.json"
  n8n import:credentials --input=/home/node/.n8n/workflows/auth.json
fi

# Activate all workflows
echo "⚙️ Activating all workflows..."
n8n update:workflow --all --active=true

# Verificar the import
echo "🔍 Verifying imported workflows:"
n8n list:workflow

echo "✅ Importation of workflows completed successfully!"
echo "🔄 To apply changes, please restart n8n manually with:"
echo "docker-compose restart n8n"
