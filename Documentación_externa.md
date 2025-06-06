# 📘 Documentación Externa del Proyecto: Chatbot E-commerce con ML

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
- Se manejaron tableros en Trello con fases: `Backlog`, `En proceso`, `Validación`, `Finalizado`.
- URL (ejemplo ficticio): [https://trello.com/b/equipoecommerce](https://trello.com/b/equipoecommerce)

### Capturas de uso de herramientas:

![Slack en uso](captures/slack.png)
![Trello tareas](captures/trello.png)


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
![alt text](image.png)

- Consulta anterior y consulta por imagen: Al haber  ya realizado una consulta pregunta y brinda la opción a seguir consultando, al realizar un envió de imagen analiza la misma, obtiene una descripción y muestra la coincidencia encontrada, brindando así 4 sugerencias más de productos que puedan interesar al cliente. 
![alt text](image-1.png)
![alt text](image-2.png)

- Uso de comando /ayuda: Al utilizar el comando ayuda brindara soporte sobre el uso del ChatBot, utilizando el comando de ayuda /destacados, brindando 5 productos destacados. 
![alt text](image-3.png)

- Uso de categorías: El comando /ayuda también brinda las categorías disponbibles del sistema, al escribir alguna de estas categorías mostrará los productos de la categoría seleccionada.
![alt text](image-4.png)

### Dashboard Streamlit:

  1. **Vista general del dashboard:**
 ![alt text](image-5.png)
  
  2. **Comparativa de precios por categoría:**
 ![alt text](image-6.png)
  
  3. **Edición de precio sugerido:**
![alt text](image-7.png)

 4. **Comparación de Precios Actuales vs Predicciones:**
![alt text](image-8.png)


## 🧠 Consideraciones Finales

Este sistema fue desarrollado como proyecto académico integrador de conocimientos en:
- Machine Learning
- Procesamiento de imágenes
- Bases de datos
- Infraestructura y automatización
- Desarrollo de interfaces interactivas


## ✅ Conclusión

El proyecto logra una experiencia e-commerce aumentada por Machine Learning, permitiendo a los usuarios encontrar productos por imagen y obtener precios predichos automáticamente. La arquitectura modular y escalable permite añadir futuras mejoras con facilidad.

