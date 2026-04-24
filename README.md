# Sistema de Control de Productos y Simulación Logística

Un sistema robusto de gestión de inventarios y simulación de centro de distribución construido con Python y Flet. Este proyecto permite administrar productos, proveedores, compradores y repartidores, e incluye un potente motor de simulación multi-hilo para modelar operaciones logísticas en tiempo real.

## Características Principales

*   **Dashboard Interactivo**: Panel principal con métricas clave, gráficas de barras para visualizar existencias y alertas de stock bajo/agotado integradas.
*   **Gestión CRUD Completa**: Interfaces amigables con cuadros de diálogo para crear, editar, eliminar y visualizar:
    *   Productos
    *   Productores / Proveedores
    *   Compradores
    *   Repartidores
*   **Simulación Concurrente**: Un motor de simulación ejecutado en segundo plano (hilos daemon) que simula el ciclo de vida real de un centro de distribución:
    *   Llegada de pedidos y compras constantes.
    *   Asignación inteligente de repartidores disponibles.
    *   Reabastecimiento automático (Restock) de productos.
*   **Sistema de Logs Visual y Thread-Safe**: Panel dedicado de registros (Logs) que captura en tiempo real todas las operaciones de la simulación, categorizadas por eventos (`Info`, `Success`, `Warning`, `Error`) sin bloquear la interfaz.
*   **Paginación Inteligente**: Tablas de datos optimizadas con sistema de paginación a prueba de fallos para manejar grandes volúmenes de registros.

## Tecnologías Utilizadas

*   **Python 3.14**: Lenguaje núcleo del sistema.
*   **Flet**: Framework basado en Flutter que permite crear interfaces de usuario interactivas, modernas y reactivas en Python puro.
*   **SQLAlchemy 2.0**: El ORM (Object Relational Mapper) más potente para Python. Gestiona la base de datos como objetos de clase, garantizando el manejo seguro en entornos multi-hilo (`check_same_thread=False`).
*   **SQLite**: Motor de base de datos ligero que no requiere configuración de servidor, ideal para almacenar el estado y los registros de la aplicación.
*   **Alembic**: Herramienta de migraciones para actualizar la estructura de la base de datos de manera segura y sin perder información.

## Requisitos Previos

Asegúrate de tener instalado en tu sistema:
*   Python 3.10 o superior (Recomendado 3.14)
*   `pip` (Gestor de paquetes de Python)

## Instalación y Configuración

1. **Clonar o descargar el repositorio** y navegar a la carpeta raíz del proyecto.
2. **Crear y activar un entorno virtual (Opcional pero recomendado)**:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install flet sqlalchemy alembic
   ```

## Ejecución del Sistema

Para iniciar la aplicación, ejecuta el archivo principal desde tu terminal:

```bash
python main.py
```
*(Nota: Si el punto de entrada principal tiene otro nombre en la raíz, como `app.py`, cámbialo en el comando).*

### Uso de la Simulación
1. Dirígete a la sección **Simulación** usando el menú lateral izquierdo.
2. Selecciona la cantidad de operaciones a simular.
3. Presiona Iniciar.
4. Puedes navegar a la vista de **Logs** para ver en tiempo real cómo los hilos despachan pedidos, asignan repartidores y reabastecen el inventario de manera paralela.

## Estructura del Proyecto

*   `models.py`: Definición de esquemas de base de datos ORM (Productos, Compradores, etc.) y operaciones de base de datos.
*   `simulate.py`: Lógica principal del motor de concurrencia y control de hilos para la simulación.
*   `views/`: Carpeta que contiene las interfaces visuales (Flet):
    *   `home.py`: Estructura base de navegación, AppBar y Sidebar.
    *   `dashboard.py`: Panel de métricas y advertencias.
    *   `crud_dialogs.py`: Controladores de ventanas emergentes para creación y edición segura.
    *   `log_view.py`: Interfaz de lectura de la consola de simulación en vivo.
    *   `pagination.py`: Lógica para iterar entre registros de manera segmentada.
    *   `simulation.py`: Panel de control de la simulación logística.

---
*Desarrollado como Proyecto Final para Control de Procesos.*