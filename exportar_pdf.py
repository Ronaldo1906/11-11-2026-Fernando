import os
from fpdf import FPDF

# Carpetas y extensiones a ignorar o incluir
CARPETAS_IGNORADAS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build', '.next'}
EXTENSIONES_VALIDAS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json', '.sql', '.md', '.env.example'}

class PDFProyecto(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Documentación de Código del Proyecto', align='R', new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

pdf = PDFProyecto()
pdf.set_auto_page_break(auto=True, margin=15)

for raiz, dirs, archivos in os.walk('.'):
    # Filtrar carpetas ignoradas
    dirs[:] = [d for d in dirs if d not in CARPETAS_IGNORADAS]

    for archivo in sorted(archivos):
        if any(archivo.endswith(ext) for ext in EXTENSIONES_VALIDAS):
            ruta_completa = os.path.join(raiz, archivo)
            if archivo == 'exportar_pdf.py':
                continue

            pdf.add_page()
            # Título del archivo
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 10, f'Archivo: {ruta_completa}', fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)

            # Contenido del código
            pdf.set_font('Courier', '', 8.5)
            try:
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                # Limpiar caracteres incompatibles con latin-1 básico si es necesario
                contenido_limpio = contenido.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 4.5, contenido_limpio)
            except Exception as e:
                pdf.multi_cell(0, 5, f'[No se pudo leer el archivo: {e}]')

pdf.output('proyecto_completo.pdf')
print("¡PDF generado exitosamente como 'proyecto_completo.pdf'!")