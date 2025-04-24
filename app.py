
from tkinter import ttk
from tkinter import *
import sqlite3

class VentanaPrincipal():
    db="database/productos.db"


    def __init__(self, root):
        self.ventanaP=root
        self.ventanaP.title('App Gestor de Productos')
        self.ventanaP.resizable(1,1)#activa la redimensión de la ventana
        self.ventanaP.wm_iconbitmap("recursos\icon.ico")#ponemos como icono la imagen descargada

        #creación del contenedor principal (frame)
        frame = LabelFrame(self.ventanaP,text='Registrar un nuevo Producto')#esta clase crea un frame pero que ademsas se puede ver en la app
        frame.grid(row=0,column=0,pady=20,columnspan=3) #obligatorio poner la posicion para que se pueda ver y generamos 3 columnas

        #label de nombre
        self.etiqueta_nombre=Label(frame,text=('Nombre: '))
        self.etiqueta_nombre.grid(row=1,column=0)
        #entry de nombre(cajon de texto)
        self.nombre = Entry(frame)
        self.nombre.grid(row=1,column=1)
        self.nombre.focus()
        # label de precio
        self.etiqueta_precio = Label(frame, text=('Precio: '))
        self.etiqueta_precio.grid(row=2, column=0)
        # entry de precio(cajon de texto)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        #crear boton añadir producto
        self.boton_aniadir = ttk.Button(frame, text='Guardar Producto',command=self.add_productos)
        self.boton_aniadir.grid(row=3,columnspan=2, sticky=W+E) #le pasamos las coordenadas para que se situe donde queramos

        #Mensaje informativo para el usuario

        self.mensaje= Label(text='',fg='red')
        self.mensaje.grid(row=4,column=0,columnspan=2, sticky=W+E)
        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',
                                                                              11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras

        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':
                                                                             'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1

        # Botones de Eliminar y Editar
        self.boton_eliminar = ttk.Button(text='ELIMINAR',command=self.del_producto)
        self.boton_eliminar.grid(row=6, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR',command=self.editar)
        self.boton_editar.grid(row=6, column=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self,consulta,parametros=()):
        with sqlite3.connect(self.db) as con: #iniciamos una conexion con la base de datos (alias con)
            cursor = con.cursor() #generamos un cursor de la concexion para poder operar en la base de datos
            resultado=cursor.execute(consulta,parametros) #preparar la consulta SQL (con parametros si lo requiere)
            con.commit()#ejecutar la consulta SQL preparada anteriormente
        return resultado #retornar el resultado de la consulta SQL

    def get_productos(self):
        #lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children() #obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)
        #consultamos a la base de datos
        query= "SELECT * FROM producto ORDER BY nombre DESC"
        registros=self.db_consulta(query)
        for fila in registros:
            print(fila)
            self.tabla.insert(parent="",index=0,text=fila[1] ,values=fila[2])

    def validacion_nombre(self):#evaluamos si el cajon de texto esta vacio o no
        return self.nombre.get().strip()!=""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio >0
        except ValueError:
            return False

    def add_productos(self):
        if not self.validacion_nombre():
            print('El nombre es obligatorio')
            self.mensaje['text']='El nombre es obigatorio y no puede estar vacio'
            return
        if not self.validacion_precio():
            print('El precio es obligatorio')
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un numero valido mayoer que 0'
            return

        query='INSERT INTO producto VALUES(NULL,?,?)'
        parametros=(self.nombre.get(),self.precio.get())
        self.db_consulta(query,parametros)
        print('Datos guardados')
        self.mensaje['text'] = 'El producto ha sido guardado con éxito'
        self.nombre.delete(0,END) #Borrar el campo nombre del formulario
        self.precio.delete(0,END) #Borrar el campo precio del formulario

        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def editar(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
                self.mensaje['text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, mensaje):
            self.ventana_principal = ventana_principal
            self.nombre = nombre
            self.precio = precio
            self.mensaje = mensaje
            self.ventana_editar = Toplevel()
            self.ventana_editar.title("Editar Producto")
            # Creación del contenedor Frame para la edición del producto
            frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
            frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
            # Label y Entry para el Nombre antiguo (solo lectura)
            Label(frame_ep, text="Nombre antiguo: ", font=('Calibri',
                                                           13)).grid(row=1, column=0)
            Entry(frame_ep, textvariable=StringVar(self.ventana_editar,value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1,
                                                                                                               column=1)
            # Label y Entry para el Nombre nuevo
            Label(frame_ep, text="Nombre nuevo: ", font=('Calibri',13)).grid(row=2, column=0)
            self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
            self.input_nombre_nuevo.grid(row=2, column=1)
            self.input_nombre_nuevo.focus()

            # Precio antiguo (solo lectura)
            Label(frame_ep, text="Precio antiguo: ", font=('Calibri',13)).grid(row=3, column=0)
            Entry(frame_ep, textvariable=StringVar(self.ventana_editar,value=precio), state='readonly', font=('Calibri', 13)).grid(row=3,column=1)

            # Precio nuevo
            Label(frame_ep, text="Precio nuevo: ", font=('Calibri',13)).grid(row=4, column=0)
            self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
            self.input_precio_nuevo.grid(row=4, column=1)

            # Botón Actualizar Producto
            ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))

            # Ejemplo de cómo creamos y configuramos el estilo en una sola línea
            ttk.Button(frame_ep, text="Actualizar Producto",style='my.TButton', command=self.actualizar).grid(row=5,columnspan=2,sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con exito'

        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'


        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()




if __name__== "__main__":
    root = Tk() #instancia de la ventana principal
    app= VentanaPrincipal(root) #creamos objeto y le pasamos la variable root para ceder el control a la clase
    root.mainloop() #lo usamos para mantener abierta la ventana
