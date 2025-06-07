Chatbot E-commerce con ML

## 🧱 Estructura del Proyecto

Este documento describe formalmente el desarrollo del proyecto de chatbot para e-commerce que integra procesamiento de imágenes, predicción de precios mediante aprendizaje automático, y visualización vía dashboard administrativo.

---
## Integrantes del Proyecto 
- Cristian Alejandro Melgar Ordoñez 7690 21 8342
- Edrei Andres Giron Leonardo 7690 21 218
- Edward Alexander Aguilar Flores 7690 21 7651


## 🔗 Enlace al Repositorio GitHub

Repositorio público del proyecto: [https://github.com/Alejmm/Chatbot_e-commerce.git](https://github.com/Alejmm/Chatbot_e-commerce.git)


## 👨‍💻 Roles del Equipo

| Rol                        | Responsabilidades principales |
|---------------------------|-------------------------------|
| Desarrollador Backend / ML | Implementación de lógica de predicción, integración de modelo visual CLIP, procesamiento de imágenes, conexión Oracle |
| Ingeniero DevOps          | Configuración de entorno local, tareas automatizadas, manejo de scripts, instalación en Windows |
| UX/UI                     | Desarrollo del dashboard Streamlit, pruebas de interfaz, experiencia de usuario |


## 🧪 Justificación Técnica

- El uso de **CLIP** permite mejorar la precisión en la identificación de productos por imagen.
- El modelo de predicción entrenado con datos históricos en Oracle permite generar precios sugeridos ajustados al comportamiento del mercado.
- El sistema integra un bot, una base de datos robusta y una interfaz de visualización, ofreciendo una solución escalable.


## 📂 Evidencia de Colaboración y Gestión

### Slack
- Se utilizó un canal dedicado en Slack (`#equipo-ecommerce`) para discusión técnica y coordinación diaria.

### Trello
- Se manejaron tableros en Trello con fases: `Tablero`, `Lista de Tareas`, `En proceso`, `Finalizado`.
- URL https://trello.com/invite/b/68438eee66b5583755ee50d1/ATTI975105ddf857d188c74f112f47cf137051A309DA/tareas-chatbot-ml
- 

### Capturas de uso de herramientas:

Slack: 
![image](https://github.com/user-attachments/assets/30907161-a911-492f-844b-fffdb488f332)

Trello: 
![image](https://github.com/user-attachments/assets/9f6f2599-f63e-41f8-9d6b-a0c80eab7280)


## 🛠️ Funcionalidades Destacadas

- Búsqueda de productos por nombre o imagen
- Descripción automática con BLIP / CLIP
- Predicción de precios y sugerencias similares
- Dashboard administrativo para edición de precios
- Integración con base de datos Oracle en tiempo real


## 📅 Automatización y Tareas Programadas

Se programó `prediccion_periodica.py` como una tarea automática diaria en Windows con `Task Scheduler` para:

- Consultar datos
- Reentrenar el modelo si es necesario
- Actualizar predicciones en base de datos


## 📈 Capturas de Funcionalidad

### Bot de Telegram:

- Inicio de conversación con saludo, y consulta por nombre: Su funcionamiento consiste que al momento de consultar un producto lo buscará y mostrará si fue satisfactorio, brindando así 4 sugerencias más de productos que puedan interesar al cliente.  
![image](https://github.com/user-attachments/assets/7c09daf1-f2ae-4384-a9ce-2f94cac971fe)

- Consulta anterior y consulta por imagen: Al haber  ya realizado una consulta pregunta y brinda la opción a seguir consultando, al realizar un envió de imagen analiza la misma, obtiene una descripción y muestra la coincidencia encontrada, brindando así 4 sugerencias más de productos que puedan interesar al cliente. 
![image-1](https://github.com/user-attachments/assets/bc5112dd-b314-4de4-b49d-82a4d68f87c6)
![image-2](https://github.com/user-attachments/assets/7a2e7d74-c17e-44ab-b0e6-952e1ef8697c)


- Uso de comando /ayuda: Al utilizar el comando ayuda brindara soporte sobre el uso del ChatBot, utilizando el comando de ayuda /destacados, brindando 5 productos destacados. 
![image-3](https://github.com/user-attachments/assets/d3115b9b-b043-4c46-8aba-21b49aee6d53)

- Uso de categorías: El comando /ayuda también brinda las categorías disponbibles del sistema, al escribir alguna de estas categorías mostrará los productos de la categoría seleccionada.
![image-4](https://github.com/user-attachments/assets/f51d189a-b9a3-48b3-8f9f-c23eb9948987)

### Dashboard Streamlit:

  1. **Vista general del dashboard:**
 ![image-5](https://github.com/user-attachments/assets/de43cb96-7fb6-4d5b-bc5f-24712d8ab77d)
  
  2. **Comparativa de precios por categoría:**
 ![image-6](https://github.com/user-attachments/assets/f4e03f99-9c70-4353-b213-7780aa7e9a60)
  
  3. **Edición de precio sugerido:**
![image-7](https://github.com/user-attachments/assets/f148c6ad-dbc9-42f1-aaf7-3c06ddc4a0bc)

 4. **Comparación de Precios Actuales vs Predicciones:**
![image-8](https://github.com/user-attachments/assets/9afef3f3-e826-43a8-a432-29ff05521cb1)


## 🧠 Consideraciones Finales

Este sistema fue desarrollado como proyecto académico integrador de conocimientos en:
- Machine Learning
- Procesamiento de imágenes
- Bases de datos
- Infraestructura y automatización
- Desarrollo de interfaces interactivas


## ✅ Conclusión

El proyecto logra una experiencia e-commerce aumentada por Machine Learning, permitiendo a los usuarios encontrar productos por imagen y obtener precios predichos automáticamente. La arquitectura modular y escalable permite añadir futuras mejoras con facilidad.

