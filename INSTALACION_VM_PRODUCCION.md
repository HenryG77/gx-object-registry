# Instalación Completa en Máquina Virtual - GeneXus Object Registry

**Guía paso a paso desde CERO hasta tener la aplicación corriendo en producción**

---

## Información del Documento

- **Versión**: 1.0
- **Fecha**: Agosto 2026
- **Sistema Host**: Windows 10/11
- **Sistema Guest**: Ubuntu Server 22.04.5 LTS
- **Virtualización**: Oracle VirtualBox
- **Audiencia**: Principiantes absolutos
- **Tiempo estimado total**: Según habilidad del usuario

---

## Tabla de Contenidos

### FASE 1: PREPARACIÓN DEL ENTORNO (Pasos 1-5)
1. [Descargar VirtualBox](#paso-1-descargar-virtualbox)
2. [Instalar VirtualBox](#paso-2-instalar-virtualbox)
3. [Descargar Ubuntu Server](#paso-3-descargar-ubuntu-server)
4. [Verificar Descarga](#paso-4-verificar-descarga)
5. [Preparar Configuración](#paso-5-preparar-configuración)

### FASE 2: CREACIÓN DE LA MÁQUINA VIRTUAL (Pasos 6-10)
6. [Crear Nueva Máquina Virtual](#paso-6-crear-nueva-máquina-virtual)
7. [Configurar Recursos](#paso-7-configurar-recursos)
8. [Configurar Red y Puertos](#paso-8-configurar-red-y-puertos)
9. [Montar ISO de Ubuntu](#paso-9-montar-iso-de-ubuntu)
10. [Revisar Configuración Final](#paso-10-revisar-configuración-final)

### FASE 3: INSTALACIÓN DE UBUNTU SERVER (Pasos 11-20)
11. [Iniciar Instalación](#paso-11-iniciar-instalación)
12. [Configurar Idioma y Teclado](#paso-12-configurar-idioma-y-teclado)
13. [Configurar Red](#paso-13-configurar-red)
14. [Configurar Almacenamiento](#paso-14-configurar-almacenamiento)
15. [Crear Usuario Inicial](#paso-15-crear-usuario-inicial)
16. [Instalar OpenSSH](#paso-16-instalar-openssh)
17. [Completar Instalación](#paso-17-completar-instalación)
18. [Primer Arranque](#paso-18-primer-arranque)
19. [Login Inicial](#paso-19-login-inicial)
20. [Actualización del Sistema](#paso-20-actualización-del-sistema)

### FASE 4: CONFIGURACIÓN INICIAL DEL SERVIDOR (Pasos 21-25)
21. [Conectarse por SSH desde Windows](#paso-21-conectarse-por-ssh-desde-windows)
22. [Instalar Herramientas Básicas](#paso-22-instalar-herramientas-básicas)
23. [Configurar Zona Horaria](#paso-23-configurar-zona-horaria)
24. [Configurar Hostname](#paso-24-configurar-hostname)
25. [Crear Snapshot de Seguridad](#paso-25-crear-snapshot-de-seguridad)

### FASE 5: INSTALACIÓN DE POSTGRESQL (Pasos 26-30)
26. [Instalar PostgreSQL](#paso-26-instalar-postgresql)
27. [Configurar PostgreSQL](#paso-27-configurar-postgresql)
28. [Crear Usuario y Base de Datos](#paso-28-crear-usuario-y-base-de-datos)
29. [Verificar Conexión](#paso-29-verificar-conexión)
30. [Snapshot Post-PostgreSQL](#paso-30-snapshot-post-postgresql)

### FASE 6: INSTALACIÓN DEL PROYECTO (Pasos 31-40)
31. [Instalar Python 3.11](#paso-31-instalar-python-311)
32. [Instalar Git](#paso-32-instalar-git)
33. [Clonar Repositorio](#paso-33-clonar-repositorio)
34. [Crear Entorno Virtual](#paso-34-crear-entorno-virtual)
35. [Instalar Dependencias](#paso-35-instalar-dependencias)
36. [Configurar Variables de Entorno](#paso-36-configurar-variables-de-entorno)
37. [Ejecutar Migraciones](#paso-37-ejecutar-migraciones)
38. [Cargar Datos Iniciales](#paso-38-cargar-datos-iniciales)
39. [Crear Usuario Administrador](#paso-39-crear-usuario-administrador)
40. [Probar Aplicación Manual](#paso-40-probar-aplicación-manual)

### FASE 7: CONFIGURACIÓN DE PRODUCCIÓN (Pasos 41-50)
41. [Instalar Gunicorn](#paso-41-instalar-gunicorn)
42. [Probar Gunicorn](#paso-42-probar-gunicorn)
43. [Crear Servicio Systemd](#paso-43-crear-servicio-systemd)
44. [Configurar Logs](#paso-44-configurar-logs)
45. [Iniciar Servicio](#paso-45-iniciar-servicio)
46. [Verificar Servicio](#paso-46-verificar-servicio)
47. [Instalar Nginx](#paso-47-instalar-nginx)
48. [Configurar Nginx](#paso-48-configurar-nginx)
49. [Configurar Firewall](#paso-49-configurar-firewall)
50. [Verificación Final](#paso-50-verificación-final)

### FASE 8: BACKUPS Y MANTENIMIENTO (Pasos 51-55)
51. [Configurar Backups](#paso-51-configurar-backups)
52. [Probar Backup](#paso-52-probar-backup)
53. [Automatizar Backups](#paso-53-automatizar-backups)
54. [Documentar Credenciales](#paso-54-documentar-credenciales)
55. [Snapshot Final](#paso-55-snapshot-final)

---

# FASE 1: PREPARACIÓN DEL ENTORNO

---

## Paso 1: Descargar VirtualBox

### Objetivo
Descargar el software de virtualización Oracle VirtualBox para Windows.

### Requisitos Previos
- Conexión a Internet
- Permisos de administrador en Windows
- Espacio en disco: ~200 MB para el instalador

### Procedimiento Detallado

#### 1.1 Abrir Navegador Web

Abre tu navegador preferido (Chrome, Firefox, Edge).

#### 1.2 Ir al Sitio Oficial

En la barra de direcciones, escribe:

```
https://www.virtualbox.org
```

Presiona **Enter**.

#### 1.3 Navegar a Descargas

En la página principal de VirtualBox:

1. Busca el menú de navegación (usualmente en la parte superior)
2. Haz clic en **"Downloads"** o **"Descargas"**

**Qué verás**: Página con diferentes versiones de VirtualBox.

#### 1.4 Seleccionar Versión para Windows

En la sección **"VirtualBox Platform Packages"**:

1. Identifica la versión más reciente (ejemplo: **VirtualBox 7.0.14**)
2. Busca la línea que dice **"Windows hosts"**
3. Haz clic en el enlace **"Windows hosts"**

**Qué sucede**: La descarga comenzará automáticamente.

**Nombre del archivo**:
```
VirtualBox-7.0.14-161095-Win.exe
```

(Los números pueden variar según la versión exacta)

#### 1.5 Guardar el Archivo

**Ubicación recomendada**:
```
C:\Users\TuUsuario\Downloads\
```

**Verifica que la descarga finalizó**:
1. Abre la carpeta de Descargas
2. Busca el archivo `VirtualBox-X.X.XX-XXXXXX-Win.exe`
3. Verifica el tamaño: ~100-120 MB

### Verificación

✅ **Archivo descargado**: VirtualBox-X.X.XX-Win.exe
✅ **Tamaño**: ~100-120 MB
✅ **Ubicación**: Carpeta de Descargas

### Solución de Problemas

**Problema**: La descarga es muy lenta.

**Solución**: Usa un servidor espejo alternativo. En la página de descargas, busca "Alternative download locations".

**Problema**: El antivirus bloquea la descarga.

**Solución**:
1. VirtualBox es software legítimo y seguro
2. Temporalmente deshabilita el antivirus
3. Descarga el archivo
4. Vuelve a habilitar el antivirus

---

## Paso 2: Instalar VirtualBox

### Objetivo
Instalar Oracle VirtualBox en Windows.

### Requisitos Previos
- ✅ VirtualBox descargado (Paso 1 completado)
- Permisos de administrador
- Espacio en disco: ~200 MB para la instalación

### Procedimiento Detallado

#### 2.1 Ejecutar Instalador

1. Ve a la carpeta de Descargas
2. Busca `VirtualBox-X.X.XX-Win.exe`
3. **Haz doble clic** en el archivo

**Qué sucede**: Aparecerá un cuadro de diálogo de Control de Cuentas de Usuario (UAC).

**Ventana UAC**:
```
¿Desea permitir que esta aplicación realice cambios en el dispositivo?
Editor verificado: Oracle Corporation
```

4. Haz clic en **"Sí"**

#### 2.2 Asistente de Instalación - Bienvenida

**Ventana**: "Welcome to the Oracle VM VirtualBox Setup Wizard"

**Qué hacer**: Haz clic en **"Next"** (Siguiente)

#### 2.3 Ubicación de Instalación

**Ventana**: "Custom Setup"

**Qué verás**:
```
Location: C:\Program Files\Oracle\VirtualBox\
```

**Componentes**:
- ✅ VirtualBox Application
- ✅ VirtualBox USB Support
- ✅ VirtualBox Networking
- ✅ VirtualBox Python Support

**Qué hacer**:
1. Deja todas las opciones marcadas
2. Deja la ubicación por defecto
3. Haz clic en **"Next"**

#### 2.4 Opciones Adicionales

**Ventana**: "Custom Setup - Options"

**Opciones**:
- ✅ Create a shortcut on the desktop (Crear acceso directo en escritorio)
- ✅ Create a shortcut in the Quick Launch Bar
- ✅ Register file associations (Registrar asociaciones de archivo)

**Qué hacer**:
1. Deja todas las opciones marcadas
2. Haz clic en **"Next"**

#### 2.5 Advertencia de Red

**Ventana**: "Warning: Network Interfaces"

**Mensaje**:
```
Installing the Oracle VM VirtualBox Networking feature will reset your network connection and temporarily disconnect you from the network.

Proceed with installation now?
```

**Qué significa**: Durante la instalación, se instalarán drivers de red virtuales. Tu conexión a Internet puede cortarse por unos segundos.

**Qué hacer**: Haz clic en **"Yes"** (Sí)

#### 2.6 Listo para Instalar

**Ventana**: "Ready to Install"

**Qué hacer**: Haz clic en **"Install"**

#### 2.7 Proceso de Instalación

**Qué verás**: Barra de progreso con mensajes como:

```
Installing VirtualBox Application...
Installing VirtualBox USB Support...
Installing VirtualBox Networking...
```

**Durante la instalación**:
- Pueden aparecer ventanas de instalación de drivers
- **MUY IMPORTANTE**: Si aparece alguna ventana preguntando "Install device software?", haz clic en **"Install"** o **"Instalar"**

**Drivers que pueden aparecer**:
- Oracle Corporation Universal Serial Bus controllers
- Oracle Corporation Network adapters
- Oracle Corporation System devices

**Para cada uno**: Haz clic en **"Install"** (Instalar)

#### 2.8 Finalización

**Ventana**: "Oracle VM VirtualBox Installation is complete"

**Opciones**:
- ☑️ Start Oracle VM VirtualBox after installation (Iniciar VirtualBox después de instalar)

**Qué hacer**:
1. Deja la opción marcada
2. Haz clic en **"Finish"**

**Qué sucede**: VirtualBox se abrirá automáticamente.

#### 2.9 Primera Vez que Abres VirtualBox

**Ventana principal de VirtualBox**:

**Qué verás**:
- Barra de menú superior: Archivo, Máquina, Ver, etc.
- Panel izquierdo: Lista de máquinas virtuales (vacía por ahora)
- Panel derecho: Detalles (vacío)
- Barra de herramientas: Botones de Nueva, Configuración, Iniciar

### Verificación

✅ **VirtualBox instalado correctamente**
✅ **Ventana principal de VirtualBox abierta**
✅ **Drivers de red instalados**
✅ **Sin errores durante la instalación**

### Información Importante

**Versión instalada**: Anota la versión. Ejemplo: `7.0.14 r161095`

**Ubicación**:
```
C:\Program Files\Oracle\VirtualBox\
```

### Solución de Problemas

**Problema**: "Installation failed" durante la instalación.

**Solución**:
1. Desinstala cualquier versión anterior de VirtualBox
2. Reinicia Windows
3. Deshabilita temporalmente el antivirus
4. Vuelve a instalar

**Problema**: Los drivers de red no se instalan.

**Solución**:
1. Abre Administrador de dispositivos
2. Busca dispositivos con signo de exclamación amarillo
3. Haz clic derecho → Actualizar controlador
4. Selecciona "Buscar controladores en mi equipo"
5. Navega a: `C:\Program Files\Oracle\VirtualBox\drivers\network\netlwf\`

---

## Paso 3: Descargar Ubuntu Server

### Objetivo
Descargar la imagen ISO de Ubuntu Server 22.04.5 LTS.

### Requisitos Previos
- Conexión a Internet
- Espacio en disco: ~2.5 GB

### Procedimiento Detallado

#### 3.1 Abrir Sitio Oficial de Ubuntu

En tu navegador, ve a:

```
https://ubuntu.com/download/server
```

#### 3.2 Localizar la Versión Correcta

**En la página**:

**Qué verás**:
- Título grande: "Download Ubuntu Server"
- Subtítulo con la versión: "Ubuntu Server 22.04.5 LTS"

**Información mostrada**:
```
Ubuntu Server 22.04.5 LTS
Released: August 2024
Supported until: April 2027
```

#### 3.3 Descargar la Imagen ISO

**Busca el botón verde grande** que dice:

```
Download Ubuntu Server 22.04.5 LTS
```

**Haz clic en el botón**.

**Qué sucede**:
1. Puede aparecer una página intermedia pidiendo información (opcional)
2. Si aparece, puedes hacer clic en "Not now, take me to the download"
3. La descarga comenzará

**Nombre del archivo**:
```
ubuntu-22.04.5-live-server-amd64.iso
```

**Tamaño aproximado**: 2.5 GB

#### 3.4 Esperar a que Termine la Descarga

**Tiempo estimado**:
- Conexión rápida (50 Mbps): 5-10 minutos
- Conexión media (10 Mbps): 30-40 minutos
- Conexión lenta (2 Mbps): 2-3 horas

**Ubicación**:
```
C:\Users\TuUsuario\Downloads\ubuntu-22.04.5-live-server-amd64.iso
```

### Verificación

✅ **Archivo descargado**: ubuntu-22.04.5-live-server-amd64.iso
✅ **Tamaño**: ~2.5 GB (2,500,000,000 bytes aproximadamente)
✅ **Extensión**: .iso

### Solución de Problemas

**Problema**: La descarga se interrumpe.

**Solución**:
1. Usa un gestor de descargas (Free Download Manager, Internet Download Manager)
2. O usa `wget` desde PowerShell:

```powershell
# Abre PowerShell
cd C:\Users\TuUsuario\Downloads

# Descarga con wget (si está instalado)
wget https://releases.ubuntu.com/22.04.5/ubuntu-22.04.5-live-server-amd64.iso
```

**Problema**: El archivo está corrupto.

**Solución**: Verifica el checksum (siguiente paso).

---

## Paso 4: Verificar Descarga

### Objetivo
Verificar que la imagen ISO se descargó correctamente.

### Procedimiento Detallado

#### 4.1 Verificar Tamaño del Archivo

1. Abre la carpeta de Descargas
2. Haz clic derecho en `ubuntu-22.04.5-live-server-amd64.iso`
3. Selecciona **"Propiedades"**

**Qué verás**:
```
Tamaño: 2.50 GB (2,500,000,000 bytes)
```

(El tamaño exacto puede variar ligeramente)

**Si el tamaño es muy diferente** (por ejemplo, solo 500 MB), la descarga está incompleta. Vuelve a descargar.

#### 4.2 Verificar Checksum (Opcional pero Recomendado)

**Qué es un checksum**: Un código único que verifica que el archivo no está corrupto.

**Obtener el checksum oficial**:

1. Ve a: https://releases.ubuntu.com/22.04.5/SHA256SUMS
2. Busca la línea que menciona `ubuntu-22.04.5-live-server-amd64.iso`
3. Copia el código SHA256 (64 caracteres hexadecimales)

**Ejemplo**:
```
9bc6028870aef3f74f4e16b900008179e78b130e6b0b9a140635434a46aa98b0 *ubuntu-22.04.5-live-server-amd64.iso
```

**Verificar en Windows**:

Abre PowerShell:

```powershell
cd C:\Users\TuUsuario\Downloads

Get-FileHash ubuntu-22.04.5-live-server-amd64.iso -Algorithm SHA256
```

**Salida esperada**:
```
Algorithm       Hash
---------       ----
SHA256          9BC6028870AEF3F74F4E16B900008179E78B130E6B0B9A140635434A46AA98B0
```

**Compara** el hash con el oficial. **Si coinciden**, el archivo está correcto.

### Verificación

✅ **Tamaño correcto**: ~2.5 GB
✅ **Checksum coincide** (si lo verificaste)
✅ **Extensión**: .iso
✅ **Nombre completo**: ubuntu-22.04.5-live-server-amd64.iso

---

## Paso 5: Preparar Configuración

### Objetivo
Documentar la configuración que usaremos para la VM.

### Configuración de la Máquina Virtual

Anota esta información para los siguientes pasos:

#### Configuración General

| Parámetro | Valor |
|-----------|-------|
| **Nombre de la VM** | `GX-Registry-Production` |
| **Tipo** | Linux |
| **Versión** | Ubuntu (64-bit) |

#### Recursos de Hardware

| Recurso | Mínimo | Recomendado | Tu Elección |
|---------|--------|-------------|-------------|
| **RAM** | 2048 MB (2 GB) | 4096 MB (4 GB) | ________ MB |
| **CPUs** | 2 | 2-4 | ________ |
| **Disco Duro** | 20 GB | 30 GB | ________ GB |

**Cómo decidir**:

**RAM**:
- Si tu PC tiene 8 GB → Elige 2048 MB
- Si tu PC tiene 16 GB → Elige 4096 MB
- Si tu PC tiene 32 GB → Elige 4096 o 8192 MB

**CPUs**:
- Si tu PC tiene 2 cores → Elige 2
- Si tu PC tiene 4 cores → Elige 2
- Si tu PC tiene 6+ cores → Elige 4

**Disco**:
- Para pruebas → 20 GB
- Para uso real → 30 GB

#### Reenvío de Puertos

| Nombre | Protocolo | Puerto Host | Puerto Guest |
|--------|-----------|-------------|--------------|
| SSH | TCP | 2222 | 22 |
| HTTP | TCP | 8080 | 80 |
| HTTPS | TCP | 8443 | 443 |
| App | TCP | 8000 | 8000 |

**Qué significa**:
- Desde Windows accederás a `localhost:8080` y se conectará al puerto 80 de Ubuntu
- SSH: `ssh -p 2222 gxapp@localhost` se conectará al puerto 22 de Ubuntu

#### Credenciales que Crearás

| Elemento | Valor Sugerido | Tu Valor |
|----------|----------------|----------|
| **Hostname** | gxregistry | ____________ |
| **Usuario** | gxapp | ____________ |
| **Contraseña Usuario** | (segura) | ____________ |
| **Nombre Completo** | GX Administrator | ____________ |

**⚠️ IMPORTANTE**: Anota estas contraseñas en un lugar seguro.

### Preparación Completada

✅ Configuración documentada
✅ Decisiones tomadas sobre recursos
✅ Contraseñas preparadas (no las olvides)

---

# FASE 2: CREACIÓN DE LA MÁQUINA VIRTUAL

---

## Paso 6: Crear Nueva Máquina Virtual

### Objetivo
Crear una nueva máquina virtual en VirtualBox con la configuración básica.

### Procedimiento Detallado

#### 6.1 Abrir VirtualBox

1. Haz doble clic en el icono de **VirtualBox** en el escritorio
2. O búscalo en el menú Inicio: Escribe "VirtualBox" y abre "Oracle VM VirtualBox"

**Ventana principal**: Deberías ver la interfaz de VirtualBox vacía (sin VMs).

#### 6.2 Iniciar Asistente de Nueva VM

**Hay dos formas**:

**Opción A**: Haz clic en el botón **"Nueva"** (icono de estrella azul) en la barra de herramientas.

**Opción B**: Menú → **Máquina** → **Nueva**

**Atajo de teclado**: `Ctrl + N`

**Qué sucede**: Se abre el asistente "Crear máquina virtual".

#### 6.3 Configurar Nombre y Sistema Operativo

**Ventana**: "Name and Operating System"

**Campos a completar**:

**Nombre**:
```
GX-Registry-Production
```

**Carpeta de la máquina** (Machine Folder):
```
C:\Users\TuUsuario\VirtualBox VMs\
```
(Dejar por defecto)

**Tipo** (Type):
- Selecciona: **Linux**

**Versión** (Version):
- Despliega el menú
- Busca y selecciona: **Ubuntu (64-bit)**

**⚠️ MUY IMPORTANTE**:
- Si NO ves opciones de 64-bit, SOLO opciones de 32-bit
- Significa que la virtualización está deshabilitada en tu BIOS
- Ver sección de "Solución de Problemas" al final de este paso

**Qué hacer**: Haz clic en **"Siguiente"** (Next)

#### 6.4 Configurar Memoria RAM

**Ventana**: "Memory Size"

**Qué verás**:
- Un slider (barra deslizante)
- Área verde (recomendado)
- Área roja (no usar)
- Valor en MB

**Configurar RAM**:

1. Arrastra el slider O escribe directamente en el cuadro
2. Valor recomendado: **2048 MB** (2 GB) o **4096 MB** (4 GB)

**Regla**:
```
RAM de la VM ≤ 50% de tu RAM total
```

**Ejemplo**:
- Tu PC tiene 8 GB (8192 MB) → Máximo para VM: 4096 MB
- Tu PC tiene 16 GB (16384 MB) → Máximo para VM: 8192 MB

**Para este proyecto**:
- Mínimo: 2048 MB
- Recomendado: 4096 MB

3. Ingresa **4096** (si tu PC lo permite)
4. Haz clic en **"Siguiente"**

#### 6.5 Crear Disco Duro Virtual

**Ventana**: "Hard Disk"

**Opciones**:
- ⚫ Do not add a virtual hard disk (No agregar)
- ⚫ Create a virtual hard disk now (Crear ahora) ← **Selecciona esta**
- ⚫ Use an existing virtual hard disk file (Usar existente)

**Qué hacer**:
1. Selecciona **"Create a virtual hard disk now"**
2. Haz clic en **"Create"** (Crear)

#### 6.6 Tipo de Archivo de Disco

**Ventana**: "Hard Disk File Type"

**Opciones**:
- ⚫ VDI (VirtualBox Disk Image) ← **Selecciona esta**
- ⚫ VHD (Virtual Hard Disk)
- ⚫ VMDK (Virtual Machine Disk)

**Qué significa**:
- **VDI**: Formato nativo de VirtualBox (recomendado)
- **VHD**: Formato de Microsoft Hyper-V
- **VMDK**: Formato de VMware

**Qué hacer**:
1. Selecciona **"VDI"**
2. Haz clic en **"Siguiente"**

#### 6.7 Almacenamiento en Disco Físico

**Ventana**: "Storage on Physical Hard Disk"

**Opciones**:
- ⚫ Dynamically allocated (Reservado dinámicamente) ← **Selecciona esta**
- ⚫ Fixed size (Tamaño fijo)

**Diferencia**:

**Dynamically allocated** (Recomendado):
- El archivo .vdi crece según se usa
- Si creas disco de 30 GB pero solo usas 10 GB, el archivo ocupará ~10 GB
- Más eficiente en espacio

**Fixed size**:
- El archivo .vdi se crea del tamaño completo inmediatamente
- Si creas disco de 30 GB, el archivo será de 30 GB desde el inicio
- Ligeramente más rápido en performance

**Para este proyecto**: Usa **"Dynamically allocated"**

**Qué hacer**:
1. Selecciona **"Dynamically allocated"**
2. Haz clic en **"Siguiente"**

#### 6.8 Ubicación y Tamaño del Archivo

**Ventana**: "File Location and Size"

**Nombre del archivo**:
```
GX-Registry-Production
```
(Ya aparece automáticamente)

**Ubicación**:
```
C:\Users\TuUsuario\VirtualBox VMs\GX-Registry-Production\
```

**Tamaño del disco**:

**Qué verás**: Un slider y un cuadro de texto

**Configurar**:
1. Escribe: **30** (30 GB)
2. O arrastra el slider hasta 30.00 GB

**Mínimo**: 20 GB
**Recomendado**: 30 GB

**Qué hacer**:
1. Establece **30 GB**
2. Haz clic en **"Crear"**

#### 6.9 VM Creada

**Qué sucede**:
- La ventana del asistente se cierra
- Regresas a la ventana principal de VirtualBox
- En el panel izquierdo aparece: **"GX-Registry-Production"**

**Estado**: Apagada (Powered Off)

### Verificación

✅ **VM aparece en la lista**
✅ **Nombre**: GX-Registry-Production
✅ **Tipo**: Linux, Ubuntu (64-bit)
✅ **RAM**: 2048 o 4096 MB
✅ **Disco**: 30 GB
✅ **Estado**: Apagada

### Información de la VM

**Haz clic en la VM en el panel izquierdo**.

**Panel derecho muestra**:
```
General
  Name: GX-Registry-Production
  Operating System: Ubuntu (64-bit)

System
  Base Memory: 4096 MB
  Processor(s): 1
  Boot Order: Floppy, Optical, Hard Disk

Display
  Video Memory: 16 MB

Storage
  Controller: IDE
    GX-Registry-Production.vdi (30.00 GB)
```

### Solución de Problemas

**Problema**: Solo aparecen opciones de 32-bit, no 64-bit.

**Causa**: Virtualización de hardware deshabilitada en BIOS.

**Solución**:

1. **Reinicia tu PC**
2. **Entra al BIOS/UEFI**:
   - Presiona `Del`, `F2`, `F10`, o `F12` al iniciar (depende del fabricante)
   - Puede decir "Press F2 to enter Setup"
3. **Busca opciones de Virtualización**:
   - Puede llamarse: `Intel VT-x`, `AMD-V`, `Virtualization Technology`, `SVM Mode`
   - Usualmente en: Advanced → CPU Configuration
4. **Habilita la opción**: Cambia a `Enabled`
5. **Guarda y sal**: `F10` → Yes
6. **Reinicia Windows**
7. **Abre VirtualBox nuevamente**
8. Ahora deberías ver opciones de 64-bit

**Problema**: "VT-x is not available" al crear VM.

**Solución**: Igual que arriba (habilitar virtualización en BIOS).

**Problema**: Error "Cannot create machine folder".

**Solución**:
1. Asegúrate de tener permisos de escritura en `C:\Users\TuUsuario\`
2. O cambia la ubicación a otra carpeta (ejemplo: `D:\VirtualBox VMs\`)

---

## Paso 7: Configurar Recursos

### Objetivo
Ajustar la configuración de CPU, RAM y otros recursos de la VM.

### Procedimiento Detallado

#### 7.1 Abrir Configuración de la VM

**Asegúrate de que la VM esté seleccionada** (haz clic en "GX-Registry-Production" en el panel izquierdo).

**Abrir configuración**:

**Opción A**: Haz clic en el botón **"Configuración"** (icono de engranaje) en la barra de herramientas.

**Opción B**: Clic derecho en la VM → **"Configuración"**

**Opción C**: Menú → **Máquina** → **Configuración**

**Atajo**: `Ctrl + S`

**Qué sucede**: Se abre la ventana "Configuración - GX-Registry-Production".

#### 7.2 Configurar Sistema - Placa Base

**En el panel izquierdo**:
1. Haz clic en **"Sistema"** (System)

**Pestaña**: "Placa base" (Motherboard) - debería estar activa

**Configuraciones**:

**Memoria base** (Base Memory):
- Ya está configurada (2048 o 4096 MB)
- No cambiar

**Orden de arranque** (Boot Order):
- ✅ Disquete (Floppy) - puedes desmarcarlo
- ✅ Óptica (Optical) - **IMPORTANTE**: dejar marcado
- ✅ Disco duro (Hard Disk) - dejar marcado
- ☐ Red (Network) - dejar desmarcado

**Orden correcto**:
1. Óptica (Optical)
2. Disco duro (Hard Disk)

**Chipset**: PIIX3 (dejar por defecto)

**Dispositivo apuntador** (Pointing Device): PS/2 Mouse (dejar por defecto)

**Características extendidas**:
- ☑️ Habilitar I/O APIC (dejar marcado)
- ☐ Habilitar EFI (dejar desmarcado)
- ☑️ Reloj hardware en hora UTC (marcar si no está)

#### 7.3 Configurar Sistema - Procesador

**En la misma ventana**:
1. Haz clic en la pestaña **"Procesador"** (Processor)

**Configuraciones**:

**Procesador(es)** (Processor(s)):

**Qué verás**: Un slider

**Configurar**:
- Si tu PC tiene 2 cores: Elige **2**
- Si tu PC tiene 4 cores: Elige **2**
- Si tu PC tiene 6+ cores: Elige **4**

**Para verificar cuántos cores tienes**:
1. Abre Administrador de Tareas (Ctrl+Shift+Esc)
2. Ve a Rendimiento → CPU
3. Busca "Núcleos" o "Cores"

**Límite de ejecución** (Execution Cap):
- Dejar en **100%**

**Características extendidas**:
- ☑️ Habilitar PAE/NX (marcar)
- ☐ Habilitar VT-x/AMD-V anidado (dejar desmarcado)

**Configuración recomendada**:
```
Procesadores: 2
Límite de ejecución: 100%
Habilitar PAE/NX: ✓
```

#### 7.4 Configurar Pantalla

**En el panel izquierdo**:
1. Haz clic en **"Pantalla"** (Display)

**Pestaña**: "Pantalla" (Screen)

**Configuraciones**:

**Memoria de vídeo** (Video Memory):
- Establecer: **16 MB** (mínimo, suficiente para servidor sin GUI)

**Monitor Count**: 1 (dejar por defecto)

**Factor de escala**: 100% (dejar por defecto)

**Aceleración gráfica**:
- ☐ Habilitar aceleración 3D (dejar desmarcado para servidor)
- ☐ Habilitar aceleración 2D (dejar desmarcado)

**Controlador gráfico**:
- Seleccionar: **VMSVGA** (recomendado para Linux)

#### 7.5 Configurar Almacenamiento (Preparar para ISO)

**En el panel izquierdo**:
1. Haz clic en **"Almacenamiento"** (Storage)

**Qué verás**:

**Árbol de almacenamiento**:
```
Controlador: IDE
  └─ Vacío (Empty)

Controlador: SATA
  └─ GX-Registry-Production.vdi
```

**Preparación**: Dejaremos esto como está por ahora. En el Paso 9 montaremos el ISO de Ubuntu.

### Verificación Parcial

✅ **RAM**: 2048 o 4096 MB
✅ **CPUs**: 2 o 4
✅ **PAE/NX habilitado**
✅ **Orden de arranque**: Óptica primero, luego disco duro
✅ **Memoria de vídeo**: 16 MB

**NO cierres** la ventana de configuración todavía. Continuamos con la red.

---

## Paso 8: Configurar Red y Puertos

### Objetivo
Configurar la red de la VM para poder acceder a la aplicación desde tu navegador Windows.

### Conceptos Importantes

#### ¿Qué es NAT?

**NAT (Network Address Translation)** es un modo de red donde:
- La VM está en una red privada
- Puede acceder a Internet a través de tu PC Windows
- Tu PC Windows puede acceder a la VM mediante **reenvío de puertos** (port forwarding)

#### ¿Por qué NAT?

**Ventajas para este proyecto**:
- ✅ Simple de configurar
- ✅ La VM tiene Internet automáticamente
- ✅ Tu PC Windows puede acceder a la VM
- ✅ La VM está protegida (no expuesta directamente a Internet)
- ✅ No requiere configuración de router

#### ¿Cómo funciona el Reenvío de Puertos?

**Ejemplo práctico**:

```
Tu navegador Windows → http://localhost:8080
           ↓
    VirtualBox NAT
           ↓
Puerto 8080 de Windows → Puerto 80 de Ubuntu
           ↓
    Nginx en Ubuntu escuchando en puerto 80
           ↓
    Tu aplicación GeneXus Registry
```

**En resumen**:
- Abres `http://localhost:8080` en Windows
- VirtualBox redirige a puerto 80 dentro de Ubuntu
- Nginx sirve la aplicación
- ¡Funciona como si fuera un servidor real!

### Procedimiento Detallado

#### 8.1 Abrir Configuración de Red

**Deberías estar todavía en la ventana de Configuración de la VM**.

**En el panel izquierdo**:
1. Haz clic en **"Red"** (Network)

**Qué verás**: 4 pestañas de adaptadores (Adapter 1, 2, 3, 4)

#### 8.2 Configurar Adaptador 1

**Pestaña**: "Adaptador 1" (Adapter 1) - debería estar activa

**Habilitar adaptador**:
- ✅ **Habilitar adaptador de red** (Enable Network Adapter) - debe estar marcado

**Conectado a** (Attached to):
- Despliega el menú
- Selecciona: **NAT**

**Qué verás después de seleccionar NAT**:
```
Conectado a: NAT
Nombre: No aplica para NAT
```

**Configuraciones avanzadas**:

Haz clic en **"Avanzadas"** (Advanced) para expandir:

**Tipo de adaptador** (Adapter Type):
- Selecciona: **Intel PRO/1000 MT Desktop (82540EM)** (recomendado)

**Modo promiscuo** (Promiscuous Mode):
- Dejar en: **Denegar** (Deny)

**Dirección MAC**:
- Dejar como está (generada automáticamente)

**Cable conectado** (Cable Connected):
- ✅ Debe estar marcado

#### 8.3 Configurar Reenvío de Puertos (MUY IMPORTANTE)

**Todavía en Adaptador 1 → Avanzadas**:

1. Haz clic en el botón **"Reenvío de puertos"** (Port Forwarding)

**Qué sucede**: Se abre una ventana "Reglas de reenvío de puertos".

**Qué verás**: Una tabla vacía con columnas:
- Nombre (Name)
- Protocolo (Protocol)
- IP anfitrión (Host IP)
- Puerto anfitrión (Host Port)
- IP invitado (Guest IP)
- Puerto invitado (Guest Port)

#### 8.4 Agregar Regla para SSH

**Propósito**: Conectarte desde Windows a Ubuntu mediante SSH.

1. Haz clic en el botón **"+"** (Agregar nueva regla) en el lado derecho

**Aparece una nueva fila**. Completa así:

| Campo | Valor |
|-------|-------|
| **Nombre** | `SSH` |
| **Protocolo** | `TCP` |
| **IP anfitrión** | `127.0.0.1` |
| **Puerto anfitrión** | `2222` |
| **IP invitado** | (dejar vacío) |
| **Puerto invitado** | `22` |

**Cómo llenar cada campo**:

1. **Nombre**: Haz clic en la celda, escribe: `SSH`
2. **Protocolo**: Despliega menú, selecciona: `TCP`
3. **IP anfitrión**: Escribe: `127.0.0.1`
4. **Puerto anfitrión**: Escribe: `2222`
5. **IP invitado**: Dejar vacío
6. **Puerto invitado**: Escribe: `22`

**Qué significa**:
- Cuando te conectes a `localhost:2222` desde Windows
- Se redirigirá al puerto `22` (SSH) dentro de Ubuntu

#### 8.5 Agregar Regla para HTTP

**Propósito**: Acceder a la aplicación web (Nginx puerto 80).

1. Haz clic nuevamente en **"+"**

**Nueva fila**:

| Campo | Valor |
|-------|-------|
| **Nombre** | `HTTP` |
| **Protocolo** | `TCP` |
| **IP anfitrión** | `127.0.0.1` |
| **Puerto anfitrión** | `8080` |
| **IP invitado** | (vacío) |
| **Puerto invitado** | `80` |

**Qué significa**:
- `http://localhost:8080` en Windows → Puerto 80 en Ubuntu (Nginx)

#### 8.6 Agregar Regla para HTTPS

**Propósito**: Acceder a la aplicación con SSL (si configuras HTTPS).

1. Haz clic en **"+"**

**Nueva fila**:

| Campo | Valor |
|-------|-------|
| **Nombre** | `HTTPS` |
| **Protocolo** | `TCP` |
| **IP anfitrión** | `127.0.0.1` |
| **Puerto anfitrión** | `8443` |
| **IP invitado** | (vacío) |
| **Puerto invitado** | `443` |

**Qué significa**:
- `https://localhost:8443` en Windows → Puerto 443 en Ubuntu (Nginx SSL)

#### 8.7 Agregar Regla para App Directa

**Propósito**: Acceder directamente al puerto de la aplicación (útil para pruebas).

1. Haz clic en **"+"**

**Nueva fila**:

| Campo | Valor |
|-------|-------|
| **Nombre** | `App` |
| **Protocolo** | `TCP` |
| **IP anfitrión** | `127.0.0.1` |
| **Puerto anfitrión** | `8000` |
| **IP invitado** | (vacío) |
| **Puerto invitado** | `8000` |

**Qué significa**:
- `http://localhost:8000` en Windows → Puerto 8000 en Ubuntu (Uvicorn/Gunicorn)

#### 8.8 Verificar Todas las Reglas

**Tu tabla de reenvío de puertos debe verse así**:

| Nombre | Protocolo | IP anfitrión | Puerto anfitrión | IP invitado | Puerto invitado |
|--------|-----------|--------------|------------------|-------------|-----------------|
| SSH | TCP | 127.0.0.1 | 2222 | | 22 |
| HTTP | TCP | 127.0.0.1 | 8080 | | 80 |
| HTTPS | TCP | 127.0.0.1 | 8443 | | 443 |
| App | TCP | 127.0.0.1 | 8000 | | 8000 |

**Si todo está correcto**:
1. Haz clic en **"Aceptar"** (OK) en la ventana de Reenvío de puertos

**Regresas a la ventana de Configuración de Red**.

#### 8.9 Verificar Configuración de Red

**En Adaptador 1 debes ver**:
```
☑️ Habilitar adaptador de red
Conectado a: NAT
Tipo de adaptador: Intel PRO/1000 MT Desktop (82540EM)
☑️ Cable conectado
```

### Verificación

✅ **Adaptador de red habilitado**
✅ **Modo**: NAT
✅ **4 reglas de reenvío de puertos creadas**
✅ **SSH**: 2222 → 22
✅ **HTTP**: 8080 → 80
✅ **HTTPS**: 8443 → 443
✅ **App**: 8000 → 8000

### Cómo Usarás Estas Configuraciones

**Desde Windows, podrás**:

**Conectarte por SSH**:
```powershell
ssh -p 2222 gxapp@localhost
```

**Acceder a la aplicación web**:
```
http://localhost:8080      (Nginx puerto 80)
https://localhost:8443     (Nginx HTTPS puerto 443)
http://localhost:8000      (App directa puerto 8000)
```

**Acceder a la documentación API**:
```
http://localhost:8080/docs
```

### Alternativa: Adaptador Puente (Bridge)

**Si prefieres que la VM tenga IP en tu red local**:

**Ventajas**:
- La VM tiene IP propia (ejemplo: 192.168.1.100)
- Puedes acceder desde otros dispositivos en tu red
- No necesitas port forwarding

**Desventajas**:
- Más complejo de configurar
- Requiere que tu router asigne IP por DHCP
- Menos seguro (VM expuesta en red local)

**Para este tutorial usaremos NAT** (más simple y seguro).

### Solución de Problemas

**Problema**: "Port 2222 is already in use"

**Causa**: Otro programa está usando el puerto.

**Solución**: Cambia el puerto de Windows:
- SSH: Usa 2223 en lugar de 2222
- HTTP: Usa 8081 en lugar de 8080

**Problema**: No puedo conectarme después desde Windows.

**Causa posible**:
1. Firewall de Windows bloqueando
2. Servicio no corriendo en Ubuntu

**Solución**: Verificaremos esto en pasos posteriores.

**NO cierres** la ventana de configuración. Continuamos con montar el ISO.

---

## Paso 9: Montar ISO de Ubuntu

### Objetivo
Montar la imagen ISO de Ubuntu Server en la unidad óptica virtual para poder instalar.

### Procedimiento Detallado

#### 9.1 Ir a Almacenamiento

**Deberías estar todavía en la ventana de Configuración**.

**En el panel izquierdo**:
1. Haz clic en **"Almacenamiento"** (Storage)

#### 9.2 Seleccionar Unidad Óptica Vacía

**Qué verás**: Árbol de dispositivos de almacenamiento:

```
Controlador: IDE
  └─ 🔵 Vacío (o "Empty")

Controlador: SATA
  └─ 💾 GX-Registry-Production.vdi
```

**En el árbol**:
1. Haz clic en **"Vacío"** (Empty) que está debajo de "Controlador: IDE"

**Qué sucede**: Se selecciona la unidad óptica virtual.

#### 9.3 Panel de Atributos

**A la derecha verás**: Panel "Atributos"

**Campos**:
```
Unidad óptica: [IDE Secundario Maestro]

  [icono de disco] ▼
```

**Qué verás**: Un icono de disco con una flecha desplegable.

#### 9.4 Seleccionar Archivo ISO

**Haz clic en el icono de disco** (pequeño CD azul con flecha) a la derecha de "IDE Secundario Maestro".

**Aparece un menú desplegable**:
```
⚪ Unidad de anfitrión 'D:\' (si tienes unidad física)
⚪ Vacío
──────────────────
📁 Elegir un archivo de disco...
```

1. Haz clic en **"Elegir un archivo de disco..."** (Choose disk file...)

**Qué sucede**: Se abre un explorador de archivos.

#### 9.5 Navegar al ISO

**En el explorador**:

1. Navega a: `C:\Users\TuUsuario\Downloads\`
2. Busca el archivo: `ubuntu-22.04.5-live-server-amd64.iso`
3. **Haz clic en el archivo para seleccionarlo**
4. Haz clic en **"Abrir"** (Open)

**Qué sucede**: El explorador se cierra y regresas a la ventana de Configuración.

#### 9.6 Verificar ISO Montado

**En el árbol de almacenamiento ahora verás**:

```
Controlador: IDE
  └─ 🔵 ubuntu-22.04.5-live-server-amd64.iso

Controlador: SATA
  └─ 💾 GX-Registry-Production.vdi
```

**En el panel de Atributos verás**:
```
Unidad óptica: IDE Secundario Maestro
  📀 ubuntu-22.04.5-live-server-amd64.iso

Información:
  Tamaño: 2.5 GB
  Ubicación: C:\Users\...\Downloads\ubuntu-22.04.5-live-server-amd64.iso
```

**Opción adicional**:
- ☑️ **Conectado en vivo** (Live CD/DVD) - debe estar marcado

### Verificación

✅ **ISO montado**: ubuntu-22.04.5-live-server-amd64.iso
✅ **Ubicación**: Controlador IDE
✅ **Tamaño**: 2.5 GB
✅ **Conectado en vivo**: Marcado

### ¿Qué Pasará al Iniciar la VM?

**Secuencia de arranque**:
1. La VM inicia
2. Lee el orden de arranque (Óptica primero)
3. Encuentra el ISO de Ubuntu
4. Arranca desde el ISO
5. Inicia el instalador de Ubuntu

**Después de instalar Ubuntu**:
- La VM arrancará desde el disco duro (GX-Registry-Production.vdi)
- Podrás expulsar el ISO (ya no será necesario)

---

## Paso 10: Revisar Configuración Final

### Objetivo
Revisar toda la configuración antes de iniciar la instalación.

### Procedimiento Detallado

#### 10.1 Revisar Resumen

**En la ventana de Configuración**:

**Panel izquierdo**, revisa cada sección:

**General**:
- Nombre: `GX-Registry-Production`
- Sistema operativo: Ubuntu (64-bit)

**Sistema**:
- RAM: 2048 o 4096 MB
- CPUs: 2 o 4
- PAE/NX: Habilitado
- Orden de arranque: Óptica, Disco duro

**Pantalla**:
- Memoria de vídeo: 16 MB
- Controlador: VMSVGA

**Almacenamiento**:
- IDE: ubuntu-22.04.5-live-server-amd64.iso
- SATA: GX-Registry-Production.vdi (30 GB)

**Red**:
- Adaptador 1: NAT
- Reenvío de puertos: 4 reglas configuradas

#### 10.2 Aplicar Configuración

**En la ventana de Configuración**:

1. Haz clic en **"Aceptar"** (OK) en la parte inferior

**Qué sucede**: La ventana de configuración se cierra y regresas a la ventana principal de VirtualBox.

#### 10.3 Verificar en Panel de Detalles

**En la ventana principal de VirtualBox**:

**Asegúrate de que** "GX-Registry-Production" **esté seleccionada** en el panel izquierdo.

**Panel derecho (Detalles) muestra**:
```
General
  Name: GX-Registry-Production
  Operating System: Ubuntu (64-bit)

System
  Base Memory: 4096 MB
  Processor(s): 2
  Boot Order: Optical, Hard Disk
  Acceleration: VT-x/AMD-V, Nested Paging

Display
  Video Memory: 16 MB
  Graphics Controller: VMSVGA

Storage
  ubuntu-22.04.5-live-server-amd64.iso (IDE)
  GX-Registry-Production.vdi (30.00 GB, SATA)

Audio
  Disabled

Network
  Adapter 1: NAT

USB
  Disabled
```

### Checklist de Pre-Instalación

```
✅ VirtualBox instalado
✅ Ubuntu Server 22.04.5 ISO descargado y verificado
✅ VM creada con nombre "GX-Registry-Production"
✅ RAM: 2048 o 4096 MB asignados
✅ CPUs: 2 o 4 asignados
✅ Disco duro virtual: 30 GB creado
✅ Virtualización (VT-x/AMD-V) habilitada
✅ ISO montado en unidad óptica
✅ Red configurada en modo NAT
✅ 4 reglas de reenvío de puertos configuradas:
    ✅ SSH (2222 → 22)
    ✅ HTTP (8080 → 80)
    ✅ HTTPS (8443 → 443)
    ✅ App (8000 → 8000)
✅ Orden de arranque: Óptica primero
```

### Crear Snapshot Inicial (Opcional pero Recomendado)

**¿Qué es un snapshot?**

Un snapshot es un punto de restauración. Si algo sale mal durante la instalación, puedes volver a este punto sin perder la configuración.

**Crear snapshot**:

1. En VirtualBox, con la VM seleccionada
2. Haz clic en el botón **"Tomar"** junto a "Instantáneas" (o menú Máquina → Tomar instantánea)
3. Nombre: `Antes de instalar Ubuntu`
4. Descripción: `VM configurada, lista para instalación`
5. Haz clic en **"Aceptar"**

**Beneficio**: Si la instalación falla, puedes restaurar este snapshot y empezar de nuevo sin reconfigurar todo.

### Información Importante para los Siguientes Pasos

**Teclado en VirtualBox**:

Cuando la VM esté corriendo:

**Capturar teclado/mouse**:
- Haz clic dentro de la ventana de la VM
- El teclado y mouse quedan "capturados"

**Liberar teclado/mouse**:
- Presiona la **tecla Host** (por defecto: `Ctrl derecho`)
- Ahora puedes usar el teclado/mouse en Windows

**Cambiar tecla Host** (opcional):
- VirtualBox → Archivo → Preferencias → Entrada
- Puedes cambiar a otra tecla (ejemplo: `Ctrl izquierdo`)

### ¡Listo para Instalar!

Todo está configurado. En el siguiente paso iniciaremos la VM y comenzaremos la instalación de Ubuntu Server.

**NO cierres VirtualBox**.

---

# FASE 3: INSTALACIÓN DE UBUNTU SERVER

---

## Paso 11: Iniciar Instalación

### Objetivo
Iniciar la máquina virtual y arrancar el instalador de Ubuntu Server.

### Procedimiento Detallado

#### 11.1 Iniciar la VM

**En VirtualBox, con "GX-Registry-Production" seleccionada**:

**Hay varias formas de iniciar**:

**Opción A**: Haz clic en el botón **"Iniciar"** (flecha verde) en la barra de herramientas.

**Opción B**: Doble clic en la VM en el panel izquierdo.

**Opción C**: Clic derecho en la VM → **Iniciar** → **Inicio normal**.

**Atajo**: Selecciona la VM y presiona `Ctrl + T`.

**Qué sucede**:
1. Se abre una **nueva ventana** (ventana de la VM)
2. Fondo negro con logo de VirtualBox
3. Mensajes de arranque

#### 11.2 Proceso de Arranque Inicial

**Qué verás en la ventana**:

**Primeros segundos**:
```
Oracle VM VirtualBox
Versión 7.0.14
```

**Luego mensajes de BIOS**:
```
VirtualBox BIOS
BIOS Date: 06/23/99
...
```

**Después**:
```
Booting from DVD/CD...
```

**Pantalla negra con cursor parpadeando**: Es normal, espera unos segundos.

#### 11.3 Menú de Arranque de Ubuntu

**Después de 5-10 segundos verás**:

**Pantalla negra con logo de Ubuntu** (puntos naranjas) y menú:

```
GNU GRUB  version 2.06

┌──────────────────────────────────────────────────┐
│ *Try or Install Ubuntu Server                   │
│  Ubuntu Server (safe graphics)                   │
│  Test memory                                     │
│  Boot from first hard disk                       │
│  UEFI Firmware Settings                          │
└──────────────────────────────────────────────────┘

Use the ↑ and ↓ keys to select which entry is highlighted.
Press enter to boot the selected OS, `e' to edit the commands
before booting or `c' for a command-line.
```

**Opción seleccionada por defecto**: `Try or Install Ubuntu Server` (con asterisco)

**Qué hacer**:

1. **Asegúrate de que** `Try or Install Ubuntu Server` **esté seleccionado** (debería estar por defecto)
2. **Presiona** `Enter`

**Si no haces nada**: Después de 30 segundos, arrancará automáticamente.

#### 11.4 Carga del Instalador

**Qué verás**:

**Pantalla negra** con mensajes desplazándose:

```
[    0.000000] Linux version 5.15.0-117-generic ...
[    0.000000] Command line: BOOT_IMAGE=/casper/vmlinuz ...
[    0.001234] x86/fpu: x87 FPU will use FXSAVE
...
[    2.345678] cloud-init[789]: Cloud-init v. 23.3.3 running...
...
```

**Estos son mensajes del kernel de Linux arrancando**. Es completamente normal.

**Duración**: 20-40 segundos.

**Pantalla puede parpadear** o cambiar de resolución. No te preocupes.

#### 11.5 Pantalla de Bienvenida del Instalador

**Finalmente verás**:

**Interfaz de texto con fondo negro y texto blanco/gris**:

**Parte superior**:
```
┌───────────────────── Willkommen! Bienvenue! Welcome! ...─┐
│                                                            │
```

**Centro de la pantalla**:
```
Use UP, DOWN and ENTER keys to select your language.

  English
  Español
  Français
  Deutsch
  ...
```

**Parte inferior**:
```
[ Help ]                                      [ Confirm: ]
```

**¡El instalador ha iniciado correctamente!** ✅

### Verificación

✅ **VM iniciada**
✅ **GRUB apareció correctamente**
✅ **Kernel de Linux cargado**
✅ **Instalador de Ubuntu Server mostrando selección de idioma**
✅ **Puedes usar las flechas del teclado para navegar**

### Navegación en el Instalador

**Controles del teclado**:

| Tecla | Función |
|-------|---------|
| `↑` `↓` | Navegar opciones |
| `Enter` | Confirmar/Continuar |
| `Tab` | Cambiar entre campos |
| `Espacio` | Marcar/Desmarcar casillas |
| `Esc` | Cancelar/Volver |

**NO uses el mouse**: El instalador es solo por teclado.

### Solución de Problemas

**Problema**: Pantalla negra y no pasa nada.

**Solución**:
1. Espera al menos 2 minutos
2. Si no cambia, presiona `Enter`
3. Si aún no responde, cierra la VM y reinicia

**Problema**: "Operating system not found"

**Causa**: El ISO no está montado correctamente.

**Solución**:
1. Cierra la VM (X en la ventana → Apagar)
2. VirtualBox → Configuración → Almacenamiento
3. Verifica que el ISO esté montado
4. Reinicia la VM

**Problema**: "VT-x is not available"

**Causa**: Virtualización deshabilitada en BIOS.

**Solución**: Ver Paso 6, sección de Solución de Problemas.

**Problema**: La VM está muy lenta.

**Causa**: Pocos recursos asignados.

**Solución**:
1. Apaga la VM
2. Configura más RAM o CPUs (si tu PC lo permite)
3. Reinicia

---

## Paso 12: Configurar Idioma y Teclado

### Objetivo
Seleccionar el idioma del instalador y configurar la distribución del teclado.

### Procedimiento Detallado

#### 12.1 Seleccionar Idioma del Instalador

**Pantalla actual**: "Language Selection"

**Opciones visibles**:
```
Use UP, DOWN and ENTER keys to select your language.

  English
  Español
  Français
  Deutsch
  ...
```

**Recomendación**: **Selecciona "English"**

**¿Por qué English?**
- Documentación y mensajes de error más fáciles de buscar en Google
- Comandos del sistema en inglés (estándar)
- Este tutorial está adaptado para instalación en inglés

**Cómo seleccionar**:
1. Usa las flechas `↑` `↓` para navegar
2. Coloca el cursor en **"English"**
3. Presiona `Enter`

**Qué sucede**: Avanza a la siguiente pantalla.

#### 12.2 Actualizar Instalador (Opcional)

**Puede aparecer**: "Installer Update Available"

**Mensaje**:
```
An updated version of the installer is available.

Release notes:
  - Bug fixes...

[ Continue without updating ]  [ Update to the new installer ]
```

**Qué hacer**:

**Opción A** (Recomendada): Selecciona **"Continue without updating"** y presiona `Enter`
- La versión actual funciona perfectamente
- Actualizar puede tardar más tiempo

**Opción B**: Selecciona **"Update to the new installer"**
- Descargará e instalará la versión más reciente
- Espera a que termine y reinicia automáticamente

**Para este tutorial**: Usaremos **"Continue without updating"**.

#### 12.3 Configurar Teclado

**Pantalla**: "Keyboard configuration"

**Qué verás**:
```
┌─────────────── Keyboard configuration ───────────────┐
│                                                       │
│ Please select your keyboard layout below, or select  │
│ "Identify keyboard" to detect your keyboard layout.  │
│                                                       │
│ Layout: [ English (US)                           ▼ ] │
│                                                       │
│ Variant: [ English (US)                          ▼ ] │
│                                                       │
│ [ Identify keyboard ]                                │
│                                                       │
│ [ Done ]                    [ Back ]                 │
└───────────────────────────────────────────────────────┘
```

**Configuración**:

**Layout** (Distribución):

**Si tienes teclado en español**:
1. Presiona `Tab` hasta que esté seleccionado el campo "Layout"
2. Presiona `Enter`
3. Aparece lista de idiomas
4. Usa flechas `↑` `↓` para buscar: **"Spanish"**
5. Presiona `Enter`

**Si tienes teclado en inglés**:
- Deja **"English (US)"**

**Variant** (Variante):

Después de seleccionar Layout:
1. Presiona `Tab` para ir a "Variant"
2. Presiona `Enter`
3. Selecciona la variante según tu región:
   - **Spanish (Latin America)** - Teclado latinoamericano
   - **Spanish** - Teclado español de España
   - **English (US)** - Teclado inglés estándar

**Probar configuración**:

En la parte inferior puede haber un campo de prueba donde puedes escribir para verificar que las teclas funcionen correctamente.

**Confirmar**:
1. Presiona `Tab` hasta llegar a **"[ Done ]"**
2. Presiona `Enter`

### Verificación

✅ **Idioma seleccionado**: English
✅ **Teclado configurado**: Según tu hardware
✅ **Avanzaste a la siguiente pantalla**

---

## Paso 13: Configurar Red

### Objetivo
Verificar que la VM tenga conexión a Internet mediante NAT.

### Procedimiento Detallado

#### 13.1 Pantalla de Configuración de Red

**Pantalla**: "Network connections"

**Qué verás**:
```
┌──────────────── Network connections ─────────────────┐
│                                                       │
│ ┌───────────────────────────────────────────────┐   │
│ │ enp0s3  eth  10.0.2.15/24                      │   │
│ └───────────────────────────────────────────────┘   │
│                                                       │
│ The following networks are available:                │
│                                                       │
│ Name             Type  Subnet         Address        │
│ ─────────────────────────────────────────────────── │
│ enp0s3          DHCPv4  10.0.2.0/24   10.0.2.15      │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

**Qué significa**:

- **enp0s3**: Nombre de la interfaz de red (puede variar)
- **10.0.2.15/24**: IP asignada automáticamente por NAT de VirtualBox
- **DHCPv4**: Configuración automática (correcto)

**¿Es correcto?**

✅ **Sí**, si ves:
- Una interfaz de red (enp0s3 o similar)
- IP asignada (10.0.2.x)
- Estado activo

❌ **No**, si ves:
- "No network connections"
- Sin IP asignada
- Error de conexión

#### 13.2 Verificar Conexión

**La red debería estar configurada automáticamente** gracias al NAT de VirtualBox.

**NO necesitas cambiar nada** en esta pantalla.

**Qué hacer**:
1. Verifica que haya una interfaz con IP asignada
2. Presiona `Tab` hasta **"[ Done ]"**
3. Presiona `Enter`

### Solución de Problemas de Red

**Problema**: No aparece ninguna interfaz de red.

**Causa**: Adaptador de red no habilitado en la VM.

**Solución**:
1. Presiona `Ctrl derecho` (tecla Host) para salir de la VM
2. Cierra la VM (X → Apagar)
3. VirtualBox → Configuración → Red
4. Verifica que Adaptador 1 esté habilitado y en modo NAT
5. Reinicia la instalación

**Problema**: Aparece "Failed to get address"

**Causa**: DHCP no está funcionando.

**Solución**:
1. En la pantalla de red, selecciona la interfaz
2. Presiona `Enter`
3. Selecciona "Edit IPv4"
4. Verifica que esté en "Automatic (DHCP)"
5. Si no funciona, usa configuración manual:
   - IP address: 10.0.2.15
   - Subnet: 255.255.255.0
   - Gateway: 10.0.2.2
   - DNS: 8.8.8.8

### Verificación

✅ **Interfaz de red detectada**
✅ **IP asignada automáticamente**
✅ **Configuración DHCPv4 activa**
✅ **Avanzaste a siguiente pantalla**

---

## Paso 14: Configurar Proxy (Opcional)

### Objetivo
Configurar proxy HTTP si tu red lo requiere (generalmente NO es necesario).

### Procedimiento Detallado

#### 14.1 Pantalla de Proxy

**Pantalla**: "Configure proxy"

**Qué verás**:
```
┌────────────────── Configure proxy ───────────────────┐
│                                                       │
│ If this system requires an HTTP proxy to access the  │
│ Internet, enter its details here.                    │
│                                                       │
│ Proxy address: [________________________________]    │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

**¿Necesitas un proxy?**

**NO** (mayoría de casos):
- Si tu red doméstica o empresa NO usa proxy
- Si puedes navegar normalmente en Internet sin configurar proxy
- Si la VM está en tu PC personal

**SÍ** (casos específicos):
- Si tu empresa requiere proxy para salir a Internet
- Si sabes que tienes un servidor proxy configurado

#### 14.2 Configurar Proxy (si es necesario)

**Si NO necesitas proxy** (caso más común):
1. Deja el campo vacío
2. Presiona `Tab` hasta **"[ Done ]"**
3. Presiona `Enter`

**Si SÍ necesitas proxy**:
1. En "Proxy address" escribe: `http://IP:PUERTO`
2. Ejemplo: `http://192.168.1.100:8080`
3. O con autenticación: `http://usuario:contraseña@IP:PUERTO`
4. Presiona `Tab` hasta **"[ Done ]"**
5. Presiona `Enter`

**Para este tutorial**: **Dejar vacío** (sin proxy).

### Verificación

✅ **Campo de proxy dejado vacío** (o configurado si era necesario)
✅ **Avanzaste a siguiente pantalla**

---

## Paso 15: Configurar Mirror de Ubuntu

### Objetivo
Seleccionar el servidor de donde se descargarán paquetes de Ubuntu.

### Procedimiento Detallado

#### 15.1 Pantalla de Mirror

**Pantalla**: "Configure Ubuntu archive mirror"

**Qué verás**:
```
┌─────── Configure Ubuntu archive mirror ──────────────┐
│                                                       │
│ If you use an alternative mirror for Ubuntu, enter   │
│ its details here.                                     │
│                                                       │
│ Mirror address: [http://archive.ubuntu.com/ubuntu]   │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

**Valor por defecto**:
```
http://archive.ubuntu.com/ubuntu
```

O puede aparecer un mirror regional:
```
http://mx.archive.ubuntu.com/ubuntu  (México)
http://ar.archive.ubuntu.com/ubuntu  (Argentina)
http://es.archive.ubuntu.com/ubuntu  (España)
```

#### 15.2 ¿Cambiar el Mirror?

**NO cambiar** (recomendado):
- El mirror por defecto funciona bien
- Es rápido y confiable
- Tiene todos los paquetes necesarios

**Cambiar** (opcional):
- Si tienes un mirror local más rápido
- Si conoces un mirror específico de tu región

**Qué hacer**:
1. **Deja el valor por defecto**
2. Presiona `Tab` hasta **"[ Done ]"**
3. Presiona `Enter`

**El instalador verificará la conexión** al mirror (tarda unos segundos).

**Qué verás**:
```
Testing connection to mirror...
```

**Espera** a que termine la verificación.

### Verificación

✅ **Mirror configurado correctamente**
✅ **Conexión al mirror verificada**
✅ **Avanzaste a siguiente pantalla**

---

## Paso 16: Configurar Almacenamiento

### Objetivo
Configurar cómo se particionará el disco duro virtual.

### Procedimiento Detallado

#### 16.1 Pantalla de Almacenamiento

**Pantalla**: "Guided storage configuration"

**Qué verás**:
```
┌────── Guided storage configuration ──────────────────┐
│                                                       │
│ Configure a guided storage layout, or create a       │
│ custom one.                                           │
│                                                       │
│ (X) Use an entire disk                               │
│                                                       │
│ [ ] Use an entire disk and set up LVM                │
│                                                       │
│ [ ] Custom storage layout                            │
│                                                       │
│ ┌─────────────────────────────────────────────────┐ │
│ │ [X] VBOX HARDDISK  30.00G                       │ │
│ └─────────────────────────────────────────────────┘ │
│                                                       │
│ [ ] Set up this disk as an LVM group                 │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

**Opciones disponibles**:

1. **Use an entire disk** (Recomendado) ✅
   - Usa todo el disco virtual
   - Particiones automáticas
   - Simple y funcional

2. **Use an entire disk and set up LVM**
   - Usa LVM (Logical Volume Manager)
   - Más flexible para redimensionar particiones
   - Más complejo

3. **Custom storage layout**
   - Crear particiones manualmente
   - Para usuarios avanzados

#### 16.2 Seleccionar Configuración

**Para este proyecto** (recomendado):

1. Asegúrate de que esté seleccionado: **(X) Use an entire disk**
2. Asegúrate de que el disco esté marcado: **[X] VBOX HARDDISK 30.00G**
3. **NO marques** "Set up this disk as an LVM group" (dejar desmarcado)

**Cómo seleccionar**:
- Usa flechas `↑` `↓` para navegar entre opciones
- Presiona `Espacio` para marcar/desmarcar
- Presiona `Tab` para cambiar entre secciones

**Confirmar selección**:
1. Presiona `Tab` hasta **"[ Done ]"**
2. Presiona `Enter`

#### 16.3 Revisar Particiones

**Pantalla**: "Storage configuration"

**Qué verás**: Resumen del esquema de particionado

```
┌────────────── Storage configuration ─────────────────┐
│                                                       │
│ FILE SYSTEM SUMMARY                                   │
│                                                       │
│ MOUNT POINT     SIZE    TYPE   DEVICE                │
│ /               29.5G   ext4   /dev/sda2             │
│                 500M    FAT32  /dev/sda1             │
│                                                       │
│ AVAILABLE DEVICES                                     │
│                                                       │
│ [ ] sda  VBOX HARDDISK  30.00G                       │
│                                                       │
│ [ Done ]            [ Reset ]           [ Back ]     │
└───────────────────────────────────────────────────────┘
```

**Particiones creadas automáticamente**:

| Partición | Tamaño | Tipo | Punto de montaje | Uso |
|-----------|--------|------|------------------|-----|
| /dev/sda1 | 512 MB | FAT32 | /boot/efi | Arranque UEFI |
| /dev/sda2 | ~29.5 GB | ext4 | / | Sistema raíz |

**¿Es correcto?**

✅ **Sí**, si ves:
- Partición raíz `/` con casi todo el espacio (~29.5 GB)
- Partición EFI `/boot/efi` (~512 MB)
- Total suma ~30 GB

**Confirmar**:
1. Revisa que todo esté correcto
2. Presiona `Tab` hasta **"[ Done ]"**
3. Presiona `Enter`

#### 16.4 Confirmar Cambios Destructivos

**Aparece ventana de confirmación**:

```
┌────────────── Confirm destructive action ────────────┐
│                                                       │
│ Selecting Continue below will begin the installation │
│ process and result in the loss of data on the        │
│ disks selected to be formatted.                      │
│                                                       │
│ You will not be able to return to this or a          │
│ previous screen once the installation has started.   │
│                                                       │
│ Are you sure you want to continue?                   │
│                                                       │
│ [ Continue ]                    [ Back ]             │
└───────────────────────────────────────────────────────┘
```

**Qué significa**:
- El instalador formateará el disco virtual
- Perderás cualquier dato en el disco (pero es nuevo, está vacío)
- No podrás volver atrás

**Qué hacer**:
1. Presiona `Tab` para seleccionar **"[ Continue ]"**
2. Presiona `Enter`

**⚠️ IMPORTANTE**: Esto es seguro porque:
- Es un disco virtual nuevo
- No tiene datos
- No afecta tu Windows ni otros discos

### Verificación

✅ **Modo seleccionado**: Use an entire disk
✅ **Disco seleccionado**: VBOX HARDDISK 30GB
✅ **Particiones revisadas**: / (raíz) y /boot/efi
✅ **Confirmación aceptada**
✅ **Instalación iniciada**

---

## Paso 17: Crear Usuario Inicial

### Objetivo
Crear el usuario principal que usarás para administrar el servidor.

### Procedimiento Detallado

#### 17.1 Pantalla de Perfil

**Pantalla**: "Profile setup"

**Qué verás**:
```
┌──────────────────── Profile setup ───────────────────┐
│                                                       │
│ Enter the username and password you will use to log  │
│ in to the system.                                     │
│                                                       │
│ Your name: [____________________________________]    │
│                                                       │
│ Your server's name: [____________________________]    │
│                                                       │
│ Pick a username: [_______________________________]    │
│                                                       │
│ Choose a password: [_____________________________]    │
│                                                       │
│ Confirm your password: [_________________________]    │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

#### 17.2 Completar Campos

**Campo 1: Your name** (Tu nombre completo)

**Qué ingresar**: Tu nombre real o descriptivo

**Ejemplo**:
```
GX Administrator
```

O simplemente:
```
Admin
```

**Cómo llenar**:
1. El cursor ya está en este campo
2. Escribe tu nombre
3. Presiona `Tab` para ir al siguiente campo

**Campo 2: Your server's name** (Nombre del servidor)

**Qué ingresar**: Nombre de la máquina (hostname)

**Recomendado** (de acuerdo al Paso 5):
```
gxregistry
```

**Características del hostname**:
- Solo letras minúsculas
- Sin espacios
- Sin caracteres especiales (solo guiones `-`)
- Será visible en el prompt: `usuario@gxregistry:~$`

**Cómo llenar**:
1. Escribe: `gxregistry`
2. Presiona `Tab`

**Campo 3: Pick a username** (Nombre de usuario)

**Qué ingresar**: Usuario para login

**Recomendado** (de acuerdo al Paso 5):
```
gxapp
```

**Características del username**:
- Solo letras minúsculas
- Sin espacios
- Primer carácter debe ser letra
- Puede contener números y guiones
- Será el usuario con el que te conectes por SSH

**Cómo llenar**:
1. Escribe: `gxapp`
2. Presiona `Tab`

**Campo 4: Choose a password** (Contraseña)

**Qué ingresar**: Contraseña segura para este usuario

**⚠️ MUY IMPORTANTE**:
- **Usa una contraseña SEGURA**
- Mínimo 8 caracteres
- Combina letras mayúsculas, minúsculas, números y símbolos
- **ANÓTALA** - la necesitarás constantemente

**Ejemplo de contraseña segura**:
```
GxApp2026!Prod
```

**NO uses contraseñas débiles como**:
- `password`
- `123456`
- `admin`
- Nombre del usuario

**Cómo llenar**:
1. Escribe tu contraseña (no se verá, es normal)
2. Presiona `Tab`

**Campo 5: Confirm your password** (Confirmar contraseña)

**Qué ingresar**: La misma contraseña exactamente

**Cómo llenar**:
1. Escribe la contraseña nuevamente
2. **Asegúrate de que sea EXACTAMENTE igual**
3. Presiona `Tab` hasta **"[ Done ]"**
4. Presiona `Enter`

**Si las contraseñas no coinciden**: Aparecerá un error. Vuelve a llenar los campos de contraseña.

#### 17.3 Verificar Información

**Antes de presionar Done, verifica**:

```
✅ Your name: GX Administrator (o el que pusiste)
✅ Server name: gxregistry
✅ Username: gxapp
✅ Password: ********* (escrita correctamente)
✅ Confirm password: ********* (coincide)
```

**⚠️ ANOTA ESTA INFORMACIÓN**:

```
Usuario: gxapp
Contraseña: [tu contraseña segura]
Hostname: gxregistry
```

### Verificación

✅ **Nombre completo ingresado**
✅ **Hostname**: gxregistry
✅ **Usuario**: gxapp
✅ **Contraseña segura** creada y confirmada
✅ **Información anotada** en lugar seguro
✅ **Avanzaste a siguiente pantalla**

---

## Paso 18: Instalar OpenSSH Server

### Objetivo
Instalar el servidor SSH para poder conectarte remotamente desde Windows.

### Importancia de OpenSSH

**OpenSSH** es CRÍTICO porque:
- ✅ Permite conectarte desde Windows por SSH
- ✅ Sin SSH, solo puedes usar la consola de VirtualBox (incómodo)
- ✅ Con SSH puedes copiar/pegar comandos
- ✅ Necesario para administración remota

**⚠️ MUY IMPORTANTE**: No saltear este paso.

### Procedimiento Detallado

#### 18.1 Pantalla de SSH Setup

**Pantalla**: "SSH Setup"

**Qué verás**:
```
┌──────────────────── SSH Setup ───────────────────────┐
│                                                       │
│ You can choose to install the OpenSSH server         │
│ package to enable secure remote access to your       │
│ server.                                               │
│                                                       │
│ [X] Install OpenSSH server                           │
│                                                       │
│ Import SSH identity:                                  │
│   ( ) No                                              │
│   ( ) from GitHub                                     │
│   ( ) from Launchpad                                  │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

#### 18.2 Marcar Instalación de OpenSSH

**MUY IMPORTANTE**:

1. **Asegúrate de que** `[X] Install OpenSSH server` **esté MARCADO**
2. Si NO está marcado:
   - Usa flechas `↑` `↓` para llegar a esa opción
   - Presiona `Espacio` para marcar
   - Debe aparecer `[X]` (marcado)

#### 18.3 Importar Identidad SSH (Opcional)

**Opciones de "Import SSH identity"**:

**( ) No** (Recomendado para este tutorial)
- No importar claves SSH
- Usarás usuario y contraseña para conectarte
- Más simple para principiantes

**( ) from GitHub**
- Importar claves SSH públicas de tu cuenta GitHub
- Solo si tienes cuenta en GitHub con claves SSH configuradas

**( ) from Launchpad**
- Importar de Launchpad (plataforma de Ubuntu)
- Raramente usado

**Para este tutorial**: Selecciona **"No"**

**Cómo seleccionar**:
1. Usa flechas para navegar a las opciones de "Import SSH identity"
2. Presiona `Espacio` en **"No"**
3. Debe aparecer: `(X) No`

#### 18.4 Confirmar Configuración

**Verificación antes de continuar**:
```
[X] Install OpenSSH server  ← DEBE estar marcado
(X) No                      ← Import identity en "No"
```

**Confirmar**:
1. Presiona `Tab` hasta **"[ Done ]"**
2. Presiona `Enter`

### ¿Qué Instalará?

**Paquete que se instalará**:
- `openssh-server` - Servidor SSH

**Puerto que abrirá**:
- Puerto 22 (SSH)

**Después de la instalación podrás**:
```powershell
# Desde Windows PowerShell
ssh -p 2222 gxapp@localhost
```

(Puerto 2222 en Windows redirige a puerto 22 en Ubuntu - configurado en Paso 8)

### Verificación

✅ **OpenSSH Server MARCADO para instalación**
✅ **Import SSH identity**: No
✅ **Avanzaste a siguiente pantalla**

### Solución de Problemas

**Problema**: Olvidé marcar "Install OpenSSH server"

**Solución**: Después de instalar Ubuntu, puedes instalarlo manualmente:
```bash
sudo apt update
sudo apt install openssh-server
```

Pero es mejor marcarlo ahora.

---

## Paso 19: Seleccionar Software Adicional (Featured Server Snaps)

### Objetivo
Decidir si instalar software adicional pre-empaquetado.

### Procedimiento Detallado

#### 19.1 Pantalla de Featured Server Snaps

**Pantalla**: "Featured Server Snaps"

**Qué verás**:
```
┌──────────── Featured Server Snaps ───────────────────┐
│                                                       │
│ These are popular snaps in server environments.      │
│ Select or deselect with SPACE, press ENTER to see   │
│ more details of the package, publisher and versions  │
│ available.                                            │
│                                                       │
│ [ ] docker          Docker container runtime         │
│ [ ] microk8s        Lightweight Kubernetes           │
│ [ ] lxd             System container manager         │
│ [ ] nextcloud       Nextcloud server                 │
│ [ ] postgresql      PostgreSQL database              │
│ ...                                                   │
│                                                       │
│ [ Done ]                        [ Back ]             │
└───────────────────────────────────────────────────────┘
```

#### 19.2 ¿Seleccionar Alguno?

**RECOMENDACIÓN**: **NO marcar ninguno**

**¿Por qué?**
- Instalaremos todo manualmente con `apt`
- Más control sobre versiones
- Evita conflictos
- PostgreSQL lo instalaremos de repositorios oficiales (no snap)
- Docker no lo necesitamos para este proyecto

**Qué hacer**:
1. **NO marques ninguna opción** (deja todo desmarcado)
2. Presiona `Tab` hasta **"[ Done ]"**
3. Presiona `Enter`

### Alternativa: Si Quieres Instalar PostgreSQL desde Aquí

**Solo si prefieres** instalarlo ahora (no recomendado para seguir el tutorial):

1. Usa flechas para navegar a `[ ] postgresql`
2. Presiona `Espacio` para marcar: `[X] postgresql`
3. Presiona `Tab` hasta **"[ Done ]"**
4. Presiona `Enter`

**Nota**: En el tutorial instalaremos PostgreSQL manualmente para tener más control.

### Verificación

✅ **Ningún snap seleccionado** (o los que decidiste instalar)
✅ **Avanzaste a siguiente pantalla**

---

## Paso 20: Proceso de Instalación y Finalización

### Objetivo
Esperar a que la instalación se complete y reiniciar el sistema.

### Procedimiento Detallado

#### 20.1 Pantalla de Instalación en Progreso

**Pantalla**: "Installing system"

**Qué verás**:

**Parte superior**:
```
┌──────────────── Installing system ───────────────────┐
│                                                       │
│ The installer is now installing the system.          │
│                                                       │
```

**Centro de la pantalla**:
Mensajes de progreso desplazándose:

```
start: subiquity/Install/install/curtin_install/run_curtin_step/cmd-install/stage-curthooks/builtin/cmd-curthooks/configuring-bootloader: configuring target system bootloader
start:    subiquity/Install/install/curtin_install/run_curtin_step/cmd-install/stage-curthooks/builtin/cmd-curthooks/install-grub: installing grub to target devices
finish:   subiquity/Install/install/curtin_install/run_curtin_step/cmd-install/stage-curthooks/builtin/cmd-curthooks/install-grub: installing grub to target devices
start:    subiquity/Install/install/postinstall: final system configuration
start:       subiquity/Install/install/postinstall/get_target_packages: calculating extra packages to install
finish:      subiquity/Install/install/postinstall/get_target_packages: calculating extra packages to install
start:       subiquity/Install/install/postinstall/configure_cloud_init: configuring cloud-init
finish:      subiquity/Install/install/postinstall/configure_cloud_init: configuring cloud-init
start:       subiquity/Install/install/postinstall/run_unattended_upgrades: downloading and installing security updates
...
```

**Estos mensajes indican**:
- ✅ Instalando bootloader (GRUB)
- ✅ Configurando sistema
- ✅ Descargando actualizaciones de seguridad
- ✅ Instalando OpenSSH
- ✅ Configurando paquetes

#### 20.2 Duración de la Instalación

**Tiempo estimado**:
- **Instalación básica**: 5-10 minutos
- **Descarga de actualizaciones**: +5-15 minutos (depende de conexión)
- **Total**: 10-25 minutos

**Qué hacer mientras esperas**:
- ✅ NO toques nada
- ✅ NO cierres la ventana
- ✅ NO presiones teclas
- ✅ Espera pacientemente

**Mensajes que verás** (ejemplos):
```
Installing kernel...
Setting up openssh-server...
Configuring grub-pc...
Running unattended upgrades...
Cleaning up...
```

#### 20.3 Instalación Completa

**Cuando la instalación termine, verás**:

**Pantalla**: "Installation complete!"

```
┌────────────── Installation complete! ────────────────┐
│                                                       │
│ Congratulations! The installation is now complete.   │
│                                                       │
│ The system will reboot when you select Reboot Now.   │
│                                                       │
│ After rebooting, remember to remove the installation │
│ media, then press ENTER to boot the installed        │
│ system.                                               │
│                                                       │
│ [ Reboot Now ]              [ View full log ]        │
└───────────────────────────────────────────────────────┘
```

**¡Felicitaciones!** ✅ Ubuntu Server está instalado.

#### 20.4 Reiniciar el Sistema

**Opciones**:

**[ Reboot Now ]** (Reiniciar ahora)
- Reinicia inmediatamente
- Recomendado

**[ View full log ]** (Ver log completo)
- Muestra detalles de la instalación
- Para diagnóstico
- No es necesario ver

**Qué hacer**:
1. Presiona `Tab` para seleccionar **"[ Reboot Now ]"**
2. Presiona `Enter`

**Qué sucede**:
- La VM comenzará a reiniciarse
- Verás mensajes de apagado
- Pantalla se pondrá negra

#### 20.5 Mensaje sobre Installation Media

**Puede aparecer un mensaje**:

```
Please remove the installation medium, then press ENTER:
```

**NO hagas nada**. VirtualBox expulsará automáticamente el ISO.

**Espera 10-20 segundos**.

Si el mensaje persiste:
1. Presiona `Enter`
2. La VM continuará arrancando

#### 20.6 Primer Arranque del Sistema Instalado

**Qué verás después del reinicio**:

**Mensajes de arranque de Linux**:
```
[    0.000000] Linux version 5.15.0-117-generic
[    1.234567] systemd[1]: Starting OpenSSH server daemon...
[    2.345678] cloud-init[789]: Cloud-init v. 23.3.3 running...
...
```

**Luego, la pantalla de login**:
```
Ubuntu 22.04.5 LTS gxregistry tty1

gxregistry login: _
```

**¡El sistema está listo!** ✅

### Verificación

✅ **Instalación completada exitosamente**
✅ **Sistema reiniciado**
✅ **Pantalla de login visible**
✅ **Hostname correcto**: gxregistry

---

## Paso 21: Primer Login y Verificación

### Objetivo
Iniciar sesión por primera vez y verificar que todo funciona.

### Procedimiento Detallado

#### 21.1 Login desde Consola de VirtualBox

**Pantalla de login**:
```
Ubuntu 22.04.5 LTS gxregistry tty1

gxregistry login: _
```

**Ingresar usuario**:
1. Escribe: `gxapp` (el usuario que creaste)
2. Presiona `Enter`

**Solicita contraseña**:
```
Password: _
```

3. Escribe tu contraseña (no se verá, es normal)
4. Presiona `Enter`

**Si la contraseña es correcta**:

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-117-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

0 updates can be applied immediately.

Last login: Mon Aug  3 10:30:15 UTC 2026
gxapp@gxregistry:~$ _
```

**¡Has iniciado sesión!** ✅

#### 21.2 Verificar Información del Sistema

**Verificar hostname**:
```bash
hostname
```

**Salida esperada**:
```
gxregistry
```

**Verificar usuario**:
```bash
whoami
```

**Salida esperada**:
```
gxapp
```

**Verificar versión de Ubuntu**:
```bash
lsb_release -a
```

**Salida esperada**:
```
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Release:        22.04
Codename:       jammy
```

**Verificar dirección IP**:
```bash
ip addr show
```

**Busca la interfaz** `enp0s3` (o similar):
```
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic enp0s3
```

**IP asignada**: `10.0.2.15` (o similar en rango 10.0.2.x)

#### 21.3 Verificar Conectividad a Internet

**Ping a Google**:
```bash
ping -c 4 google.com
```

**Salida esperada**:
```
PING google.com (142.250.185.46) 56(84) bytes of data.
64 bytes from 142.250.185.46: icmp_seq=1 ttl=115 time=15.2 ms
64 bytes from 142.250.185.46: icmp_seq=2 ttl=115 time=14.8 ms
64 bytes from 142.250.185.46: icmp_seq=3 ttl=115 time=15.1 ms
64 bytes from 142.250.185.46: icmp_seq=4 ttl=115 time=14.9 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
```

**Si funciona**: ✅ Tienes Internet

**Si no funciona**: Ver sección de solución de problemas.

#### 21.4 Verificar SSH Instalado

**Comprobar estado de SSH**:
```bash
sudo systemctl status ssh
```

**Te pedirá contraseña** (es la primera vez que usas `sudo`):
```
[sudo] password for gxapp: _
```

Escribe tu contraseña y presiona `Enter`.

**Salida esperada**:
```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2026-08-03 10:30:25 UTC; 5min ago
```

**Importante**:
- `Active: active (running)` ← SSH está corriendo ✅
- `enabled` ← Se inicia automáticamente ✅

**Presiona** `q` para salir de la visualización.

### Verificación

✅ **Login exitoso** con usuario `gxapp`
✅ **Hostname**: gxregistry
✅ **IP asignada**: 10.0.2.x
✅ **Internet funciona** (ping exitoso)
✅ **SSH corriendo** y habilitado

---

## Paso 22: Conectarse por SSH desde Windows

### Objetivo
Conectarte a Ubuntu desde PowerShell/Terminal de Windows usando SSH.

### Por Qué Usar SSH

**Ventajas de SSH vs Consola de VirtualBox**:
- ✅ Puedes copiar y pegar comandos
- ✅ Mejor rendimiento de texto
- ✅ Múltiples ventanas/pestañas
- ✅ Redimensionable
- ✅ Más cómodo para trabajar

### Procedimiento Detallado

#### 22.1 Obtener IP de la VM (Opcional - para verificación)

**Desde la consola de Ubuntu (VirtualBox)**:
```bash
ip addr show enp0s3 | grep inet
```

**Salida esperada**:
```
inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic enp0s3
```

**Anota la IP**: `10.0.2.15` (aunque no la necesitarás gracias al port forwarding)

#### 22.2 Abrir PowerShell en Windows

**En tu Windows** (NO en la VM):

1. Presiona `Windows + R`
2. Escribe: `powershell`
3. Presiona `Enter`

O busca "PowerShell" en el menú Inicio.

#### 22.3 Conectarse por SSH

**En PowerShell, ejecuta**:

```powershell
ssh -p 2222 gxapp@localhost
```

**Qué hace cada parte**:
- `ssh`: Comando SSH
- `-p 2222`: Puerto 2222 de Windows (redirige a puerto 22 de Ubuntu)
- `gxapp`: Tu usuario en Ubuntu
- `localhost`: Tu propia máquina (Windows)

**Primera vez - Advertencia de Seguridad**:

```
The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? _
```

**Qué hacer**:
1. Escribe: `yes`
2. Presiona `Enter`

**Solicita contraseña**:
```
gxapp@localhost's password: _
```

3. Escribe tu contraseña de Ubuntu
4. Presiona `Enter`

**Conexión exitosa**:

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-117-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Last login: Mon Aug  3 10:35:42 2026 from 10.0.2.2
gxapp@gxregistry:~$ _
```

**¡Estás conectado por SSH desde Windows!** ✅

#### 22.4 Probar SSH

**Ejecuta un comando simple**:
```bash
uname -a
```

**Salida esperada**:
```
Linux gxregistry 5.15.0-117-generic #127-Ubuntu SMP ... x86_64 x86_64 x86_64 GNU/Linux
```

**Copiar y pegar funciona**:
- Copia texto desde este documento
- Haz clic derecho en PowerShell para pegar
- Funciona perfectamente ✅

#### 22.5 Cerrar Sesión SSH

**Para salir de SSH**:
```bash
exit
```

O presiona `Ctrl+D`

**Vuelves a PowerShell de Windows**:
```
PS C:\Users\TuUsuario> _
```

**Reconectarte es fácil**:
```powershell
ssh -p 2222 gxapp@localhost
```

### Verificación

✅ **Conexión SSH exitosa desde Windows**
✅ **Puedes copiar/pegar comandos**
✅ **Conexión es rápida y estable**
✅ **Puedes reconectarte fácilmente**

### Solución de Problemas SSH

**Problema**: "Connection refused"

**Causa**: SSH no está corriendo en Ubuntu.

**Solución**:
1. Desde consola de VirtualBox (no SSH)
2. Ejecuta:
   ```bash
   sudo systemctl start ssh
   sudo systemctl enable ssh
   ```

**Problema**: "Connection timed out"

**Causa**: Port forwarding no configurado.

**Solución**:
1. Apaga la VM
2. VirtualBox → Configuración → Red
3. Verifica reglas de port forwarding (Paso 8)
4. Debe existir regla: SSH, TCP, 2222 → 22

**Problema**: "Permission denied (publickey)"

**Causa**: Autenticación por contraseña deshabilitada.

**Solución**:
1. Desde consola VirtualBox
2. Edita configuración SSH:
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
3. Busca y modifica:
   ```
   PasswordAuthentication yes
   ```
4. Guarda (`Ctrl+X`, `Y`, `Enter`)
5. Reinicia SSH:
   ```bash
   sudo systemctl restart ssh
   ```

---

# FASE 4: CONFIGURACIÓN INICIAL DEL SERVIDOR

---

## Paso 23: Actualizar Sistema Completamente

### Objetivo
Actualizar todos los paquetes del sistema a sus últimas versiones.

### Importancia
Es CRÍTICO actualizar el sistema antes de instalar software adicional para:
- ✅ Tener las últimas correcciones de seguridad
- ✅ Evitar conflictos de dependencias
- ✅ Tener versiones más recientes de paquetes base

### Procedimiento Detallado

#### 23.1 Conectarse por SSH

**Desde Windows PowerShell**:
```powershell
ssh -p 2222 gxapp@localhost
```

Ingresa tu contraseña cuando te la solicite.

**Deberías ver**:
```
gxapp@gxregistry:~$ _
```

#### 23.2 Actualizar Lista de Paquetes

**Ejecuta**:
```bash
sudo apt update
```

**Te pedirá contraseña**:
```
[sudo] password for gxapp: _
```

Escribe tu contraseña y presiona `Enter`.

**Qué hace**: Descarga la información de paquetes disponibles desde los repositorios.

**Salida esperada**:
```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
Get:3 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
...
Fetched 15.2 MB in 8s (1,890 kB/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
45 packages can be upgraded. Run 'apt list --upgradable' to see them.
```

**Importante**: Puede decir "X packages can be upgraded" (X paquetes pueden actualizarse).

#### 23.3 Ver Paquetes Actualizables (Opcional)

**Para ver qué se actualizará**:
```bash
apt list --upgradable
```

**Verás lista como**:
```
Listing... Done
base-files/jammy-updates 12ubuntu4.6 amd64 [upgradable from: 12ubuntu4.5]
curl/jammy-security 7.81.0-1ubuntu1.18 amd64 [upgradable from: 7.81.0-1ubuntu1.16]
...
```

No es necesario leer todo, solo para referencia.

#### 23.4 Actualizar Paquetes

**Ejecuta**:
```bash
sudo apt upgrade -y
```

**Qué hace**:
- `upgrade`: Actualiza paquetes instalados
- `-y`: Responde "yes" automáticamente a prompts

**Salida esperada**:
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
The following packages will be upgraded:
  base-files curl libcurl4 ...
45 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Need to get 125 MB of archives.
After this operation, 1,024 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 base-files amd64 12ubuntu4.6 [70.2 kB]
...
Fetching headers...
Downloading packages...
...
Unpacking ...
Setting up ...
```

**Duración**: 5-15 minutos dependiendo de cuántos paquetes haya que actualizar.

**Durante el proceso puede aparecer**:

**Pantalla de configuración de servicios**:
```
┌─────────── Configuring libssl1.1:amd64 ──────────────┐
│                                                       │
│ Services to restart to make them use the new         │
│ libraries:                                            │
│                                                       │
│ [*] ssh                                               │
│ [ ] systemd-logind                                    │
│                                                       │
│ <Ok>                                 <Cancel>         │
└───────────────────────────────────────────────────────┘
```

**Qué hacer**: Presiona `Tab` hasta `<Ok>` y presiona `Enter`.

**Mensaje sobre kernel**:
```
A new version of configuration file /etc/kernel/postinst.d/zz-update-grub is available,
but the version installed currently has been locally modified.
  1. install the package maintainer's version
  2. keep the local version currently installed
What would you like to do about it?
```

**Qué hacer**: Escribe `1` y presiona `Enter` (usar versión del mantenedor).

**Al finalizar verás**:
```
Processing triggers for ...
Processing triggers for man-db (2.10.2-1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
```

#### 23.5 Actualización Completa (Dist-Upgrade)

**Ejecuta**:
```bash
sudo apt dist-upgrade -y
```

**Qué hace**: Actualiza paquetes que requieren instalar/remover dependencias.

**Salida esperada**:
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

O puede instalar algunas actualizaciones adicionales.

#### 23.6 Limpiar Paquetes Innecesarios

**Ejecuta**:
```bash
sudo apt autoremove -y
```

**Qué hace**: Remueve paquetes que ya no son necesarios.

**Salida esperada**:
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

O puede remover algunos paquetes obsoletos.

#### 23.7 Limpiar Caché de Paquetes

**Ejecuta**:
```bash
sudo apt clean
```

**Qué hace**: Limpia archivos de paquetes descargados (libera espacio).

**No muestra salida** - es normal.

### Verificación

✅ **Sistema actualizado completamente**
✅ **Sin errores durante la actualización**
✅ **Paquetes innecesarios removidos**
✅ **Caché limpiada**

**Verificar que no haya paquetes pendientes**:
```bash
sudo apt update && apt list --upgradable
```

**Debería mostrar**:
```
All packages are up to date.
```

---

## Paso 24: Instalar Herramientas Básicas

### Objetivo
Instalar herramientas esenciales para desarrollo y administración.

### Procedimiento Detallado

#### 24.1 Instalar Build Essentials

**Ejecuta**:
```bash
sudo apt install -y build-essential
```

**Qué instala**:
- `gcc` - Compilador de C
- `g++` - Compilador de C++
- `make` - Herramienta de compilación
- Bibliotecas de desarrollo

**Necesario para**: Compilar paquetes de Python que requieren extensiones en C.

**Salida esperada**:
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  binutils cpp dpkg-dev g++ g++-11 gcc gcc-11 libc6-dev ...
...
Setting up build-essential (12.9ubuntu3) ...
```

**Duración**: 1-2 minutos.

#### 24.2 Instalar Herramientas de Red y Descarga

**Ejecuta**:
```bash
sudo apt install -y curl wget git net-tools
```

**Qué instala**:
- `curl` - Transferir datos con URLs
- `wget` - Descargar archivos
- `git` - Control de versiones
- `net-tools` - Herramientas de red (ifconfig, netstat, etc.)

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  curl git git-man liberror-perl net-tools wget
...
Setting up git (1:2.34.1-1ubuntu1.11) ...
```

**Verificar instalación**:
```bash
curl --version
git --version
```

**Salidas esperadas**:
```
curl 7.81.0 (x86_64-pc-linux-gnu) ...

git version 2.34.1
```

#### 24.3 Instalar Utilidades Adicionales

**Ejecuta**:
```bash
sudo apt install -y vim nano htop tree unzip zip
```

**Qué instala**:
- `vim` - Editor de texto avanzado
- `nano` - Editor de texto simple
- `htop` - Monitor de procesos interactivo
- `tree` - Visualizar estructura de directorios
- `unzip`, `zip` - Comprimir/descomprimir archivos

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  htop nano tree unzip vim vim-runtime zip
...
```

**Probar htop** (opcional):
```bash
htop
```

**Qué verás**: Monitor de procesos en tiempo real.

**Para salir**: Presiona `F10` o `q`.

#### 24.4 Instalar Bibliotecas de Desarrollo de Python

**Ejecuta**:
```bash
sudo apt install -y python3-dev python3-pip python3-venv
```

**Qué instala**:
- `python3-dev` - Archivos de desarrollo de Python
- `python3-pip` - Gestor de paquetes de Python
- `python3-venv` - Entornos virtuales de Python

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  python3-dev python3-pip python3-venv ...
...
Setting up python3-pip (22.0.2+dfsg-1ubuntu0.4) ...
```

**Verificar Python**:
```bash
python3 --version
pip3 --version
```

**Salidas esperadas**:
```
Python 3.10.12

pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```

#### 24.5 Instalar Dependencias de PostgreSQL

**Ejecuta**:
```bash
sudo apt install -y libpq-dev
```

**Qué instala**:
- `libpq-dev` - Bibliotecas de desarrollo de PostgreSQL

**Necesario para**: El paquete Python `psycopg2` (driver de PostgreSQL).

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  libpq-dev libpq5
...
```

### Verificación

✅ **build-essential instalado**
✅ **curl, wget, git instalados**
✅ **Editores (vim, nano) instalados**
✅ **Python 3.10+ con pip y venv**
✅ **libpq-dev instalado**

**Verificar todas las herramientas**:
```bash
which curl git python3 pip3
```

**Salida esperada**:
```
/usr/bin/curl
/usr/bin/git
/usr/bin/python3
/usr/bin/pip3
```

---

## Paso 25: Configurar Zona Horaria y Localización

### Objetivo
Configurar la zona horaria correcta para logs y timestamps.

### Procedimiento Detallado

#### 25.1 Ver Zona Horaria Actual

**Ejecuta**:
```bash
timedatectl
```

**Salida esperada**:
```
               Local time: Mon 2026-08-03 10:45:30 UTC
           Universal time: Mon 2026-08-03 10:45:30 UTC
                 RTC time: Mon 2026-08-03 10:45:30
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

**Zona horaria por defecto**: UTC (Coordinated Universal Time)

#### 25.2 Listar Zonas Horarias Disponibles

**Para América Latina**:
```bash
timedatectl list-timezones | grep America
```

**Verás**:
```
America/Argentina/Buenos_Aires
America/Bogota
America/Caracas
America/Lima
America/Mexico_City
America/Santiago
...
```

**Para Europa**:
```bash
timedatectl list-timezones | grep Europe
```

#### 25.3 Configurar Zona Horaria

**Ejemplo para México**:
```bash
sudo timedatectl set-timezone America/Mexico_City
```

**Ejemplo para Argentina**:
```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

**Ejemplo para España**:
```bash
sudo timedatectl set-timezone Europe/Madrid
```

**O mantener UTC** (recomendado para servidores):
```bash
sudo timedatectl set-timezone UTC
```

**Nota**: UTC es recomendado para servidores porque:
- No hay confusión con horarios de verano
- Logs consistentes
- Facilita coordinación internacional

**Verificar cambio**:
```bash
timedatectl
```

**Salida después del cambio** (ejemplo con Mexico_City):
```
               Local time: Mon 2026-08-03 04:45:30 CST
           Universal time: Mon 2026-08-03 10:45:30 UTC
                 RTC time: Mon 2026-08-03 10:45:30
                Time zone: America/Mexico_City (CST, -0600)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

#### 25.4 Configurar Locale (Opcional)

**Ver locales actuales**:
```bash
locale
```

**Salida esperada**:
```
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
...
```

**Si quieres español** (opcional):
```bash
sudo apt install -y language-pack-es
sudo update-locale LANG=es_ES.UTF-8
```

**Para mantener inglés** (recomendado):
No cambiar nada. Mantener `en_US.UTF-8`.

### Verificación

✅ **Zona horaria configurada correctamente**
✅ **NTP service activo** (reloj sincronizado)
✅ **Locale configurado**

---

# FASE 5: INSTALACIÓN DE POSTGRESQL

---

## Paso 26: Instalar PostgreSQL 15

### Objetivo
Instalar PostgreSQL 15, el sistema de base de datos para la aplicación.

### Procedimiento Detallado

#### 26.1 Verificar Repositorios de PostgreSQL

**Ubuntu 22.04 incluye PostgreSQL 14 por defecto**, pero queremos PostgreSQL 15+.

**Agregar repositorio oficial de PostgreSQL**:

```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

**Importar clave GPG del repositorio**:
```bash
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```

**Salida esperada**:
```
OK
```

**Actualizar lista de paquetes**:
```bash
sudo apt update
```

**Verás nuevos repositorios de PostgreSQL**:
```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://apt.postgresql.org/pub/repos/apt jammy-pgdg InRelease
...
```

#### 26.2 Instalar PostgreSQL 15

**Ejecuta**:
```bash
sudo apt install -y postgresql-15 postgresql-contrib-15
```

**Qué instala**:
- `postgresql-15` - Servidor PostgreSQL versión 15
- `postgresql-contrib-15` - Módulos adicionales

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  postgresql-15 postgresql-client-15 postgresql-client-common
  postgresql-common postgresql-contrib-15
...
Creating new PostgreSQL cluster 15/main ...
...
Ver Cluster Port Status Owner    Data directory              Log file
15  main    5432 online postgres /var/lib/postgresql/15/main /var/log/postgresql/postgresql-15-main.log
```

**Duración**: 2-3 minutos.

#### 26.3 Verificar Instalación

**Verificar versión**:
```bash
psql --version
```

**Salida esperada**:
```
psql (PostgreSQL) 15.8 (Ubuntu 15.8-1.pgdg22.04+1)
```

**Verificar que PostgreSQL está corriendo**:
```bash
sudo systemctl status postgresql
```

**Salida esperada**:
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Mon 2026-08-03 11:00:15 UTC; 2min ago
```

**Ver estado**: `Active: active (exited)` ✅

**Presiona** `q` para salir.

**Verificar puerto de escucha**:
```bash
sudo netstat -plunt | grep postgres
```

**Salida esperada**:
```
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      12345/postgres
tcp6       0      0 ::1:5432                :::*                    LISTEN      12345/postgres
```

**PostgreSQL escuchando en puerto 5432** ✅

### Verificación

✅ **PostgreSQL 15 instalado**
✅ **Servicio corriendo**
✅ **Escuchando en puerto 5432**
✅ **Habilitado para inicio automático**

---

## Paso 27: Configurar PostgreSQL

### Objetivo
Configurar PostgreSQL para la aplicación GeneXus Object Registry.

### Procedimiento Detallado

#### 27.1 Acceder a PostgreSQL como Usuario postgres

**Cambiar a usuario postgres**:
```bash
sudo -i -u postgres
```

**Prompt cambia a**:
```
postgres@gxregistry:~$ _
```

**Acceder a consola PostgreSQL**:
```bash
psql
```

**Prompt cambia a**:
```
postgres=# _
```

**¡Estás en la consola de PostgreSQL!** ✅

#### 27.2 Crear Usuario para la Aplicación

**Ejecuta en PostgreSQL**:
```sql
CREATE USER gxapp_user WITH PASSWORD 'GxApp2026!SecureDB';
```

**⚠️ IMPORTANTE**:
- Cambia `GxApp2026!SecureDB` por una contraseña SEGURA
- **ANOTA esta contraseña** - la necesitarás en el archivo `.env`

**Salida esperada**:
```
CREATE ROLE
```

**Verificar usuario creado**:
```sql
\du
```

**Salida esperada**:
```
                                   List of roles
 Role name  |                         Attributes                         | Member of
------------+------------------------------------------------------------+-----------
 gxapp_user |                                                            | {}
 postgres   | Superuser, Create role, Create DB, Replication, Bypass RLS| {}
```

#### 27.3 Crear Base de Datos

**Ejecuta en PostgreSQL**:
```sql
CREATE DATABASE gx_object_registry OWNER gxapp_user;
```

**Salida esperada**:
```
CREATE DATABASE
```

**Verificar base de datos creada**:
```sql
\l
```

**Verás lista de bases de datos**:
```
                                                List of databases
       Name        |    Owner    | Encoding |   Collate   |    Ctype    |   Access privileges
-------------------+-------------+----------+-------------+-------------+-----------------------
 gx_object_registry| gxapp_user  | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres          | postgres    | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0         | postgres    | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                   |             |          |             |             | postgres=CTc/postgres
 template1         | postgres    | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                   |             |          |             |             | postgres=CTc/postgres
```

#### 27.4 Otorgar Privilegios

**Conectarse a la nueva base de datos**:
```sql
\c gx_object_registry
```

**Salida**:
```
You are now connected to database "gx_object_registry" as user "postgres".
```

**Otorgar todos los privilegios**:
```sql
GRANT ALL PRIVILEGES ON DATABASE gx_object_registry TO gxapp_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO gxapp_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO gxapp_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO gxapp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gxapp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gxapp_user;
```

**Cada comando responderá**: `GRANT` o `ALTER DEFAULT PRIVILEGES`

#### 27.5 Salir de PostgreSQL

**Salir de consola psql**:
```sql
\q
```

**Vuelves a**:
```
postgres@gxregistry:~$ _
```

**Salir de usuario postgres**:
```bash
exit
```

**Vuelves a**:
```
gxapp@gxregistry:~$ _
```

### Verificación

✅ **Usuario gxapp_user creado**
✅ **Base de datos gx_object_registry creada**
✅ **Privilegios otorgados**

**Probar conexión** (desde usuario gxapp):
```bash
psql -h localhost -U gxapp_user -d gx_object_registry
```

**Te pedirá contraseña**:
```
Password for user gxapp_user: _
```

Ingresa la contraseña que configuraste.

**Si funciona, verás**:
```
psql (15.8)
Type "help" for help.

gx_object_registry=> _
```

**Salir**:
```sql
\q
```

✅ **Conexión exitosa**

---

## Paso 28: Configurar Autenticación de PostgreSQL (Opcional)

### Objetivo
Configurar PostgreSQL para permitir conexiones con contraseña desde localhost.

### ¿Es Necesario?

**Por defecto**, PostgreSQL en Ubuntu usa autenticación `peer` para conexiones locales:
- Funciona solo si el usuario Unix coincide con el usuario PostgreSQL
- Puede causar problemas con la aplicación

**Cambiaremos a** `md5` para autenticación por contraseña.

### Procedimiento Detallado

#### 28.1 Editar Archivo pg_hba.conf

**Abrir archivo de configuración**:
```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

**Qué verás**: Archivo de configuración de autenticación.

**Busca la sección** (cerca del final):
```
# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256
# IPv6 local connections:
host    all             all             ::1/128                 scram-sha-256
```

#### 28.2 Modificar Métodos de Autenticación

**Cambiar**:
```
local   all             all                                     peer
```

**Por**:
```
local   all             all                                     md5
```

**Y cambiar**:
```
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
```

**Por**:
```
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

**Después del cambio debería verse**:
```
# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

**Guardar archivo**:
1. Presiona `Ctrl + X`
2. Presiona `Y` (Yes)
3. Presiona `Enter`

#### 28.3 Reiniciar PostgreSQL

**Reiniciar servicio**:
```bash
sudo systemctl restart postgresql
```

**Verificar que reinició correctamente**:
```bash
sudo systemctl status postgresql
```

**Debe mostrar**: `Active: active (exited)`

### Verificación

✅ **pg_hba.conf modificado**
✅ **PostgreSQL reiniciado**
✅ **Autenticación md5 configurada**

**Probar conexión nuevamente**:
```bash
psql -h localhost -U gxapp_user -d gx_object_registry
```

Debería funcionar con contraseña. ✅

---

## Paso 29: Optimizar Configuración de PostgreSQL (Opcional)

### Objetivo
Ajustar configuración de PostgreSQL para mejor rendimiento.

### Cuándo Optimizar

**Para VM de desarrollo/prueba** (tu caso): Las configuraciones por defecto están bien.

**Para producción real**: Sí es recomendable optimizar.

### Configuraciones Básicas (Opcional)

#### 29.1 Editar postgresql.conf

**Abrir archivo**:
```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

**Buscar y modificar** (usa `Ctrl + W` para buscar):

**shared_buffers** (busca `shared_buffers`):
```
shared_buffers = 128MB
```

Cambiar a:
```
shared_buffers = 256MB
```

**effective_cache_size** (busca `effective_cache_size`):
```
#effective_cache_size = 4GB
```

Descomentar y cambiar a:
```
effective_cache_size = 2GB
```

**work_mem** (busca `work_mem`):
```
#work_mem = 4MB
```

Descomentar y cambiar a:
```
work_mem = 8MB
```

**Guardar**: `Ctrl + X`, `Y`, `Enter`

#### 29.2 Reiniciar PostgreSQL

```bash
sudo systemctl restart postgresql
```

### Verificación

✅ **Configuraciones optimizadas** (si decidiste hacerlo)
✅ **PostgreSQL reiniciado y funcionando**

**Nota**: Estas optimizaciones son opcionales y pueden omitirse para una VM de desarrollo.

---

## Paso 30: Backup Inicial de PostgreSQL (Opcional)

### Objetivo
Crear un script de backup automático para PostgreSQL.

### ¿Es Necesario Ahora?

**NO** - La base de datos está vacía. Lo haremos después de poblarla con datos.

**Puedes saltar este paso por ahora**.

### Verificación Final de PostgreSQL

**Verificar que todo está listo**:
```bash
sudo systemctl status postgresql
psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT version();"
```

**Salida esperada**:
```
Password for user gxapp_user: [ingresar contraseña]
                                                 version
---------------------------------------------------------------------------------------------------------
 PostgreSQL 15.8 (Ubuntu 15.8-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, 64-bit
(1 row)
```

✅ **PostgreSQL listo para la aplicación**

---

# FASE 6: INSTALACIÓN DEL PROYECTO GX OBJECT REGISTRY

---

## Paso 31: Clonar Repositorio del Proyecto

### Objetivo
Obtener el código fuente del proyecto desde el repositorio Git.

### Preparación

**¿Dónde está tu repositorio?**

**Opción A**: En GitHub/GitLab (repositorio remoto)
**Opción B**: En tu PC Windows (necesitarás transferirlo)
**Opción C**: No está en Git (crearás el proyecto manualmente)

**Para este tutorial**: Asumimos que **el código está en tu PC Windows** y lo transferiremos.

### Procedimiento Detallado

#### 31.1 Crear Directorio de Aplicaciones

**Desde SSH (como usuario gxapp)**:
```bash
cd ~
mkdir -p ~/apps
cd ~/apps
```

**Verificar ubicación**:
```bash
pwd
```

**Salida esperada**:
```
/home/gxapp/apps
```

#### 31.2 Transferir Proyecto desde Windows

**Opción 1: Usando Git (si tienes el proyecto en GitHub/GitLab)**

Si tu proyecto está en un repositorio remoto:
```bash
git clone https://github.com/TU_USUARIO/gx-object-registry.git
cd gx-object-registry
```

**Opción 2: Transferir con SCP desde Windows**

**En tu PC Windows**, abre PowerShell en el directorio del proyecto:
```powershell
cd C:\Users\operador\Proyectos\web\gx-object-registry
```

**Comprimir el proyecto** (excluyendo archivos innecesarios):
```powershell
# Crear un zip excluyendo venv, __pycache__, etc.
Compress-Archive -Path * -DestinationPath gx-object-registry.zip -Force
```

**Transferir a Ubuntu**:
```powershell
scp -P 2222 gx-object-registry.zip gxapp@localhost:/home/gxapp/apps/
```

**Te pedirá contraseña**. Ingrésala.

**En Ubuntu (desde SSH)**:
```bash
cd ~/apps
unzip gx-object-registry.zip -d gx-object-registry
cd gx-object-registry
```

**Opción 3: Crear proyecto manualmente**

Si prefieres crear todo desde cero:
```bash
cd ~/apps
mkdir gx-object-registry
cd gx-object-registry
```

Luego tendrás que crear todos los archivos manualmente o transferirlos uno por uno.

#### 31.3 Verificar Estructura del Proyecto

**Listar archivos**:
```bash
ls -la
```

**Deberías ver**:
```
total 48
drwxrwxr-x  8 gxapp gxapp 4096 Aug  3 12:00 .
drwxrwxr-x  3 gxapp gxapp 4096 Aug  3 11:55 ..
drwxrwxr-x  2 gxapp gxapp 4096 Aug  3 12:00 alembic
-rw-rw-r--  1 gxapp gxapp  156 Aug  3 12:00 alembic.ini
-rw-rw-r--  1 gxapp gxapp 1234 Aug  3 12:00 main.py
-rw-rw-r--  1 gxapp gxapp  512 Aug  3 12:00 requirements.txt
drwxrwxr-x  5 gxapp gxapp 4096 Aug  3 12:00 src
drwxrwxr-x  2 gxapp gxapp 4096 Aug  3 12:00 scripts
...
```

**Verificar estructura de carpetas**:
```bash
tree -L 2 -d
```

**O si tree no está instalado**:
```bash
find . -type d -maxdepth 2 | grep -v __pycache__ | sort
```

### Verificación

✅ **Proyecto copiado a** `/home/gxapp/apps/gx-object-registry`
✅ **Estructura de carpetas correcta**
✅ **Archivos principales presentes**: main.py, requirements.txt, alembic.ini

---

## Paso 32: Crear Entorno Virtual de Python

### Objetivo
Crear un entorno virtual aislado para las dependencias de Python.

### ¿Por Qué Entorno Virtual?

- ✅ Aísla dependencias del proyecto
- ✅ No interfiere con paquetes del sistema
- ✅ Fácil gestión de versiones
- ✅ Buena práctica en producción

### Procedimiento Detallado

#### 32.1 Verificar Python Instalado

```bash
python3 --version
```

**Salida esperada**:
```
Python 3.10.12
```

#### 32.2 Crear Entorno Virtual

**Desde el directorio del proyecto**:
```bash
cd ~/apps/gx-object-registry
python3 -m venv venv
```

**Qué hace**:
- Crea carpeta `venv` con Python aislado
- Incluye pip y setuptools

**Duración**: 10-20 segundos

**Verificar que se creó**:
```bash
ls -la venv
```

**Verás**:
```
total 20
drwxrwxr-x 5 gxapp gxapp 4096 Aug  3 12:05 .
drwxrwxr-x 9 gxapp gxapp 4096 Aug  3 12:05 ..
drwxrwxr-x 2 gxapp gxapp 4096 Aug  3 12:05 bin
drwxrwxr-x 2 gxapp gxapp 4096 Aug  3 12:05 include
drwxrwxr-x 3 gxapp gxapp 4096 Aug  3 12:05 lib
-rw-rw-r-- 1 gxapp gxapp   69 Aug  3 12:05 pyvenv.cfg
```

#### 32.3 Activar Entorno Virtual

```bash
source venv/bin/activate
```

**Prompt cambia a**:
```
(venv) gxapp@gxregistry:~/apps/gx-object-registry$ _
```

**Nota el prefijo** `(venv)` ✅

**Verificar pip del entorno virtual**:
```bash
which pip
```

**Salida esperada**:
```
/home/gxapp/apps/gx-object-registry/venv/bin/pip
```

#### 32.4 Actualizar pip y setuptools

```bash
pip install --upgrade pip setuptools wheel
```

**Salida esperada**:
```
Requirement already satisfied: pip in ./venv/lib/python3.10/site-packages (22.0.2)
Collecting pip
  Downloading pip-24.0-py3-none-any.whl (2.1 MB)
...
Successfully installed pip-24.0 setuptools-69.5.1 wheel-0.43.0
```

### Verificación

✅ **Entorno virtual creado**: venv/
✅ **Entorno activado**: Prompt muestra (venv)
✅ **pip actualizado** a última versión

**Desactivar** (si necesitas salir):
```bash
deactivate
```

**Prompt vuelve a**:
```
gxapp@gxregistry:~/apps/gx-object-registry$ _
```

**Reactivar** cuando lo necesites:
```bash
source venv/bin/activate
```

---

## Paso 33: Instalar Dependencias de Python

### Objetivo
Instalar todos los paquetes requeridos por la aplicación.

### Procedimiento Detallado

#### 33.1 Verificar Entorno Virtual Activo

**Asegúrate de que venv esté activo**:
```bash
source venv/bin/activate
```

**Prompt debe mostrar**: `(venv)`

#### 33.2 Verificar requirements.txt

```bash
cat requirements.txt
```

**Deberías ver** (versiones pueden variar):
```
fastapi==0.115.5
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
alembic==1.14.0
psycopg2-binary==2.9.10
pydantic==2.10.2
pydantic-settings==2.6.1
python-dotenv==1.0.1
python-multipart==0.0.17
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.2.1
jinja2==3.1.4
```

#### 33.3 Instalar Todas las Dependencias

```bash
pip install -r requirements.txt
```

**Qué hace**: Instala todos los paquetes listados en requirements.txt

**Salida esperada**:
```
Collecting fastapi==0.115.5
  Downloading fastapi-0.115.5-py3-none-any.whl (94 kB)
Collecting uvicorn[standard]==0.32.1
  Downloading uvicorn-0.32.1-py3-none-any.whl (63 kB)
...
Collecting psycopg2-binary==2.9.10
  Downloading psycopg2_binary-2.9.10-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
...
Installing collected packages: typing-extensions, sniffio, idna, h11, exceptiongroup, ...
Successfully installed alembic-1.14.0 annotated-types-0.7.0 anyio-4.6.2.post1 bcrypt-4.2.1 ...
```

**Duración**: 2-5 minutos (depende de conexión a Internet)

#### 33.4 Solución de Problemas Comunes

**Problema**: Error instalando `psycopg2-binary`

**Error**:
```
Error: pg_config executable not found.
```

**Solución**:
```bash
deactivate
sudo apt install -y libpq-dev python3-dev
source venv/bin/activate
pip install -r requirements.txt
```

**Problema**: Error con `bcrypt`

**Error**:
```
error: command 'gcc' failed
```

**Solución**:
```bash
deactivate
sudo apt install -y build-essential libffi-dev
source venv/bin/activate
pip install -r requirements.txt
```

#### 33.5 Verificar Instalación

**Listar paquetes instalados**:
```bash
pip list
```

**Salida esperada** (parcial):
```
Package              Version
-------------------- -----------
alembic              1.14.0
bcrypt               4.2.1
fastapi              0.115.5
psycopg2-binary      2.9.10
pydantic             2.10.2
sqlalchemy           2.0.36
uvicorn              0.32.1
...
```

**Verificar paquetes críticos**:
```bash
pip show fastapi psycopg2-binary sqlalchemy
```

Debe mostrar información de cada paquete.

### Verificación

✅ **requirements.txt presente**
✅ **Todas las dependencias instaladas sin errores**
✅ **FastAPI, SQLAlchemy, psycopg2 instalados correctamente**

---

## Paso 34: Configurar Variables de Entorno (.env)

### Objetivo
Crear archivo de configuración con variables de entorno de producción.

### Procedimiento Detallado

#### 34.1 Crear Archivo .env

**Desde el directorio del proyecto**:
```bash
cd ~/apps/gx-object-registry
nano .env
```

#### 34.2 Configurar Variables de Entorno

**Copia y pega el siguiente contenido** (ajusta los valores):

```env
# Entorno
ENVIRONMENT=production

# Base de datos
DATABASE_URL=postgresql+asyncpg://gxapp_user:GxApp2026!SecureDB@localhost/gx_object_registry

# Seguridad
SECRET_KEY=CAMBIA_ESTO_POR_UNA_CLAVE_SUPER_SEGURA_Y_ALEATORIA_DE_AL_MENOS_32_CARACTERES
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (orígenes permitidos)
CORS_ORIGINS=["http://localhost:8000","http://localhost:8080"]

# Logs
LOG_LEVEL=INFO
```

**⚠️ MUY IMPORTANTE - Personalizar**:

**DATABASE_URL**: Cambia la contraseña por la que configuraste en PostgreSQL (Paso 27.2)
```
postgresql+asyncpg://gxapp_user:TU_CONTRASEÑA_AQUI@localhost/gx_object_registry
```

**SECRET_KEY**: Genera una clave aleatoria segura.

**En otra terminal SSH** (mantén nano abierto), ejecuta:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Salida** (ejemplo):
```
xJ8_9kLmNpQrStUvWxYz0AbCdEfGhIjKlMnOpQrStUv
```

**Copia esa clave** y pégala en SECRET_KEY en el archivo .env.

**CORS_ORIGINS**: Ajusta según tu configuración:
```env
CORS_ORIGINS=["http://localhost:8080"]
```

#### 34.3 Guardar Archivo

**En nano**:
1. Presiona `Ctrl + X`
2. Presiona `Y`
3. Presiona `Enter`

#### 34.4 Proteger Archivo .env

**Cambiar permisos** (solo el dueño puede leer):
```bash
chmod 600 .env
```

**Verificar permisos**:
```bash
ls -l .env
```

**Salida esperada**:
```
-rw------- 1 gxapp gxapp 345 Aug  3 12:30 .env
```

**Los permisos** `-rw-------` significan:
- Dueño: leer y escribir
- Grupo: sin permisos
- Otros: sin permisos
✅ Seguro

#### 34.5 Verificar Configuración

**Ver contenido** (sin mostrar contraseñas):
```bash
grep -v PASSWORD .env | grep -v SECRET_KEY
```

**Debería mostrar**:
```
ENVIRONMENT=production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:8080"]
LOG_LEVEL=INFO
```

### Verificación

✅ **Archivo .env creado**
✅ **DATABASE_URL configurado con contraseña correcta**
✅ **SECRET_KEY generado y único**
✅ **Permisos seguros** (600)

---

## Paso 35: Configurar Alembic para Migraciones

### Objetivo
Configurar Alembic para gestionar migraciones de base de datos.

### Procedimiento Detallado

#### 35.1 Verificar alembic.ini

```bash
cat alembic.ini | grep sqlalchemy.url
```

**Salida esperada**:
```
sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Este es un placeholder**. Alembic leerá la URL real desde settings.py.

**No necesitas modificar alembic.ini** si tu proyecto ya está configurado para leer desde variables de entorno.

#### 35.2 Verificar Configuración de Alembic

**Revisar env.py**:
```bash
cat alembic/env.py | grep -A 5 "config.set_main_option"
```

**Deberías ver algo como**:
```python
from src.shared.config.settings import settings
# ...
config.set_main_option("sqlalchemy.url", settings.database_url)
```

Si tu proyecto está configurado así, **Alembic usará la URL del .env**. ✅

#### 35.3 Verificar Modelos Importados

**Alembic debe conocer todos los modelos** para detectar cambios.

**Revisar** `alembic/env.py`:
```bash
grep "target_metadata" alembic/env.py
```

**Debería verse**:
```python
from src.shared.infrastructure.database import Base
target_metadata = Base.metadata
```

O puede importar modelos específicamente:
```python
from src.auth.domain.user import User
from src.object_types.domain.object_type import ObjectType
from src.objects.domain.object import Object
# ...
target_metadata = Base.metadata
```

### Verificación

✅ **alembic.ini presente**
✅ **alembic/env.py configurado para usar .env**
✅ **Modelos importados correctamente**

---

## Paso 36: Ejecutar Migraciones de Base de Datos

### Objetivo
Crear las tablas en la base de datos usando Alembic.

### Procedimiento Detallado

#### 36.1 Verificar Conexión a Base de Datos

**Probar conexión**:
```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT 1;"
```

**Ingresar contraseña** cuando lo solicite.

**Salida esperada**:
```
 ?column?
----------
        1
(1 row)
```

✅ **Conexión exitosa**

#### 36.2 Ver Migraciones Disponibles

**Con entorno virtual activo**:
```bash
source venv/bin/activate
alembic history
```

**Salida esperada** (ejemplo):
```
<base> -> 001_initial (head), Initial migration
```

O puede mostrar varias migraciones:
```
<base> -> 001_initial, Initial migration
001_initial -> 002_add_objects, Add objects table
002_add_objects -> 003_add_users (head), Add users table
```

#### 36.3 Ver Estado Actual

```bash
alembic current
```

**Salida esperada** (si no se han aplicado migraciones):
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

Sin output de revisión = base de datos vacía.

#### 36.4 Aplicar Todas las Migraciones

```bash
alembic upgrade head
```

**Qué hace**: Aplica todas las migraciones pendientes hasta la más reciente.

**Salida esperada**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial, Initial migration
INFO  [alembic.runtime.migration] Running upgrade 001_initial -> 002_add_objects, Add objects table
INFO  [alembic.runtime.migration] Running upgrade 002_add_objects -> 003_add_users, Add users table
```

**Duración**: 5-10 segundos

#### 36.5 Verificar Migraciones Aplicadas

```bash
alembic current
```

**Salida esperada**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
003_add_users (head)
```

✅ **Todas las migraciones aplicadas**

#### 36.6 Verificar Tablas Creadas

```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "\dt"
```

**Salida esperada**:
```
Password for user gxapp_user: [ingresar contraseña]
                List of relations
 Schema |       Name        | Type  |   Owner
--------+-------------------+-------+------------
 public | alembic_version   | table | gxapp_user
 public | object_types      | table | gxapp_user
 public | objects           | table | gxapp_user
 public | users             | table | gxapp_user
(4 rows)
```

✅ **Tablas creadas correctamente**

**Ver estructura de tabla** (ejemplo: users):
```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "\d users"
```

**Salida esperada**:
```
                                      Table "public.users"
    Column     |            Type             | Collation | Nullable |      Default
---------------+-----------------------------+-----------+----------+-------------------
 id            | uuid                        |           | not null |
 username      | character varying(50)       |           | not null |
 email         | character varying(255)      |           | not null |
 hashed_password| character varying(255)     |           | not null |
 full_name     | character varying(255)      |           |          |
 is_active     | boolean                     |           | not null | true
 created_at    | timestamp without time zone |           | not null |
 updated_at    | timestamp without time zone |           | not null |
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "ix_users_email" UNIQUE, btree (email)
    "ix_users_username" UNIQUE, btree (username)
```

### Verificación

✅ **Migraciones aplicadas exitosamente**
✅ **Tablas creadas**: object_types, objects, users, alembic_version
✅ **Esquema de base de datos correcto**

---

## Paso 37: Crear Datos Iniciales (Seed)

### Objetivo
Poblar la base de datos con tipos de objeto iniciales.

### Procedimiento Detallado

#### 37.1 Verificar Script de Seed

```bash
cat scripts/seed_database.py | head -20
```

**Deberías ver** el script que crea tipos de objeto.

#### 37.2 Ejecutar Script de Seed

**Con entorno virtual activo**:
```bash
source venv/bin/activate
python scripts/seed_database.py
```

**Salida esperada**:
```
🌱 Iniciando seed de tipos de objeto...
📊 Base de datos: localhost/gx_object_registry

✅ Creado: PROCEDURE (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: TRANSACTION (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: DATA_PROVIDER (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: WEB_PANEL (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: WORK_WITH (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: DASHBOARD (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: SD_PANEL (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: MASTER_PAGE (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: THEME (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: DOMAIN (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: IMAGE (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
✅ Creado: STYLE (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

✨ Seed completado:
   • Creados: 12
   • Ya existían: 0
   • Total: 12
```

#### 37.3 Verificar Datos en Base de Datos

```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT * FROM object_types;"
```

**Salida esperada**:
```
                  id                  |     name      |         created_at
--------------------------------------+---------------+---------------------------
 xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | PROCEDURE     | 2026-08-03 12:45:30.123456
 xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | TRANSACTION   | 2026-08-03 12:45:30.234567
 xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | DATA_PROVIDER | 2026-08-03 12:45:30.345678
 ...
(12 rows)
```

✅ **12 tipos de objeto creados**

### Verificación

✅ **Script de seed ejecutado sin errores**
✅ **12 tipos de objeto en la base de datos**

---

## Paso 38: Crear Usuario Administrador

### Objetivo
Crear el primer usuario administrador para acceder al sistema.

### Procedimiento Detallado

#### 38.1 Verificar Script create_admin.py

```bash
cat scripts/create_admin.py | head -30
```

**Deberías ver** el script interactivo para crear usuarios.

#### 38.2 Ejecutar Script

**Con entorno virtual activo**:
```bash
python scripts/create_admin.py
```

**El script mostrará**:
```
============================================================
  CREAR USUARIO ADMINISTRADOR
============================================================

Ingresa los datos del nuevo usuario:
------------------------------------------------------------
Username (3-50 caracteres): _
```

#### 38.3 Ingresar Datos del Usuario

**Username**:
```
admin
```

**Email**:
```
admin@gxregistry.local
```

**Nombre completo** (opcional):
```
Administrador del Sistema
```

**Contraseña** (no se verá al escribir):
```
[TuContraseñaSuperSegura123!]
```

**Confirmar contraseña**:
```
[TuContraseñaSuperSegura123!]
```

**⚠️ IMPORTANTE**: **ANOTA estas credenciales**. Las necesitarás para acceder al sistema.

#### 38.4 Confirmar Creación

```
------------------------------------------------------------
Datos del usuario:
  Username:  admin
  Email:     admin@gxregistry.local
  Nombre:    Administrador del Sistema
------------------------------------------------------------

¿Crear este usuario? (S/n): S
```

Escribe `S` y presiona `Enter`.

**Salida esperada**:
```
Creando usuario...

✅ Usuario creado exitosamente!

============================================================
  CREDENCIALES DE ACCESO
============================================================
  Username:  admin
  Email:     admin@gxregistry.local
  Nombre:    Administrador del Sistema
  ID:        xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
============================================================

Puedes iniciar sesión en: http://localhost:8000/web/login
```

#### 38.5 Verificar Usuario en Base de Datos

```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT username, email, full_name, is_active FROM users;"
```

**Salida esperada**:
```
 username |          email           |         full_name          | is_active
----------+--------------------------+----------------------------+-----------
 admin    | admin@gxregistry.local   | Administrador del Sistema  | t
(1 row)
```

✅ **Usuario administrador creado**

### Verificación

✅ **Usuario admin creado exitosamente**
✅ **Credenciales anotadas**
✅ **Usuario visible en base de datos**

---

## Paso 39: Probar Aplicación en Modo Desarrollo

### Objetivo
Verificar que la aplicación funciona correctamente antes de configurar producción.

### Procedimiento Detallado

#### 39.1 Iniciar Servidor de Desarrollo

**Con entorno virtual activo**:
```bash
cd ~/apps/gx-object-registry
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Qué hace**:
- Inicia el servidor Uvicorn
- Escucha en todas las interfaces (0.0.0.0)
- Puerto 8000

**Salida esperada**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Servidor corriendo**

**NO cierres esta terminal**. Déjala corriendo.

#### 39.2 Probar desde Windows

**En tu navegador Windows**, abre:
```
http://localhost:8000
```

**Deberías ver**: La página de inicio de la aplicación.

**Probar documentación API**:
```
http://localhost:8000/docs
```

**Deberías ver**: Documentación interactiva de Swagger UI.

#### 39.3 Probar Login

**Acceder a login**:
```
http://localhost:8000/web/login
```

**Ingresar credenciales**:
- **Username**: `admin`
- **Password**: [la que creaste]

**Si funciona**: ✅ Serás redirigido al dashboard

#### 39.4 Detener Servidor

**En la terminal SSH donde corre Uvicorn**:

Presiona `Ctrl + C`

**Salida**:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12345]
```

### Verificación

✅ **Aplicación inicia sin errores**
✅ **Accesible desde navegador Windows**
✅ **API Docs funcionando** (/docs)
✅ **Login funcionando correctamente**

---

## Paso 40: Preparar para Producción

### Objetivo
Realizar ajustes finales antes de configurar servicios de producción.

### Procedimiento Detallado

#### 40.1 Crear Directorio de Logs

```bash
mkdir -p ~/apps/gx-object-registry/logs
chmod 755 ~/apps/gx-object-registry/logs
```

#### 40.2 Crear Script de Inicio

**Crear script**:
```bash
nano ~/apps/gx-object-registry/start.sh
```

**Contenido**:
```bash
#!/bin/bash

# Activar entorno virtual
source /home/gxapp/apps/gx-object-registry/venv/bin/activate

# Iniciar aplicación con Gunicorn
cd /home/gxapp/apps/gx-object-registry
exec gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Hacer ejecutable**:
```bash
chmod +x ~/apps/gx-object-registry/start.sh
```

#### 40.3 Instalar Gunicorn

**Con entorno virtual activo**:
```bash
source venv/bin/activate
pip install gunicorn
```

**Salida esperada**:
```
Collecting gunicorn
  Downloading gunicorn-21.2.0-py3-none-any.whl (80 kB)
...
Successfully installed gunicorn-21.2.0
```

#### 40.4 Probar Script de Inicio

```bash
./start.sh
```

**Debería iniciar** con Gunicorn.

**Detener**: `Ctrl+C`

### Verificación

✅ **Directorio de logs creado**
✅ **Script start.sh creado y ejecutable**
✅ **Gunicorn instalado**
✅ **Script de inicio funciona**

---

# FASE 7: CONFIGURACIÓN DE PRODUCCIÓN

---

## Paso 41: Configurar Servicio Systemd

### Objetivo
Configurar la aplicación como servicio del sistema para que inicie automáticamente.

### ¿Por Qué Systemd?

- ✅ Inicia automáticamente al arrancar el servidor
- ✅ Reinicia automáticamente si la aplicación falla
- ✅ Gestión centralizada de servicios
- ✅ Logs integrados con journalctl

### Procedimiento Detallado

#### 41.1 Crear Archivo de Servicio

**Crear archivo**:
```bash
sudo nano /etc/systemd/system/gxregistry.service
```

**Contenido del archivo**:
```ini
[Unit]
Description=GeneXus Object Registry - FastAPI Application
After=network.target postgresql.service

[Service]
Type=exec
User=gxapp
Group=gxapp
WorkingDirectory=/home/gxapp/apps/gx-object-registry
Environment="PATH=/home/gxapp/apps/gx-object-registry/venv/bin"
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info

Restart=always
RestartSec=10

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Explicación de configuraciones**:

| Opción | Descripción |
|--------|-------------|
| `After=postgresql.service` | Espera a que PostgreSQL inicie |
| `User=gxapp` | Ejecuta como usuario gxapp |
| `WorkingDirectory` | Directorio del proyecto |
| `ExecStart` | Comando para iniciar la aplicación |
| `Restart=always` | Reinicia si falla |
| `RestartSec=10` | Espera 10s antes de reiniciar |

**Guardar**: `Ctrl+X`, `Y`, `Enter`

#### 41.2 Recargar Systemd

```bash
sudo systemctl daemon-reload
```

**Qué hace**: Recarga la configuración de systemd para reconocer el nuevo servicio.

#### 41.3 Habilitar Servicio

```bash
sudo systemctl enable gxregistry.service
```

**Salida esperada**:
```
Created symlink /etc/systemd/system/multi-user.target.wants/gxregistry.service → /etc/systemd/system/gxregistry.service.
```

**Qué hace**: Configura el servicio para iniciar automáticamente al arrancar.

#### 41.4 Iniciar Servicio

```bash
sudo systemctl start gxregistry.service
```

**Sin salida** = éxito ✅

#### 41.5 Verificar Estado del Servicio

```bash
sudo systemctl status gxregistry.service
```

**Salida esperada**:
```
● gxregistry.service - GeneXus Object Registry - FastAPI Application
     Loaded: loaded (/etc/systemd/system/gxregistry.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2026-08-03 13:00:15 UTC; 10s ago
   Main PID: 23456 (gunicorn)
      Tasks: 5 (limit: 4556)
     Memory: 125.5M
        CPU: 2.341s
     CGroup: /system.slice/gxregistry.service
             ├─23456 /home/gxapp/apps/gx-object-registry/venv/bin/python3 /home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app...
             ├─23457 /home/gxapp/apps/gx-object-registry/venv/bin/python3 /home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app...
             ├─23458 /home/gxapp/apps/gx-object-registry/venv/bin/python3 /home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app...
             ├─23459 /home/gxapp/apps/gx-object-registry/venv/bin/python3 /home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app...
             └─23460 /home/gxapp/apps/gx-object-registry/venv/bin/python3 /home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app...

Aug 03 13:00:15 gxregistry systemd[1]: Started GeneXus Object Registry - FastAPI Application.
Aug 03 13:00:16 gxregistry gunicorn[23456]: [2026-08-03 13:00:16 +0000] [23456] [INFO] Starting gunicorn 21.2.0
Aug 03 13:00:16 gxregistry gunicorn[23456]: [2026-08-03 13:00:16 +0000] [23456] [INFO] Listening at: http://0.0.0.0:8000 (23456)
Aug 03 13:00:16 gxregistry gunicorn[23456]: [2026-08-03 13:00:16 +0000] [23456] [INFO] Using worker: uvicorn.workers.UvicornWorker
```

**Ver**:
- ✅ `Active: active (running)` - Servicio corriendo
- ✅ `enabled` - Inicia automáticamente
- ✅ `4 workers` corriendo

**Presiona** `q` para salir.

#### 41.6 Ver Logs en Tiempo Real

```bash
sudo journalctl -u gxregistry.service -f
```

**Qué hace**: Muestra logs del servicio en tiempo real.

**Para salir**: `Ctrl+C`

### Comandos Útiles del Servicio

**Detener servicio**:
```bash
sudo systemctl stop gxregistry.service
```

**Reiniciar servicio**:
```bash
sudo systemctl restart gxregistry.service
```

**Ver logs recientes**:
```bash
sudo journalctl -u gxregistry.service -n 50
```

**Ver logs desde hoy**:
```bash
sudo journalctl -u gxregistry.service --since today
```

### Verificación

✅ **Servicio creado**: /etc/systemd/system/gxregistry.service
✅ **Servicio habilitado** para inicio automático
✅ **Servicio corriendo** en puerto 8000
✅ **Workers funcionando** (4 procesos)

**Probar desde Windows**:
```
http://localhost:8000
```

Debería funcionar ✅

---

## Paso 42: Instalar y Configurar Nginx

### Objetivo
Instalar Nginx como proxy reverso para la aplicación.

### ¿Por Qué Nginx?

- ✅ Mejor manejo de conexiones HTTP
- ✅ Sirve archivos estáticos eficientemente
- ✅ Compresión gzip
- ✅ HTTPS con certificados SSL
- ✅ Caché de respuestas

### Procedimiento Detallado

#### 42.1 Instalar Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

**Salida esperada**:
```
Reading package lists... Done
...
The following NEW packages will be installed:
  nginx nginx-common nginx-core
...
Setting up nginx (1.18.0-0ubuntu1.4) ...
```

#### 42.2 Verificar Instalación

```bash
nginx -v
```

**Salida esperada**:
```
nginx version: nginx/1.18.0 (Ubuntu)
```

**Verificar estado**:
```bash
sudo systemctl status nginx
```

**Debe mostrar**: `Active: active (running)` ✅

#### 42.3 Crear Configuración de Sitio

**Eliminar sitio por defecto** (opcional):
```bash
sudo rm /etc/nginx/sites-enabled/default
```

**Crear configuración para la aplicación**:
```bash
sudo nano /etc/nginx/sites-available/gxregistry
```

**Contenido**:
```nginx
server {
    listen 80;
    server_name _;

    # Logs
    access_log /var/log/nginx/gxregistry-access.log;
    error_log /var/log/nginx/gxregistry-error.log;

    # Tamaño máximo de archivos
    client_max_body_size 10M;

    # Proxy a la aplicación FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Servir archivos estáticos (si los hay)
    location /static/ {
        alias /home/gxapp/apps/gx-object-registry/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Compresión gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

#### 42.4 Habilitar Sitio

**Crear enlace simbólico**:
```bash
sudo ln -s /etc/nginx/sites-available/gxregistry /etc/nginx/sites-enabled/
```

**Verificar sintaxis de configuración**:
```bash
sudo nginx -t
```

**Salida esperada**:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

✅ **Configuración correcta**

#### 42.5 Reiniciar Nginx

```bash
sudo systemctl restart nginx
```

**Verificar estado**:
```bash
sudo systemctl status nginx
```

**Debe mostrar**: `Active: active (running)` ✅

### Verificación

✅ **Nginx instalado y corriendo**
✅ **Configuración creada y habilitada**
✅ **Proxy reverso configurado**

**Probar desde Windows** (puerto 80 → 8080 por port forwarding):
```
http://localhost:8080
```

Debería mostrar la aplicación ✅

---

## Paso 43: Configurar Firewall UFW

### Objetivo
Configurar el firewall para permitir solo tráfico necesario.

### Procedimiento Detallado

#### 43.1 Verificar UFW

```bash
sudo ufw status
```

**Salida esperada**:
```
Status: inactive
```

#### 43.2 Configurar Reglas Predeterminadas

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Qué hace**:
- Bloquea todo tráfico entrante por defecto
- Permite todo tráfico saliente

#### 43.3 Permitir SSH

**MUY IMPORTANTE**: Antes de habilitar UFW, permitir SSH:

```bash
sudo ufw allow 22/tcp comment 'SSH'
```

**Salida**:
```
Rules updated
Rules updated (v6)
```

#### 43.4 Permitir HTTP y HTTPS

```bash
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
```

#### 43.5 Permitir Puerto de Aplicación (Opcional)

Si quieres acceso directo al puerto 8000:
```bash
sudo ufw allow 8000/tcp comment 'GX Registry App'
```

#### 43.6 Habilitar Firewall

```bash
sudo ufw enable
```

**Advertencia**:
```
Command may disrupt existing ssh connections. Proceed with operation (y|n)? _
```

**Escribe**: `y` y presiona `Enter`

**Salida**:
```
Firewall is active and enabled on system startup
```

#### 43.7 Verificar Reglas

```bash
sudo ufw status numbered
```

**Salida esperada**:
```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere                   # SSH
[ 2] 80/tcp                     ALLOW IN    Anywhere                   # HTTP
[ 3] 443/tcp                    ALLOW IN    Anywhere                   # HTTPS
[ 4] 8000/tcp                   ALLOW IN    Anywhere                   # GX Registry App
[ 5] 22/tcp (v6)                ALLOW IN    Anywhere (v6)              # SSH
[ 6] 80/tcp (v6)                ALLOW IN    Anywhere (v6)              # HTTP
[ 7] 443/tcp (v6)               ALLOW IN    Anywhere (v6)              # HTTPS
[ 8] 8000/tcp (v6)              ALLOW IN    Anywhere (v6)              # GX Registry App
```

### Verificación

✅ **UFW habilitado**
✅ **SSH permitido** (puerto 22)
✅ **HTTP permitido** (puerto 80)
✅ **HTTPS permitido** (puerto 443)
✅ **App directa permitida** (puerto 8000)

**Probar que SSH sigue funcionando**:

Desde Windows:
```powershell
ssh -p 2222 gxapp@localhost
```

Debería conectarse normalmente ✅

---

## Paso 44: Optimizar Configuración de Producción

### Objetivo
Ajustar configuraciones para mejor rendimiento y seguridad.

### Procedimiento Detallado

#### 44.1 Ajustar Configuración de Gunicorn

**Editar archivo de servicio**:
```bash
sudo nano /etc/systemd/system/gxregistry.service
```

**Modificar línea ExecStart**:

**Antes**:
```
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info
```

**Después** (agregar más opciones):
```
ExecStart=/home/gxapp/apps/gx-object-registry/venv/bin/gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50
```

**Cambios importantes**:
- `--bind 127.0.0.1:8000` → Solo escucha localhost (más seguro, Nginx hace proxy)
- `--timeout 120` → Timeout de 2 minutos
- `--max-requests 1000` → Reinicia worker cada 1000 requests (evita memory leaks)

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Recargar y reiniciar**:
```bash
sudo systemctl daemon-reload
sudo systemctl restart gxregistry.service
```

#### 44.2 Configurar Nginx para Better Performance

**Editar configuración de Nginx**:
```bash
sudo nano /etc/nginx/sites-available/gxregistry
```

**Agregar configuraciones adicionales**:

Después de `gzip_types`, agregar:
```nginx
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate limiting zone (prevenir abusos)
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
```

**Guardar**, verificar sintaxis y reiniciar:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

#### 44.3 Configurar Logrotate

**Crear configuración para logs de la aplicación**:
```bash
sudo nano /etc/logrotate.d/gxregistry
```

**Contenido**:
```
/home/gxapp/apps/gx-object-registry/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 gxapp gxapp
    sharedscripts
    postrotate
        systemctl reload gxregistry.service > /dev/null 2>&1 || true
    endscript
}
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Qué hace**:
- Rota logs diariamente
- Mantiene 14 días de logs
- Comprime logs antiguos
- Recarga el servicio después de rotar

### Verificación

✅ **Gunicorn optimizado**
✅ **Nginx con headers de seguridad**
✅ **Logrotate configurado**

---

## Paso 45: Configurar Backups Automáticos

### Objetivo
Crear script de backup automático para base de datos.

### Procedimiento Detallado

#### 45.1 Crear Directorio de Backups

```bash
mkdir -p ~/backups/database
chmod 700 ~/backups
```

#### 45.2 Crear Script de Backup

```bash
nano ~/backups/backup_database.sh
```

**Contenido**:
```bash
#!/bin/bash

# Configuración
DB_NAME="gx_object_registry"
DB_USER="gxapp_user"
BACKUP_DIR="/home/gxapp/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/gxregistry_$DATE.sql.gz"
KEEP_DAYS=7

# Exportar contraseña (lee desde .env)
export PGPASSWORD="GxApp2026!SecureDB"  # ⚠️ CAMBIAR POR TU CONTRASEÑA

# Crear backup
echo "🔄 Iniciando backup de base de datos..."
pg_dump -h localhost -U $DB_USER -d $DB_NAME | gzip > $BACKUP_FILE

# Verificar éxito
if [ $? -eq 0 ]; then
    echo "✅ Backup completado: $BACKUP_FILE"

    # Eliminar backups antiguos
    find $BACKUP_DIR -name "gxregistry_*.sql.gz" -type f -mtime +$KEEP_DAYS -delete
    echo "🧹 Backups antiguos eliminados (más de $KEEP_DAYS días)"
else
    echo "❌ Error en backup"
    exit 1
fi

# Limpiar variable de contraseña
unset PGPASSWORD

echo "✨ Proceso completado"
```

**⚠️ IMPORTANTE**: Cambia `GxApp2026!SecureDB` por tu contraseña real de PostgreSQL.

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Hacer ejecutable**:
```bash
chmod 700 ~/backups/backup_database.sh
```

#### 45.3 Probar Script de Backup

```bash
~/backups/backup_database.sh
```

**Salida esperada**:
```
🔄 Iniciando backup de base de datos...
✅ Backup completado: /home/gxapp/backups/database/gxregistry_20260803_130000.sql.gz
🧹 Backups antiguos eliminados (más de 7 días)
✨ Proceso completado
```

**Verificar backup creado**:
```bash
ls -lh ~/backups/database/
```

**Verás**:
```
total 4.0K
-rw-r--r-- 1 gxapp gxapp 2.3K Aug  3 13:00 gxregistry_20260803_130000.sql.gz
```

✅ **Backup creado**

#### 45.4 Configurar Cron para Backups Automáticos

**Editar crontab**:
```bash
crontab -e
```

**Si es primera vez**, te preguntará editor. Elige `1` (nano).

**Agregar al final**:
```cron
# Backup de base de datos diario a las 2:00 AM
0 2 * * * /home/gxapp/backups/backup_database.sh >> /home/gxapp/backups/backup.log 2>&1
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Verificar cron**:
```bash
crontab -l
```

**Debe mostrar**:
```
# Backup de base de datos diario a las 2:00 AM
0 2 * * * /home/gxapp/backups/backup_database.sh >> /home/gxapp/backups/backup.log 2>&1
```

### Verificación

✅ **Script de backup creado**
✅ **Backup manual funciona**
✅ **Cron configurado** para backups diarios

---

## Paso 46: Crear Script de Restauración

### Objetivo
Crear script para restaurar base de datos desde backup.

### Procedimiento Detallado

#### 46.1 Crear Script de Restauración

```bash
nano ~/backups/restore_database.sh
```

**Contenido**:
```bash
#!/bin/bash

# Verificar argumento
if [ -z "$1" ]; then
    echo "❌ Uso: $0 <archivo_backup.sql.gz>"
    echo ""
    echo "Backups disponibles:"
    ls -1 /home/gxapp/backups/database/*.sql.gz 2>/dev/null || echo "  No hay backups"
    exit 1
fi

BACKUP_FILE="$1"

# Verificar que archivo existe
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Archivo no encontrado: $BACKUP_FILE"
    exit 1
fi

# Configuración
DB_NAME="gx_object_registry"
DB_USER="gxapp_user"
export PGPASSWORD="GxApp2026!SecureDB"  # ⚠️ CAMBIAR POR TU CONTRASEÑA

echo "⚠️  ADVERTENCIA: Esta operación eliminará todos los datos actuales"
echo "📁 Archivo: $BACKUP_FILE"
echo ""
read -p "¿Continuar? (escriba 'SI' para confirmar): " confirm

if [ "$confirm" != "SI" ]; then
    echo "❌ Restauración cancelada"
    exit 0
fi

echo ""
echo "🔄 Deteniendo aplicación..."
sudo systemctl stop gxregistry.service

echo "🔄 Eliminando base de datos actual..."
psql -h localhost -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "🔄 Creando nueva base de datos..."
psql -h localhost -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

echo "🔄 Restaurando backup..."
gunzip -c "$BACKUP_FILE" | psql -h localhost -U $DB_USER -d $DB_NAME

if [ $? -eq 0 ]; then
    echo "✅ Restauración completada exitosamente"
else
    echo "❌ Error en la restauración"
    exit 1
fi

echo "🔄 Reiniciando aplicación..."
sudo systemctl start gxregistry.service

unset PGPASSWORD

echo "✨ Proceso completado"
```

**⚠️ IMPORTANTE**: Cambia la contraseña.

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Hacer ejecutable**:
```bash
chmod 700 ~/backups/restore_database.sh
```

### Uso del Script de Restauración

**Listar backups disponibles**:
```bash
ls -lh ~/backups/database/
```

**Restaurar desde un backup**:
```bash
~/backups/restore_database.sh ~/backups/database/gxregistry_20260803_130000.sql.gz
```

**Te pedirá confirmación**. Escribe `SI` para continuar.

### Verificación

✅ **Script de restauración creado**
✅ **Puede listar backups disponibles**
✅ **Listo para restaurar si es necesario**

---

## Paso 47: Monitoreo Básico del Sistema

### Objetivo
Configurar herramientas básicas de monitoreo.

### Procedimiento Detallado

#### 47.1 Instalar Herramientas de Monitoreo

```bash
sudo apt install -y htop iotop ncdu
```

**Qué instala**:
- `htop` - Monitor de procesos interactivo
- `iotop` - Monitor de I/O de disco
- `ncdu` - Analizador de uso de disco

#### 47.2 Crear Script de Estado del Sistema

```bash
nano ~/check_system.sh
```

**Contenido**:
```bash
#!/bin/bash

echo "═══════════════════════════════════════════════════════"
echo "  ESTADO DEL SISTEMA - GX Registry"
echo "═══════════════════════════════════════════════════════"
echo ""

# Servicio de aplicación
echo "📦 Servicio GX Registry:"
systemctl is-active --quiet gxregistry.service && echo "  ✅ Corriendo" || echo "  ❌ Detenido"

# PostgreSQL
echo ""
echo "🗄️  PostgreSQL:"
systemctl is-active --quiet postgresql && echo "  ✅ Corriendo" || echo "  ❌ Detenido"

# Nginx
echo ""
echo "🌐 Nginx:"
systemctl is-active --quiet nginx && echo "  ✅ Corriendo" || echo "  ❌ Detenido"

# Uso de disco
echo ""
echo "💾 Uso de disco:"
df -h / | tail -1 | awk '{print "  Usado: "$3" / "$2" ("$5")"}'

# Uso de memoria
echo ""
echo "🧠 Uso de memoria:"
free -h | grep Mem | awk '{print "  Usado: "$3" / "$2}'

# Carga del sistema
echo ""
echo "⚡ Carga del sistema:"
uptime | awk -F'load average:' '{print "  "$2}'

# Últimos errores en logs
echo ""
echo "📋 Últimos errores (si hay):"
sudo journalctl -u gxregistry.service -p err -n 5 --no-pager --since "1 hour ago" 2>/dev/null || echo "  Sin errores recientes"

echo ""
echo "═══════════════════════════════════════════════════════"
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

**Hacer ejecutable**:
```bash
chmod +x ~/check_system.sh
```

#### 47.3 Probar Script

```bash
~/check_system.sh
```

**Salida esperada**:
```
═══════════════════════════════════════════════════════════
  ESTADO DEL SISTEMA - GX Registry
═══════════════════════════════════════════════════════════

📦 Servicio GX Registry:
  ✅ Corriendo

🗄️  PostgreSQL:
  ✅ Corriendo

🌐 Nginx:
  ✅ Corriendo

💾 Uso de disco:
  Usado: 5.2G / 29G (19%)

🧠 Uso de memoria:
  Usado: 1.2G / 3.8G

⚡ Carga del sistema:
   0.15, 0.20, 0.18

📋 Últimos errores (si hay):
  Sin errores recientes

═══════════════════════════════════════════════════════════
```

### Verificación

✅ **Herramientas de monitoreo instaladas**
✅ **Script de estado creado y funcionando**

---

## Paso 48: Documentar Configuración

### Objetivo
Crear archivo con información importante del sistema.

### Procedimiento Detallado

#### 48.1 Crear Archivo de Documentación

```bash
nano ~/SISTEMA.md
```

**Contenido**:
```markdown
# GeneXus Object Registry - Información del Sistema

## Servidor

- **Hostname**: gxregistry
- **OS**: Ubuntu 22.04.5 LTS
- **IP**: 10.0.2.15 (NAT)
- **Usuario**: gxapp

## Aplicación

- **Ubicación**: /home/gxapp/apps/gx-object-registry
- **Python**: 3.10.12
- **Framework**: FastAPI
- **Entorno virtual**: /home/gxapp/apps/gx-object-registry/venv

## Base de Datos

- **Motor**: PostgreSQL 15
- **Base de datos**: gx_object_registry
- **Usuario**: gxapp_user
- **Puerto**: 5432

## Servicios

### GX Registry (Aplicación)
- **Servicio**: gxregistry.service
- **Puerto**: 8000 (solo localhost)
- **Workers**: 4 (Gunicorn + Uvicorn)
- **Auto-inicio**: Sí

### Nginx (Proxy Reverso)
- **Puerto HTTP**: 80
- **Puerto HTTPS**: 443 (si está configurado)
- **Configuración**: /etc/nginx/sites-available/gxregistry

### PostgreSQL
- **Puerto**: 5432
- **Auto-inicio**: Sí

## Acceso

### Desde Windows (VirtualBox)

**SSH**:
```
ssh -p 2222 gxapp@localhost
```

**Web (Nginx)**:
```
http://localhost:8080
```

**API Directa**:
```
http://localhost:8000
```

**API Docs**:
```
http://localhost:8080/docs
```

## Comandos Útiles

### Servicios

**Ver estado de todos los servicios**:
```bash
~/check_system.sh
```

**Reiniciar aplicación**:
```bash
sudo systemctl restart gxregistry.service
```

**Ver logs de aplicación**:
```bash
sudo journalctl -u gxregistry.service -f
```

### Base de Datos

**Conectarse a PostgreSQL**:
```bash
psql -h localhost -U gxapp_user -d gx_object_registry
```

**Backup manual**:
```bash
~/backups/backup_database.sh
```

**Restaurar backup**:
```bash
~/backups/restore_database.sh ~/backups/database/archivo.sql.gz
```

## Backups

- **Ubicación**: ~/backups/database/
- **Frecuencia**: Diaria (2:00 AM)
- **Retención**: 7 días
- **Log**: ~/backups/backup.log

## Archivos Importantes

- **Configuración app**: ~/apps/gx-object-registry/.env
- **Servicio systemd**: /etc/systemd/system/gxregistry.service
- **Nginx config**: /etc/nginx/sites-available/gxregistry
- **Logs app**: ~/apps/gx-object-registry/logs/
- **Logs nginx**: /var/log/nginx/

## Credenciales

**Usuario administrador**:
- Username: admin
- Email: admin@gxregistry.local
- Password: [Ver archivo seguro]

**Base de datos**:
- Ver archivo .env

## Mantenimiento

**Actualizar sistema**:
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart gxregistry.service
```

**Actualizar aplicación**:
```bash
cd ~/apps/gx-object-registry
source venv/bin/activate
git pull  # Si usas Git
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart gxregistry.service
```

**Limpiar logs antiguos**:
```bash
sudo journalctl --vacuum-time=7d
```
```

**Guardar**: `Ctrl+X`, `Y`, `Enter`

### Verificación

✅ **Documentación del sistema creada**
✅ **Comandos útiles documentados**

---

## Paso 49: Configurar HTTPS (Opcional)

### Objetivo
Configurar certificado SSL para HTTPS (si se desea).

### ¿Es Necesario?

**Para VM local/desarrollo**: NO es necesario
**Para servidor en Internet**: SÍ es recomendado

### Para VM Local (Tu Caso)

**Puedes saltarte este paso** ya que estás en una VM local.

Si en el futuro despliegas en un servidor real con dominio, usa Let's Encrypt:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tudominio.com
```

### Para Desarrollo con Certificado Auto-firmado (Opcional)

Si quieres probar HTTPS localmente:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/gxregistry-selfsigned.key \
  -out /etc/ssl/certs/gxregistry-selfsigned.crt
```

Luego modificar Nginx para usar HTTPS.

**Para este tutorial**: No configuraremos HTTPS.

---

## Paso 50: Pruebas Finales del Sistema

### Objetivo
Verificar que todo el sistema funciona correctamente.

### Checklist de Pruebas

#### 50.1 Servicios Corriendo

```bash
~/check_system.sh
```

**Verificar**:
- ✅ GX Registry corriendo
- ✅ PostgreSQL corriendo
- ✅ Nginx corriendo

#### 50.2 Acceso desde Windows

**En navegador Windows**:

**1. Página principal**:
```
http://localhost:8080
```
✅ Debe cargar

**2. Login**:
```
http://localhost:8080/web/login
```
✅ Debe mostrar formulario

**3. API Docs**:
```
http://localhost:8080/docs
```
✅ Debe mostrar Swagger UI

**4. Iniciar sesión**:
- Username: admin
- Password: [tu contraseña]
✅ Debe iniciar sesión

#### 50.3 Verificar Base de Datos

```bash
psql -h localhost -U gxapp_user -d gx_object_registry -c "SELECT COUNT(*) FROM users;"
```

**Debe mostrar**:
```
 count
-------
     1
(1 row)
```

✅ **Usuario existe**

#### 50.4 Probar Backup

```bash
~/backups/backup_database.sh
ls -lh ~/backups/database/
```

✅ **Backup se crea correctamente**

#### 50.5 Verificar Logs

```bash
sudo journalctl -u gxregistry.service -n 20 --no-pager
```

**No deben haber errores recientes**. ✅

#### 50.6 Reiniciar VM y Verificar Auto-inicio

```bash
sudo reboot
```

**Espera 1-2 minutos** para que la VM reinicie.

**Reconecta por SSH**:
```powershell
ssh -p 2222 gxapp@localhost
```

**Verificar servicios**:
```bash
~/check_system.sh
```

**Todos los servicios deben iniciar automáticamente**. ✅

**Probar en navegador**:
```
http://localhost:8080
```

✅ **Aplicación funciona después de reinicio**

### Verificación Final

✅ **Todos los servicios corriendo**
✅ **Aplicación accesible desde Windows**
✅ **Login funcionando**
✅ **Base de datos poblada**
✅ **Backups funcionando**
✅ **Auto-inicio configurado**
✅ **Sistema estable después de reinicio**

---

# FASE 8: MANTENIMIENTO Y TROUBLESHOOTING

---

## Paso 51: Comandos de Mantenimiento Diario

### Objetivo
Conocer comandos para mantenimiento rutinario.

### Comandos Útiles

#### Ver Estado del Sistema
```bash
~/check_system.sh
```

#### Ver Logs en Tiempo Real
```bash
# Aplicación
sudo journalctl -u gxregistry.service -f

# Nginx
sudo tail -f /var/log/nginx/gxregistry-access.log
sudo tail -f /var/log/nginx/gxregistry-error.log
```

#### Reiniciar Servicios
```bash
# Solo la aplicación
sudo systemctl restart gxregistry.service

# Nginx
sudo systemctl restart nginx

# PostgreSQL
sudo systemctl restart postgresql
```

#### Verificar Uso de Recursos
```bash
# CPU y Memoria
htop

# Uso de disco
df -h
ncdu /home/gxapp/apps/gx-object-registry

# Procesos de la aplicación
ps aux | grep gunicorn
```

---

## Paso 52: Actualizar la Aplicación

### Objetivo
Procedimiento para actualizar código de la aplicación.

### Procedimiento

#### Si usas Git

```bash
cd ~/apps/gx-object-registry
source venv/bin/activate

# Backup antes de actualizar
~/backups/backup_database.sh

# Actualizar código
git pull

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Ejecutar migraciones
alembic upgrade head

# Reiniciar servicio
sudo systemctl restart gxregistry.service

# Verificar
sudo systemctl status gxregistry.service
```

#### Si transfieres archivos manualmente

```powershell
# Desde Windows
scp -P 2222 archivo.py gxapp@localhost:/home/gxapp/apps/gx-object-registry/
```

Luego reiniciar servicio en Ubuntu.

---

## Paso 53: Troubleshooting Común

### Problema: La aplicación no inicia

**Síntoma**:
```bash
sudo systemctl status gxregistry.service
# Muestra: failed
```

**Diagnóstico**:
```bash
sudo journalctl -u gxregistry.service -n 50
```

**Causas comunes**:
1. Error en código Python
2. Error en .env
3. Base de datos no accesible
4. Puerto ya en uso

**Solución**:
- Revisar logs
- Verificar .env
- Verificar PostgreSQL corriendo
- Matar proceso en puerto 8000:
  ```bash
  sudo lsof -ti:8000 | xargs kill -9
  ```

### Problema: No puedo acceder desde Windows

**Diagnóstico**:
```bash
# Verificar que app esté escuchando
sudo netstat -tlnp | grep 8000

# Verificar Nginx
sudo nginx -t
sudo systemctl status nginx
```

**Causas comunes**:
1. Firewall bloqueando
2. Port forwarding no configurado
3. Servicio detenido

**Solución**:
- Verificar UFW permite puertos
- Verificar configuración de VirtualBox
- Reiniciar servicios

### Problema: Error de base de datos

**Síntoma**: "connection refused" o "authentication failed"

**Diagnóstico**:
```bash
psql -h localhost -U gxapp_user -d gx_object_registry
```

**Causas comunes**:
1. PostgreSQL detenido
2. Contraseña incorrecta en .env
3. Base de datos no existe

**Solución**:
```bash
sudo systemctl start postgresql
# Verificar .env
# Recrear base de datos si es necesario
```

---

## Paso 54: Optimizaciones Adicionales (Opcional)

### Objetivo
Mejoras opcionales para producción.

### Redis para Caché (Opcional)

```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Luego configurar en la aplicación.

### Monitoreo con Prometheus (Opcional)

Para monitoreo avanzado, instalar Prometheus y Grafana.

### Backup Remoto (Opcional)

Configurar respaldo de backups a otro servidor o servicio cloud.

---

## Paso 55: Checklist Final de Producción

### Objetivo
Verificación final antes de considerar el sistema en producción.

### Checklist Completo

#### Seguridad
- ✅ Contraseñas fuertes configuradas
- ✅ SECRET_KEY único y seguro
- ✅ Firewall habilitado y configurado
- ✅ Archivo .env con permisos 600
- ✅ PostgreSQL solo escucha localhost
- ✅ Aplicación solo escucha localhost (Nginx hace proxy)

#### Servicios
- ✅ GX Registry como servicio systemd
- ✅ Nginx configurado como proxy reverso
- ✅ PostgreSQL corriendo y optimizado
- ✅ Todos los servicios con auto-inicio habilitado

#### Base de Datos
- ✅ Usuario y base de datos creados
- ✅ Migraciones aplicadas
- ✅ Datos iniciales (seed) cargados
- ✅ Usuario administrador creado

#### Backups
- ✅ Script de backup funcionando
- ✅ Cron configurado para backups diarios
- ✅ Script de restauración creado
- ✅ Backup manual probado

#### Monitoreo
- ✅ Script de estado del sistema
- ✅ Logs configurados y rotando
- ✅ Herramientas de monitoreo instaladas

#### Acceso
- ✅ SSH funcionando desde Windows
- ✅ Aplicación web accesible
- ✅ Login funcionando
- ✅ API Docs accesible

#### Documentación
- ✅ Archivo SISTEMA.md creado
- ✅ Credenciales anotadas
- ✅ Comandos útiles documentados

#### Pruebas
- ✅ Sistema reiniciado y servicios auto-inician
- ✅ Aplicación estable después de reinicio
- ✅ Todas las funcionalidades principales probadas

---

# 🎉 ¡INSTALACIÓN COMPLETADA! 🎉

---

## Resumen de lo Instalado

Has instalado y configurado exitosamente:

1. ✅ **VirtualBox** con Ubuntu Server 22.04.5 LTS
2. ✅ **Networking** configurado (NAT + Port Forwarding)
3. ✅ **SSH** para acceso remoto desde Windows
4. ✅ **PostgreSQL 15** como base de datos
5. ✅ **Python 3.10** con entorno virtual
6. ✅ **FastAPI** application (GeneXus Object Registry)
7. ✅ **Gunicorn** con Uvicorn workers
8. ✅ **Nginx** como proxy reverso
9. ✅ **Systemd** para gestión de servicios
10. ✅ **Firewall UFW** configurado
11. ✅ **Backups automáticos** diarios
12. ✅ **Monitoreo básico** del sistema

## Accesos Rápidos

### Desde Windows

**SSH**:
```powershell
ssh -p 2222 gxapp@localhost
```

**Aplicación Web**:
```
http://localhost:8080
```

**API Documentation**:
```
http://localhost:8080/docs
```

**Login**:
```
http://localhost:8080/web/login
Username: admin
```

### Comandos Esenciales

**Estado del sistema**:
```bash
~/check_system.sh
```

**Ver logs**:
```bash
sudo journalctl -u gxregistry.service -f
```

**Reiniciar aplicación**:
```bash
sudo systemctl restart gxregistry.service
```

**Backup manual**:
```bash
~/backups/backup_database.sh
```

## Próximos Pasos

1. **Personalizar la aplicación** según tus necesidades
2. **Importar objetos** de GeneXus
3. **Crear más usuarios** si es necesario
4. **Configurar HTTPS** si despliegas a Internet
5. **Monitorear** el sistema regularmente

## Soporte

- **Documentación**: ~/SISTEMA.md
- **Logs**: sudo journalctl -u gxregistry.service
- **Backups**: ~/backups/database/

---

**Instalación completada exitosamente el**: Agosto 3, 2026

**Versión del documento**: 1.0

**Sistema**: Ubuntu 22.04.5 LTS en VirtualBox

---

**¡Gracias por usar GeneXus Object Registry!** 🚀
