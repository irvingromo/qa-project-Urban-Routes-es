# Pruebas Automatizadas E2E - Proyecto Urban Routes

## Descripción del Proyecto
Este proyecto contiene una suite completa de pruebas End-to-End (E2E) para la aplicación de transporte "Urban Routes". El objetivo es automatizar y validar exitosamente todo el flujo funcional en el que un usuario solicita un viaje en la tarifa "Comfort", agregando extras como helado, pañuelos y un método de pago con tarjeta.

## Tecnologías y Técnicas Utilizadas
- **Python 3:** Lenguaje principal de desarrollo.
- **Selenium WebDriver:** Para la automatización e interacción del navegador web con la interfaz gráfica de usuario (UI).
- **Pytest:** Framework utilizado para la estructuración y ejecución secuencial de las pruebas.
- **Page Object Model (POM):** Técnica de diseño arquitectónico empleada para crear una clase separada (`UrbanRoutesPage`) que concentra todos los localizadores (usando estrategias variadas como `By.ID`, `By.CLASS_NAME`, `By.XPATH` y `By.CSS_SELECTOR`) y los métodos de interacción. Esto asegura que el código de prueba (`TestUrbanRoutes`) se mantenga limpio y enfocado exclusivamente en aserciones.
- **Explicit Waits (WebDriverWait):** Implementación de esperas dinámicas para garantizar que los elementos del DOM (botones modales, animaciones y asignación de conductor) estén completamente interactuables antes de enviar comandos.

## Instrucciones de Ejecución
1. Asegúrate de tener instalado Python 3, `pytest` y `selenium` en tu entorno virtual.
2. Descarga el controlador de navegador compatible con tu versión de Google Chrome (ChromeDriver).
3. Actualiza la variable `urban_routes_url` dentro del archivo `data.py` con el enlace temporal proporcionado por el servidor.
4. Ejecuta las pruebas desde la terminal navegando al directorio del proyecto y corriendo:
   ```bash
   pytest main.py