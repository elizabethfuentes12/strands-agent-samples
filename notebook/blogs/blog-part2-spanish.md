# Procesamiento de Contenido Multi-Modal con Memoria: Llevando Strands Agent al Siguiente Nivel

*Parte 2: Agregando Memoria Persistente con FAISS*

En nuestro [artículo anterior](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-just-a-few-lines-of-code-4hn4), exploramos cómo construir un agente de IA multi-modal capaz de procesar imágenes, documentos y videos usando el framework Strands Agent. Hoy, vamos un paso más allá agregando **capacidades de memoria persistente** usando FAISS (Facebook AI Similarity Search) para crear un agente que puede recordar y recuperar información a través de sesiones.

## 🧠 Por Qué Importa la Memoria

Imagina tener un asistente de IA que no solo procesa tu contenido, sino que también recuerda lo que le has mostrado antes. Esto abre casos de uso poderosos:

- **Conversaciones contextuales**: "¿Recuerdas ese diagrama de arquitectura que te mostré ayer? ¿Cómo se relaciona con este nuevo documento?"
- **Aprendizaje progresivo**: Construir conocimiento a lo largo del tiempo a partir de múltiples interacciones
- **Respuestas personalizadas**: Adaptar respuestas basadas en tus preferencias y contenido previo
- **Continuidad entre sesiones**: Mantener contexto incluso después de reiniciar tu aplicación

## 🚀 Lo Que Estamos Construyendo

Mejoraremos nuestro agente multi-modal con:

1. **Almacenamiento de memoria con FAISS** usando la herramienta `mem0_memory`
2. **Almacenamiento persistente de información** a través de sesiones
3. **Recuperación inteligente** de memorias relevantes basada en contexto
4. **Operaciones de gestión de memoria** (almacenar, recuperar, listar)

## 🛠️ Configurando el Agente Mejorado

Comencemos configurando nuestro agente con capacidades de memoria:

```python
import boto3
from strands.models import BedrockModel
from strands import Agent
from strands_tools import image_reader, file_read, mem0_memory, use_llm
from video_reader import video_reader

# Prompt del sistema mejorado con instrucciones de memoria
MULTIMODAL_SYSTEM_PROMPT = """ Eres un asistente útil que puede procesar documentos, imágenes y videos. 
Analiza su contenido y proporciona información relevante. Tienes capacidades de memoria y puedes recordar interacciones previas.

Puedes:
1. Para formatos PNG, JPEG/JPG, GIF o WebP usa image_reader para procesar el archivo
2. Para formatos PDF, csv, docx, xls o xlsx usa file_read para procesar el archivo  
3. Para formatos MP4, MOV, AVI, MKV, WebM usa video_reader para procesar el archivo
4. Simplemente entregar la respuesta

Capacidades de memoria:
- Almacenar nueva información usando la herramienta mem0_memory (action="store")
- Recuperar memorias relevantes (action="retrieve")
- Listar todas las memorias (action="list")
- Proporcionar respuestas personalizadas

Reglas clave:
- Siempre incluir user_id={USER_ID} en las llamadas a herramientas
- Ser conversacional y natural en las respuestas
- Formatear la salida claramente
- Reconocer información almacenada
- Referenciar interacciones pasadas relevantes cuando sea apropiado
"""

# Configurar AWS Bedrock
session = boto3.Session(region_name='us-west-2')
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    boto_session=session,
    streaming=False
)

# Crear agente mejorado con capacidades de memoria
multimodal_agent = Agent(
    system_prompt=MULTIMODAL_SYSTEM_PROMPT,
    tools=[image_reader, file_read, video_reader, mem0_memory, use_llm],
    model=bedrock_model,
)
```

## 💾 Operaciones de Memoria en Acción

### 1. Almacenando Contexto Inicial del Usuario

Primero, almacenemos información básica sobre nuestro usuario:

```python
USER_ID = "eli_abc"  # Generar un ID único de usuario
content = """Hola, mi nombre es Elizabeth, pero me dicen Eli. Soy developer advocate en AWS, 
y quiero entender qué hay en imágenes, videos y documentos para mejorar mi trabajo diario."""

# Almacenar contexto del usuario en memoria
multimodal_agent.tool.mem0_memory(action="store", content=content, user_id=USER_ID)
```

### 2. Análisis de Imagen con Almacenamiento en Memoria

Ahora analicemos una imagen y almacenemos automáticamente los resultados:

```python
print("=== 📸 ANÁLISIS DE IMAGEN CON MEMORIA ===")
image_result = multimodal_agent(
    f"Analiza la imagen data-sample/diagram.jpg en detalle y describe todo lo que observas. "
    f"Recuerda esta información para más tarde. USER_ID: {USER_ID}"
)
print(image_result)
```

El agente:
1. Procesará la imagen usando `image_reader`
2. Analizará el diagrama arquitectónico
3. Almacenará automáticamente el análisis en memoria usando `mem0_memory`
4. Proporcionará una descripción detallada

### 3. Análisis de Video con Memoria

Procesemos un video y almacenemos su contenido:

```python
print("=== 🎬 ANÁLISIS DE VIDEO CON MEMORIA ===")
video_result = multimodal_agent(
    "Analiza el video data-sample/moderation-video.mp4 y describe en detalle "
    "las acciones y escenas que observas. Almacena esta información en tu memoria."
)
print(video_result)
```

### 4. Procesamiento de Documento con Memoria

Procesa y recuerda el contenido del documento:

```python
print("=== 📄 ANÁLISIS DE DOCUMENTO CON MEMORIA ===")
doc_result = multimodal_agent(
    "Resume como json el contenido del documento data-sample/Welcome-Strands-Agents-SDK.pdf "
    "y almacena esta información en tu memoria."
)
print(doc_result)
```

## 🔍 Recuperación y Gestión de Memoria

### Recuperando Memorias Específicas

```python
# Recuperar memorias relacionadas con una consulta específica
retrieved_memories = multimodal_agent.tool.mem0_memory(
    action="retrieve", 
    query="¿Qué servicios están en la imagen?", 
    user_id=USER_ID
)
print("Memorias Recuperadas:", retrieved_memories)
```

### Listando Todas las Memorias Almacenadas

```python
# Listar todas las memorias almacenadas para el usuario
all_memories = multimodal_agent.tool.mem0_memory(
    action="list", 
    user_id=USER_ID
)
print("Todas las Memorias Almacenadas:", all_memories)
```

### Probando Recuperación de Memoria Cross-Modal

El verdadero poder viene al probar la memoria a través de diferentes tipos de medios:

```python
print("=== 🧠 PRUEBA DE RECUPERACIÓN DE MEMORIA ===")
memory_result = multimodal_agent(
    "¿Qué recuerdas sobre la imagen, video y documento que te mostré anteriormente?"
)
print(memory_result)
```

## 🎯 Casos de Uso del Mundo Real

Este agente mejorado con memoria abre numerosas aplicaciones prácticas:

### 1. **Asistente de Documentación Técnica**
- Recordar diagramas de arquitectura, fragmentos de código y documentación
- Proporcionar respuestas contextuales basadas en tu historial de proyecto
- Rastrear cambios y evolución de tus diseños técnicos

### 2. **Pipeline de Análisis de Contenido**
- Procesar lotes de imágenes, videos y documentos
- Construir una base de conocimiento de contenido analizado
- Generar reportes basados en insights acumulados

### 3. **Gestión de Conocimiento Personal**
- Almacenar y recordar información de varios tipos de medios
- Crear conexiones entre diferentes piezas de contenido
- Construir un asistente de IA personalizado que crezca con tus necesidades

### 4. **Procesamiento de Contenido Educativo**
- Analizar materiales educativos en diferentes formatos
- Recordar preferencias y patrones de aprendizaje de estudiantes
- Proporcionar recomendaciones de aprendizaje personalizadas

## 🔧 Características y Beneficios Clave

### **Memoria Persistente**
- La información sobrevive a reinicios de aplicación
- Búsqueda de similitud con FAISS para recuperación relevante
- Almacenamiento y consulta eficiente de grandes cantidades de datos

### **Comprensión Cross-Modal**
- Conectar insights de imágenes, videos y documentos
- Construir comprensión integral a través de tipos de medios
- Generar respuestas holísticas basadas en múltiples fuentes

### **Personalización**
- Almacenamiento de memoria específico por usuario con IDs únicos
- Respuestas adaptadas basadas en historial del usuario
- Aprendizaje progresivo de interacciones del usuario

### **Escalabilidad**
- Manejar grandes volúmenes de contenido y memorias
- Búsqueda de similitud eficiente usando FAISS
- Optimizado para cargas de trabajo de producción

## 🚀 Comenzando

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd notebook
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar credenciales de AWS** para acceso a Bedrock

4. **Ejecutar el notebook**:
   ```bash
   jupyter notebook multi-understanding-with-memory.ipynb
   ```

## 🎉 ¿Qué Sigue?

Con procesamiento multi-modal mejorado con memoria, puedes:

- Construir asistentes de IA más sofisticados
- Crear pipelines de análisis de contenido personalizados
- Desarrollar aplicaciones que aprenden y mejoran con el tiempo
- Implementar continuidad entre sesiones en tus flujos de trabajo de IA

La combinación de las capacidades multi-modales de Strands Agent con memoria persistente crea una base poderosa para construir aplicaciones inteligentes y conscientes del contexto que pueden verdaderamente entender y recordar tu contenido.

## 📚 Recursos

- [Documentación de Strands Agent](https://github.com/awslabs/strands)
- [Parte 1: Procesamiento Multi-Modal Básico](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-just-a-few-lines-of-code-4hn4)
- [Ejemplos de Código Completos](https://github.com/your-repo/multi-understanding-notebooks)
- [Documentación de AWS Bedrock](https://docs.aws.amazon.com/bedrock/)

---

*¿Listo para construir tu propio agente de IA mejorado con memoria? ¡Prueba el notebook completo y cuéntanos qué aplicaciones increíbles creas!*

#AWS #IA #AprendizajeAutomatico #MultiModal #FAISS #StrandsAgent #Bedrock #Memoria #InteligenciaArtificial
