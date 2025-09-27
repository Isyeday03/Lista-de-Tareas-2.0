import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json, os

class TodoApp:
    """
    Aplicación GUI de Lista de Tareas usando Tkinter
    
    Permite al usuario:
    - Añadir nuevas tareas
    - Marcar tareas como completadas
    - Eliminar tareas
    - Guardar y cargar tareas automáticamente
    """
    
    def __init__(self, root):
        """
        Inicializa la aplicación de lista de tareas
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Lista de Tareas")
        self.tareas = []
        self.archivo = "tareas.json"
        self.ui()
        self.cargar()
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def ui(self):
        """
        Crea todos los elementos de la interfaz gráfica de usuario
        """
        ttk.Label(self.root, text="📝 Lista de Tareas", font=("Arial", 16, "bold")).pack(pady=10)
        f = ttk.Frame(self.root); f.pack(pady=5, fill='x')
        self.e = ttk.Entry(f, font=("Arial", 11)); self.e.pack(side='left', fill='x', expand=True)
        self.e.bind('<Return>', lambda _: self.add())
        ttk.Button(f, text="Añadir", command=self.add).pack(side='left', padx=5)
        self.tree = ttk.Treeview(self.root, columns=("estado", "tarea", "fecha"), show="headings", height=12)
        for c, w in zip(("estado", "tarea", "fecha"), (80, 250, 120)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor=tk.CENTER)
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', lambda _: self.comp())
        b = ttk.Frame(self.root); b.pack(pady=5)
        ttk.Button(b, text="Completar", command=self.comp).pack(side='left', padx=5)
        ttk.Button(b, text="Eliminar", command=self.elim).pack(side='left', padx=5)
        ttk.Button(b, text="Limpiar Completadas", command=self.limp).pack(side='left', padx=5)
        self.stats = ttk.Label(self.root, text=""); self.stats.pack(pady=5)

    def add(self):
        """
        Añade una nueva tarea a la lista
        """
        t = self.e.get().strip()
        if t:
            self.tareas.append({"texto": t, "completada": False, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")})
            self.e.delete(0, tk.END)
            self.upd(); self.guardar()

    def comp(self):
        """
        Marca la tarea seleccionada como completada o pendiente
        """
        s = self.tree.selection()
        if s:
            i = self.tree.index(s[0])
            self.tareas[i]["completada"] = not self.tareas[i]["completada"]
            self.upd(); self.guardar()

    def elim(self):
        """
        Elimina la tarea seleccionada de la lista
        """
        s = self.tree.selection()
        if s:
            i = self.tree.index(s[0])
            del self.tareas[i]
            self.upd(); self.guardar()

    def limp(self):
        """
        Elimina todas las tareas marcadas como completadas
        """
        self.tareas = [t for t in self.tareas if not t["completada"]]
        self.upd(); self.guardar()

    def upd(self):
        """
        Actualiza la visualización de la lista de tareas en el Treeview
        """
        self.tree.delete(*self.tree.get_children())
        for t in self.tareas:
            estado = "✅" if t["completada"] else "⏳"
            self.tree.insert("", tk.END, values=(estado, t["texto"], t["fecha"]))
        total = len(self.tareas)
        comp = sum(t["completada"] for t in self.tareas)
        self.stats.config(text=f"Total: {total} | Pendientes: {total-comp} | Completadas: {comp}")

    def guardar(self):
        """
        Guarda las tareas en un archivo JSON para persistencia
        """
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.tareas, f, ensure_ascii=False)
        except: pass

    def cargar(self):
        """
        Carga las tareas desde el archivo JSON si existe
        """
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    self.tareas = json.load(f)
            except: self.tareas = []
        self.upd()

    def salir(self):
        """
        Maneja el evento de cierre de la aplicación
        """
        self.guardar()
        self.root.destroy()

def main():
    """
    Función principal para ejecutar la aplicación
    """
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()