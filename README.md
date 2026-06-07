# MarkTransform

> Convierte cualquier archivo a Markdown en segundos, sin escribir una sola línea de código.

**MarkTransform** es una aplicación de escritorio para Windows que convierte documentos, hojas de cálculo, presentaciones, imágenes, audio, páginas web y más al formato Markdown, listo para usar con inteligencia artificial, documentación o análisis de texto.

Construido sobre [MarkItDown](https://github.com/microsoft/markitdown) de Microsoft.

---

## Capturas de pantalla

> *Interfaz principal con tema oscuro*
<img width="1360" height="887" alt="image" src="https://github.com/user-attachments/assets/94cab19c-7fa9-4950-a164-69641f200454" />

---

## Características

- **Interfaz amigable** — diseño moderno con tema oscuro y claro
- **Sin conocimientos técnicos** — arrastra o selecciona tus archivos y haz clic en Convertir
- **Múltiples archivos a la vez** — convierte varios documentos en una sola operación
- **URLs compatibles** — pega links de YouTube o páginas web para convertirlos
- **Vista previa en tiempo real** — lee el Markdown generado antes de guardarlo
- **Copiar al portapapeles** — un clic para copiar el resultado
- **Guardar como `.md`** — elige dónde guardar tu archivo Markdown
- **Sin instalación de Python** — el `.exe` funciona en cualquier PC con Windows

---

## Formatos soportados

| Categoría     | Formatos                                      |
|---------------|-----------------------------------------------|
| Documentos    | PDF, Word (.docx, .doc)                       |
| Presentaciones| PowerPoint (.pptx, .ppt)                      |
| Hojas de cálculo | Excel (.xlsx, .xls)                        |
| Imágenes      | JPG, JPEG, PNG, GIF                           |
| Audio         | MP3, WAV                                      |
| Web           | HTML, URLs, YouTube                           |
| Datos         | CSV, JSON, XML                                |
| Otros         | EPub, ZIP, Jupyter Notebook (.ipynb)          |

---

## Instalación

### Opción 1 — Ejecutable directo (recomendado)

1. Descarga el archivo `MarkTransform_Installer.exe` desde la sección [Releases](../../releases)
2. Ejecuta el instalador y sigue los pasos
3. Abre **MarkTransform** desde el escritorio o el menú de inicio

No se requiere Python ni ninguna otra instalación.

### Opción 2 — Desde el código fuente

**Requisitos:** Python 3.10 o superior

```bash
# Clonar el repositorio
git clone https://github.com/Ruberemix/marktransform.git
cd marktransform

# Instalar dependencias
pip install "markitdown[all]" customtkinter pyperclip pillow

# Ejecutar la aplicación
python desktop_app/app.py
```

---

## Cómo usar

1. Abre **MarkTransform**
2. Haz clic en **Examinar archivos** y selecciona uno o varios archivos
   - O pega una URL de YouTube o página web en el campo de URL
3. Haz clic en **▶ Convertir**
4. Lee la vista previa del Markdown generado
5. Haz clic en **💾 Guardar** para guardar el archivo, o **📋 Copiar** para copiarlo al portapapeles

---

## Construir el instalador (desarrolladores)

```bash
# 1. Instalar dependencias de desarrollo
pip install pyinstaller pillow

# 2. Crear el ícono
python desktop_app/create_icon.py

# 3. Compilar el ejecutable
cd desktop_app
python -m PyInstaller markitdown_app.spec --clean --noconfirm

# 4. El ejecutable queda en:
#    desktop_app/dist/MarkTransform/MarkTransform.exe

# 5. Para crear el instalador, instala Inno Setup (https://jrsoftware.org/isdl.php)
#    y compila: desktop_app/installer.iss
```

---

## Estructura del proyecto

```
marktransform/
├── desktop_app/
│   ├── app.py                  # Aplicación principal
│   ├── create_icon.py          # Generador del ícono
│   ├── markitdown_app.spec     # Configuración de PyInstaller
│   ├── installer.iss           # Script de Inno Setup
│   └── icon.ico                # Ícono de la aplicación
├── packages/
│   └── markitdown/             # Librería base (Microsoft MarkItDown)
└── README.md
```

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| [MarkItDown](https://github.com/microsoft/markitdown) | Motor de conversión a Markdown |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfaz gráfica moderna |
| [PyInstaller](https://pyinstaller.org) | Empaquetado del ejecutable |
| [Inno Setup](https://jrsoftware.org/isinfo.php) | Creación del instalador Windows |
| Python 3.13 | Lenguaje base |

---

## Contribuir

Las contribuciones son bienvenidas. Para cambios importantes, abre primero un issue para discutir qué te gustaría cambiar.

1. Haz fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Haz push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## Licencia

© 2026 Ruberemix. Todos los derechos reservados.

Queda prohibida la copia, distribución, modificación o uso de este software sin autorización expresa y por escrito del autor.

El motor de conversión MarkItDown es propiedad de Microsoft Corporation, licenciado bajo MIT.

---

## Autor

Desarrollado por **Ruberemix**  
Basado en [MarkItDown](https://github.com/microsoft/markitdown) de Microsoft
