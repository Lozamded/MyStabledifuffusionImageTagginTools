import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import re

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Imágenes")

        self.image_label = tk.Label(root)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.image_name_label = tk.Label(root, text="")
        self.image_name_label.pack(side=tk.TOP, padx=10, pady=10)
                
        self.text_widget = tk.Text(root, wrap=tk.WORD, width=40, height=20)
        self.text_widget.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Guardar", command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.prev_button = tk.Button(button_frame, text="Anterior", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.skip_entry = tk.Entry(button_frame, width=5)
        self.skip_entry.pack(side=tk.LEFT)

        self.skip_button = tk.Button(button_frame, text="Saltar", command=self.skip_to_image)
        self.skip_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(button_frame, text="Siguiente", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT)

        # Agregar la lista seleccionable y la barra de desplazamiento
        list_frame = tk.Frame(root)
        list_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.image_list = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.image_list_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.image_list.yview)
        self.image_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_list.config(yscrollcommand=self.image_list_scrollbar.set)

        self.image_list.bind("<<ListboxSelect>>", self.select_image_from_list)

        self.image_files = []
        self.text_files = []
        self.current_index = 0

        self.auto_save_var = tk.IntVar(value=1)
        self.auto_save_checkbox = tk.Checkbutton(button_frame, text="Guardar automáticamente al cambiar de imagen", variable=self.auto_save_var)
        self.auto_save_checkbox.pack(side=tk.LEFT)

        self.auto_save_checkbox.pack(side=tk.LEFT)

        self.load_image_folder()

        self.root.update()  # Actualizar la ventana para asegurarse de que esté completamente construida
        self.root.focus_force()  # Enfocar la ventana principal al inicio


    def load_image_folder(self):
        folder_path = filedialog.askdirectory(title="Selecciona la carpeta de imágenes")
        if folder_path:
            self.image_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
            self.text_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
            self.image_files.sort(key=lambda x: [int(s) if s.isdigit() else s.lower() for s in re.split('([0-9]+)', x)])
            self.text_files.sort(key=lambda x: [int(s) if s.isdigit() else s.lower() for s in re.split('([0-9]+)', x)])
            self.image_folder = folder_path
            if self.image_files:
                self.show_image(0)
                self.populate_image_list()


    def populate_image_list(self):
        self.image_list.delete(0, tk.END)
        for filename in self.image_files:
            self.image_list.insert(tk.END, filename)


    def select_image_from_list(self, event):
        if self.auto_save_var.get() == 1:  # Verifica si la casilla está marcada
            self.save_text()
        selected_index = self.image_list.curselection()
        if selected_index:
            index = int(selected_index[0])
            self.show_image(index)


    def show_image(self, index):
        image_path = os.path.join(self.image_folder, self.image_files[index])
        self.current_index = index
        image = Image.open(image_path)

        # Redimensionar la imagen si es más ancha que 512 píxeles
        if image.width > 512:
            aspect_ratio = image.width / image.height
            new_width = 512
            new_height = int(new_width / aspect_ratio)
            image = image.resize((new_width, new_height), resample=Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        text_path = os.path.join(self.image_folder, self.text_files[index])
        with open(text_path, "r") as file:
            text_content = file.read()
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text_content)

        # Actualizar el nombre de la imagen en la etiqueta
        self.image_name_label.config(text=os.path.basename(self.image_files[index]))

        # Actualizar la selección en la lista
        self.image_list.selection_clear(0, tk.END)
        self.image_list.selection_set(index)


    def show_next_image(self):
        if self.auto_save_var.get() == 1:  # Verifica si la casilla está marcada
            self.save_text()
        if self.current_index < len(self.image_files) - 1:
            self.show_image(self.current_index + 1)


    def show_prev_image(self):
        if self.auto_save_var.get() == 1:  # Verifica si la casilla está marcada
            self.save_text()
        if self.current_index > 0:
            self.show_image(self.current_index - 1)


    def skip_to_image(self):
        try:
            skip_index = int(self.skip_entry.get())
            if 0 <= skip_index < len(self.image_files):
                self.show_image(skip_index)
                self.skip_entry.delete(0, tk.END)
        except ValueError:
            pass


    def save_text(self):
        if self.current_index < len(self.image_files):
            text_path = os.path.join(self.image_folder, self.text_files[self.current_index])
            text_content = self.text_widget.get("1.0", tk.END).strip()  # Eliminar espacios al principio y al final
            with open(text_path, "w") as file:
                file.write(text_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
