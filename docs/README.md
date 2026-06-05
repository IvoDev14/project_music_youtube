# Product Spec

## Elevator Pitch

Esta aplicación permitirá la edición automática de edits de canciones
con vídeos de fondo. Además de la subida automática a redes sociales,
con sus datos pertinentes (descipción, título...)

## Requisitos del MVP

El proyecto se desarrollará siguiendo un pipeline modular de 5 fases. Para mantener el MVP ágil y económico, **no habrá generación de vídeo por IA**, sino una maquetación mecánica asistida por un LLM que actuará como "Director de Edición" aplicando efectos predefinidos a través de un archivo de configuración JSON intermedio.

### 1. Fase de Ingesta (React + Python Backend)
*   **R1.1:** El sistema debe permitir la subida de un archivo de audio principal (`.mp3` o `.wav`).
*   **R1.2:** El sistema debe permitir la subida de uno o varios archivos de vídeo de origen (brutos/escenas).
*   **R1.3:** La interfaz debe capturar un parámetro numérico del usuario ($X$) que definirá el intervalo de corte basado en el ritmo (ej. *«cambiar de escena cada $X$ beats»*).

### 2. Fase de Análisis Métrico y Acústico (Python - No Creativo)
*   **R2.1 (Subtítulos):** El backend procesará el audio con **Whisper** (o una versión optimizada como `faster-whisper` en local) para extraer el texto y generar un mapa de subtítulos con timestamps exactos palabra por palabra.
*   **R2.2 (Ritmo):** El backend analizará el audio con **Librosa** para detectar los transitorios (picos de energía / *beats*) y devolverá un array con las marcas de tiempo exactas (milisegundos) de cada golpe de ritmo.

### 3. Fase de Maquetación Mecánica (Python - Algorítmico)
*   **R3.1 (Línea de Tiempo):** El sistema generará una "receta de edición" en formato **JSON** uniendo los datos acústicos y los inputs del usuario.
*   **R3.2 (Cortes Matemáticos):** El algoritmo calculará los puntos de corte exactos usando el array de *beats* y el parámetro $X$ del usuario, asignando secuencialmente fragmentos de los vídeos de origen a cada bloque de tiempo.
*   **R3.3 (Capa de Texto):** El JSON incluirá el mapeo base de los subtítulos alineados cronológicamente con la línea de tiempo.

### 4. Fase de Enriquecimiento Creativo (IA + n8n/Python)
*   **R4.1 (Análisis de Mood):** Se enviará la letra de la canción y el JSON mecánico a un LLM para que analice el contexto emocional, identificando clímax, *drops* o cambios de ritmo.
*   **R4.2 (Inyección de Efectos):** La IA modificará el JSON intermedio añadiendo instrucciones estéticas basadas en un catálogo de herramientas limitado y preprogramado.
*   **R4.3 (Catálogo de Herramientas de la IA):**
    *   Filtros globales por tramos (ej. `grayscale`, saturación, estilo vintage).
    *   Efectos de transición en timestamps específicos (ej. `flash_white`, zoom rápido/sacudida en los *drops*).

### 5. Fase de Renderizado y Compilación Final (Python + FFmpeg)
*   **R5.1 (Ejecución de Receta):** El backend de Python tomará el JSON final enriquecido por la IA y lo procesará usando **FFmpeg** (o MoviePy) para realizar los cortes físicos y aplicar los filtros en los tiempos indicados.
*   **R5.2 (Estilizado de Subtítulos):** El motor quemará los subtítulos en el vídeo usando formatos que permitan personalización avanzada (como `.ass` para fuentes, sombras y animaciones palabra por palabra en vertical 9:16).
*   **R5.3 (Salida):** El sistema compilará el vídeo final con el audio integrado en un archivo `.mp4` listo para su visualización o descarga.
 
