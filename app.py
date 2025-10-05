import tkinter as tk                                     
from tkinter import filedialog, messagebox, scrolledtext 
from PIL import Image, ImageTk                           
import pandas as pd                                      
from datetime import datetime                            
from docxtpl import DocxTemplate                         
import os                                                
import sys                                               


def resource_path(relative_path):                        
    
    # Devuelve la ruta absoluta de un archivo, funcionando igual
    # en desarrollo o cuando el script está empaquetado con PyInstaller.
    
    if getattr(sys, 'frozen', False):                    
        base_path = sys._MEIPASS                         
    else:
        base_path = os.path.abspath(".")                 
    return os.path.join(base_path, relative_path)        

# Funciones para seleccionar archivos con diálogo 
def seleccionar_excel():                                 
    ruta = filedialog.askopenfilename(
        title="Selecciona el archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")]
    )
    entrada_excel.delete(0, tk.END)                      
    entrada_excel.insert(0, ruta)                        

def seleccionar_plantilla():                             
    ruta = filedialog.askopenfilename(
        title="Selecciona la plantilla Word",
        filetypes=[("Plantilla Word", "*.docx")]
    )
    entrada_plantilla.delete(0, tk.END)                  
    entrada_plantilla.insert(0, ruta)                    

# Función principal que genera los documentos
def generar_documentos():
    try:
        excel_path = entrada_excel.get().strip()         
        doc_path = entrada_plantilla.get().strip()       

        if not excel_path or not doc_path:               
            messagebox.showwarning("Advertencia", "Selecciona el Excel y la plantilla antes de continuar.")
            return

        # aseguramos que la carpeta de salida exista
        os.makedirs("prueba", exist_ok=True)

        # constantes que se inyectarán en la plantilla
        nombre = "favio candia"
        telefono = "61508169"
        correo = "favioalvarez26@gmail.com"
        fecha = datetime.today().strftime("%d/%m/%Y")   

        constantes = {
            'nombre': nombre,
            'telefono': telefono,
            'correo': correo,
            'fecha': fecha
        }

        # Lectura del Excel
        df = pd.read_excel(excel_path)                   

        # Validación de columnas (evita KeyError y ayuda al usuario)
        required_cols = ['Nombre del Alumno', 'Mat', 'Fis', 'Qui']
        for col in required_cols:
            if col not in df.columns:
                messagebox.showerror("Error", f"Falta la columna '{col}' en el Excel. Asegúrate del nombre exacto.")
                return

        # Generación de documentos
        for indice, fila in df.iterrows():                # iteramos fila por fila del DataFrame
            doc = DocxTemplate(doc_path)                  

            contenido = {
                'nombre_alumno': fila['Nombre del Alumno'], 
                'nota_mat': fila['Mat'],
                'nota_fis': fila['Fis'],
                'nota_qui': fila['Qui']
            }

            contenido.update(constantes)                 
            nombre_archivo = f"prueba/Notas_de_{fila['Nombre del Alumno']}.docx" 
            doc.render(contenido)                         
            doc.save(nombre_archivo)                      

            log_text.insert(tk.END, f" Generado: {nombre_archivo}\n")   
            log_text.see(tk.END)                         

        messagebox.showinfo("Éxito", "Documentos generados correctamente en la carpeta 'prueba'")

    except Exception as e:
        messagebox.showerror("Error", str(e))           

# Ventana principal (UI)
ventana = tk.Tk()                                      # creamos la ventana principal de la aplicación
ventana.title("Generador de Documentos - TECBA")       
ventana.geometry("700x500")                            

# Intentamos cargar un icono .ico si existe (usado en Windows)
try:
    icon_path = resource_path("icono/images.ico")     
    ventana.iconbitmap(icon_path)                     
except Exception:
    # Si falla, intentamos un PNG vía iconphoto (más flexible)
    try:
        png_icon = resource_path("icono/images.png")
        img = Image.open(png_icon)
        photo = ImageTk.PhotoImage(img)
        ventana.iconphoto(True, photo)                
    except Exception:
        print(" No se pudo cargar el ícono (ni .ico ni .png). Continuando sin icono.")

# Widgets: título
titulo = tk.Label(ventana, text="Generador de Documentos", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Frame: selección de Excel 
frame_excel = tk.Frame(ventana)
frame_excel.pack(pady=5, fill="x", padx=10)

tk.Label(frame_excel, text="Archivo Excel:", font=("Arial", 11)).pack(side="left")  # etiqueta
entrada_excel = tk.Entry(frame_excel, width=50)               # entrada de texto para la ruta del Excel
entrada_excel.pack(side="left", padx=5)
tk.Button(frame_excel, text="Buscar", command=seleccionar_excel).pack(side="left") 

# Frame: selección de plantilla Word
frame_doc = tk.Frame(ventana)
frame_doc.pack(pady=5, fill="x", padx=10)

tk.Label(frame_doc, text="Plantilla Word:", font=("Arial", 11)).pack(side="left")  # etiqueta
entrada_plantilla = tk.Entry(frame_doc, width=50)         # entrada de texto para la ruta de la plantilla
entrada_plantilla.pack(side="left", padx=5)
tk.Button(frame_doc, text="Buscar", command=seleccionar_plantilla).pack(side="left") 

# Botón principal para generar documentos
btn_generar = tk.Button(ventana, text="Generar Documentos", font=("Arial", 12, "bold"),
                        bg="#2e7d32", fg="white", command=generar_documentos)
btn_generar.pack(pady=15)

# Área de log (salida)
log_text = scrolledtext.ScrolledText(ventana, width=80, height=15, font=("Consolas", 10))
log_text.pack(padx=10, pady=10)

# arrancamos el bucle principal de la interfaz gráfica
ventana.mainloop()

