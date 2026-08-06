# Instalación VM - GeneXus Object Registry

Ubuntu Server 22.04.5 LTS

---

## 1. Actualizar los paquetes

```bash
sudo apt update
sudo apt upgrade -y
```

## 2. Instalar OpenSSH Server

```bash
sudo apt install openssh-server -y
```

## 3. Verificar SSH

```bash
systemctl status ssh
```

## 4. Activar SSH (si no está activo)

```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

## 5. Instalar Git

```bash
sudo apt install git -y
```

## 6. Instalar Python 3.11

```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

## 7. Instalar PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

## 8. Configurar PostgreSQL

```bash
cd /tmp
sudo -u postgres psql -c "CREATE USER gxuser WITH PASSWORD 'gxpassword';"
sudo -u postgres psql -c "CREATE DATABASE gx_object_registry OWNER gxuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxuser;"
```

## 9. Clonar repositorio

```bash
cd ~
git clone https://github.com/HenryG77/gx-object-registry.git
cd gx-object-registry
```

## 10. Crear entorno virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

## 11. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 12. Configurar archivo .env

Generar SECRET_KEY:
```bash
python3.11 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copiar y editar archivo .env:
```bash
cp .env.example .env
nano .env
```

Editar las siguientes variables:
```
DATABASE_URL=postgresql+asyncpg://gxuser:gxpassword@localhost:5432/gx_object_registry
APP_ENV=production
DEBUG=false
SECRET_KEY=CAMBIAR_ESTA_CLAVE_SECRETA
```

