import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

# Funciones para guardar y cargar datos (las dejé igual)
def guardar_datos(datos):
    try:
        with open("datos_usuario.json", "r") as archivo:
            datos_existentes = json.load(archivo)
    except FileNotFoundError:
        datos_existentes = []

    datos_existentes.append(datos)
    with open("datos_usuario.json", "w") as archivo:
        json.dump(datos_existentes, archivo, indent=4)

def cargar_datos_usuario(nombre, contrasena):
    try:
        with open("datos_usuario.json", "r") as archivo:
            datos = json.load(archivo)
        for usuario in datos:
            if usuario["nombre"] == nombre and usuario["contraseña"] == contrasena:
                return usuario
    except FileNotFoundError:
        return None
    return None

class Ventana1:
    def __init__(self, root):
        self.root = root
        self.root.title("SaluVid")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")
        
        # Cargar imagen con PIL y convertir para Tkinter
       # Cargar imagen con ruta completa
        imagen = Image.open("D:\proyecto_final/Imagen_de_WhatsApp_2025-04-10_a_las_10.43.51_8186f097-removebg-preview.png")
        imagen = imagen.resize((350, 350), Image.Resampling.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(imagen)

        # Mostrar imagen en label
        label_img = tk.Label(root, image=self.img_tk, bg="#D1E7DD")
        label_img.pack(pady=10)
        
        
        tk.Label(root, text="Bienvenido", font=("Castellar", 25), bg="#D1E7DD").pack(pady=49)

        # Botones
        tk.Button(root, text="Cerrar", font=("Arial", 14), width=12, bg="#59BDCA", command=root.quit).pack(side="left", padx=20, pady=20)
        tk.Button(root, text="Siguiente", font=("Arial", 14), width=12, bg="#59BDCA", command=self.ir_a_ventana2).pack(side="right", padx=20, pady=20)

    def ir_a_ventana2(self):
       self.root.withdraw()  # Oculta Ventana1
       Ventana2(tk.Toplevel(), self.root)  # Crea Ventana2 y le pasa root

class Ventana2:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("SaluVid - Inicio")
        self.root.geometry("360x640")
        self.root.configure(bg="#71E2A9")

        tk.Label(root, text="¿Deseas iniciar sesión?", font=("Copperplate Gothic Bold", 19), bg="#77E4A0").pack(pady=20)

        tk.Button(root, text="Registrar", font=("Engravers MT", 13), width=20, bg="#D6E580", command=self.ir_a_ventana3).pack(pady=25)
        tk.Button(root, text="Inicia Sesión", font=("Engravers MT", 14), width=20, bg="#D6E580", command=self.iniciar_sesion).pack(pady=25)
        tk.Button(root, text="Quizá más tarde", font=("Engravers MT", 13), width=20, bg="#D6E580", command=self.ir_a_quizas_mas_tarde).pack(pady=25)
        tk.Button(root, text="Cerrar", font=("Arial", 14), width=20, bg="#D6E580", command=self.cerrar_todo).pack(pady=20)

    def ir_a_ventana3(self):
        self.root.withdraw()
        Ventana3(tk.Toplevel(), self.root)

    def iniciar_sesion(self):
        self.root.withdraw()
        VentanaLogin(tk.Toplevel(), self.root)

    def ir_a_quizas_mas_tarde(self):
        self.root.withdraw()
        VentanaQuizasMasTarde(tk.Toplevel(), self.ventana_anterior)
        
    def cerrar_todo(self):
        self.root.destroy()
        self.ventana_anterior.destroy()

class Ventana3():
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Registro")
        self.root.geometry("360x640")
        self.root.configure(bg="#70E2E2")

        tk.Label(root, text="Ingresa tus datos", font=("Copperplate Gothic Bold", 19), bg="#70E2E2").pack(pady=10)

        tk.Label(root, text="Nombre:").pack()
        self.nombre = tk.Entry(root)
        self.nombre.pack()

        tk.Label(root, text="Sexo:").pack()
        self.sexo = tk.StringVar()
        tk.Radiobutton(root, text="Femenino", variable=self.sexo, value="Femenino").pack()
        tk.Radiobutton(root, text="Masculino", variable=self.sexo, value="Masculino").pack()

        tk.Label(root, text="Edad:").pack()
        self.edad = tk.StringVar()
        edades = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70"]
        tk.OptionMenu(root, self.edad, *edades).pack()

        tk.Label(root, text="Altura (cm):").pack()
        self.altura = tk.Entry(root)
        self.altura.pack()

        tk.Label(root, text="Peso (kg):").pack()
        self.peso = tk.Entry(root)
        self.peso.pack()

        tk.Label(root, text="Contraseña:").pack()
        self.contraseña = tk.Entry(root, show="*")
        self.contraseña.pack()

        tk.Button(root, text="Siguiente", command=self.calcular_imc).pack(pady=10)
        tk.Button(root, text="Regresar", command=self.regresar_a_ventana_anterior).pack()


    def calcular_imc(self):
        try:
            peso = float(self.peso.get())
            altura = float(self.altura.get()) / 100
            imc = peso / (altura ** 2)
            datos = {
                "nombre": self.nombre.get(),
                "sexo": self.sexo.get(),
                "edad": self.edad.get(),
                "altura": self.altura.get(),
                "peso": self.peso.get(),
                "contraseña": self.contraseña.get(),
                "imc": imc
            }
            guardar_datos(datos)

            ventana4 = tk.Toplevel()
            self.root.withdraw()
            Ventana4(ventana4, imc, self.sexo.get(), self.edad.get(), ventana_anterior=self.root, desde_registro=True, ventana3=self.root)

        except ValueError:
            tk.Label(self.root, text="Error en los datos", fg="red").pack()

    def regresar_a_ventana_anterior(self):
        self.root.destroy()  # O puedes usar withdraw() si quieres solo ocultar
        self.ventana_anterior.deiconify()


class Ventana4:
    def __init__(self, root, imc, genero, edad, ventana_anterior=None, desde_registro=False, ventana3=None):
        self.root = root
        self.root.title("Resultado IMC")
        self.root.geometry("360x640")
        self.root.configure(bg="#FF6AFF")
        self.desde_registro = desde_registro
        self.ventana_anterior = ventana_anterior
        self.ventana3 = ventana3  # <- nueva línea

        tk.Label(root, text=f"Tu IMC es: {imc:.2f}", font=("Copperplate Gothic Bold", 20), bg="#FF6AFF").pack(pady=43)
        tk.Button(root, text="Continuar", font=("Arial", 14), width=20, bg="#97D6DF",
                  command=lambda: self.ir_a_ventana5(imc, genero, edad)).pack(pady=43)
        
    def ir_a_ventana5(self, imc, genero, edad):
        self.root.destroy()
        Ventana5(tk.Toplevel(), imc, genero, edad, ventana3=self.ventana3, from_login=False)

    def volver_a_ventana_anterior(self):
        self.root.destroy()
    # YA NO SE REACTIVA ventana_anterior (Ventana3)


class Ventana5:
    def __init__(self, root, imc, genero, edad, ventana3=None, from_login=False):
        self.root = root
        self.root.title("Inicio")
        self.root.geometry("360x640")
        self.root.configure(bg="#CCCCCB")
        self.imc = imc
        self.genero = genero
        self.edad = edad
        self.from_login = from_login
        self.ventana3 = ventana3  # <- ahora la tiene

        tk.Label(root, text="¡Con qué deseas comenzar!", font=("Copperplate Gothic Bold", 16), bg="#CCCCCB").pack(pady=43)

        tk.Button(root, text="Dieta", font=("Engravers MT", 13), width=20, bg="#E2BF92",
                  command=self.ir_a_dieta).pack(pady=43)
        tk.Button(root, text="Ejercicio", font=("Engravers MT", 13), width=20, bg="#E2BF92",
                  command=self.ir_a_ejercicio).pack(pady=43)
        tk.Button(root, text="Regresar", font=("Engravers MT", 12), width=20, bg="#E2BF92",
                  command=self.volver).pack(pady=43)

    def ir_a_dieta(self):
        self.root.withdraw()
        VentanaDieta(tk.Toplevel(), self.root, self.imc, self.genero, self.edad, self.from_login)

    def ir_a_ejercicio(self):
        self.root.withdraw()
        VentanaEjercicio(tk.Toplevel(), self.root, self.imc, self.genero, self.edad, self.from_login)

    def volver(self):
        self.root.destroy()
        if self.from_login:
            VentanaLogin(tk.Tk(), None)
        else:
            self.ventana3.deiconify()  # <- vuelve directamente a Ventana3

class VentanaDieta: 
    def __init__(self, root, ventana_anterior, imc, genero, edad, from_login):
        self.ventana_anterior = ventana_anterior
        self.root = root
        self.root.title("Dieta")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")
        self.imc = imc
        self.genero = genero
        self.edad = edad
        self.from_login = from_login

        tk.Label(root, text="Opciones de dieta", font=("Copperplate Gothic Bold", 19), bg="#D1E7DD").pack(pady=10)

        texto_dietas = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_dietas.pack(padx=10, pady=10, expand=True, fill="both")

        dietas = self.obtener_dietas_por_imc(imc)
        texto_dietas.insert("1.0", dietas)
        texto_dietas.config(state="disabled")  # Para que no se pueda editar

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.regresar).pack(pady=10)

    def obtener_dietas_por_imc(self, imc):
        if imc < 18.5:
            return """DIETAS PARA BAJO PESO:

1. Dieta alta en calorías y proteínas:
Desayuno: Taza de leche entera con cereales hinchados de maíz y chocolate negro.
Media mañana: Bocadillo de jamón y queso mozzarella.
Comida: Puré de calabaza, arroz con pavo y una naranja.
Merienda: Plátano y tostada con tahín.
Cena: Ensalada de aguacate y tortilla de patatas.

2. Dieta rica en carbohidratos:
Desayuno: Leche entera con cereales, tostada con mermelada, plátano.
Media mañana: Frutos secos y yogur.
Comida: Arroz con verdura y pescado, pan con aceite.
Merienda: Tostada con miel y zumo de frutas.
Cena: Pasta con carne y ensalada.

3. Dieta con grasas saludables:
Desayuno: Tostadas con mantequilla y aguacate, huevo y leche.
Media mañana: Nueces y fruta.
Comida: Pescado con verduras al vapor y patatas.
Merienda: Yogur con frutos secos.
Cena: Pasta con tomate, aguacate y aceite de oliva.

4. Dieta con batidos:
Desayuno: Batido de leche, plátano y miel.
Media mañana: Yogur y fruta seca.
Comida: Pasta con carne y puré de verduras.
Merienda: Batido de frutas y yogur.
Cena: Ensalada de frutas y batido de leche.

5. Dieta equilibrada:
Desayuno: Pan integral con aguacate y huevo, leche entera.
Media mañana: Fruta y yogur.
Comida: Pescado con verduras, pan con tomate.
Merienda: Fruta y nueces.
Cena: Pasta con salsa de tomate y ensalada."""
        
        elif 18.5 <= imc < 25:
            return """DIETAS PARA PESO NORMAL:

1. Dieta mediterránea:
Desayuno: Yogur natural con avena, frutas y nueces.
Media mañana: Fruta de temporada.
Comida: Ensalada mixta, arroz integral con pescado y verduras.
Merienda: Pan integral con aceite de oliva.
Cena: Verduras al horno y pechuga de pollo.

2. Dieta equilibrada:
Desayuno: Pan integral con aguacate, huevo cocido, leche vegetal.
Media mañana: Yogur y nueces.
Comida: Lentejas con arroz y ensalada.
Merienda: Batido natural de frutas.
Cena: Pescado al vapor con verduras.

3. Dieta flexitariana:
Desayuno: Smoothie de plátano, avena y almendras.
Media mañana: Barrita de cereales y fruta.
Comida: Tacos vegetales con frijoles y aguacate.
Merienda: Yogur natural.
Cena: Sopa de verduras y pan integral.

4. Dieta DASH:
Desayuno: Avena con leche descremada, plátano y canela.
Media mañana: Puñado de nueces.
Comida: Pechuga de pollo, brócoli y arroz integral.
Merienda: Fruta y yogur natural.
Cena: Ensalada con huevo duro y pan integral.

5. Dieta rica en fibra:
Desayuno: Pan integral con mermelada baja en azúcar.
Media mañana: Fruta fresca.
Comida: Sopa de verduras, lentejas y ensalada.
Merienda: Galletas integrales y té verde.
Cena: Puré de calabaza y pescado blanco."""
        
        elif imc >= 25:
            return """DIETAS PARA SOBREPESO:

1. Dieta hipocalórica:
Desayuno: Yogur bajo en grasa con avena y fruta.
Media mañana: Manzana o zanahoria.
Comida: Sopa de verduras, filete de pollo a la plancha y ensalada.
Merienda: Infusión y galletas integrales.
Cena: Verduras al vapor con pescado blanco.

2. Dieta cetogénica:
Desayuno: Huevos con aguacate.
Media mañana: Puñado de almendras.
Comida: Carne con verduras bajas en carbohidratos.
Merienda: Queso bajo en grasa.
Cena: Sopa de coliflor y salmón.

3. Dieta baja en carbohidratos:
Desayuno: Tortilla con espinacas y tomate.
Media mañana: Yogur natural.
Comida: Pollo a la plancha con ensalada de espinacas.
Merienda: Gelatina sin azúcar.
Cena: Crema de calabacín y huevo cocido.

4. Dieta con control de porciones:
Desayuno: Tostadas integrales con aguacate.
Media mañana: Fruta pequeña.
Comida: Plato pequeño de arroz con pollo y verduras.
Merienda: Yogur desnatado.
Cena: Sopa ligera y ensalada.

5. Dieta basada en vegetales:
Desayuno: Avena con leche de almendra y plátano.
Media mañana: Zumo natural.
Comida: Ensalada completa con legumbres.
Merienda: Barrita de semillas.
Cena: Puré de zanahoria con tofu."""
        
        else:
            return "IMC no reconocido. No se pueden mostrar las dietas."

    def regresar(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()

class VentanaEjercicio: 
    def __init__(self, root, ventana_anterior, imc, genero, edad, from_login):
        self.ventana_anterior = ventana_anterior
        self.root = root
        self.root.title("Ejercicio")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")
        self.imc = imc
        self.genero = genero
        self.edad = edad
        self.from_login = from_login

        tk.Label(root, text="Opciones de ejercicio", font=("Copperplate Gothic Bold", 19), bg="#D1E7DD").pack(pady=10)

        texto_ejercicios = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_ejercicios.pack(padx=10, pady=10, expand=True, fill="both")

        ejercicios = self.obtener_ejercicios_por_imc(imc)
        texto_ejercicios.insert("1.0", ejercicios)
        texto_ejercicios.config(state="disabled")  # Para evitar edición

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.regresar).pack(pady=10)

    def obtener_ejercicios_por_imc(self, imc):
        if imc < 18.5:
            return """EJERCICIOS PARA BAJO PESO:

1. Caminata ligera:
Duración: 30 minutos diarios.
Objetivo: Estimular el apetito y mejorar la circulación.

2. Yoga para principiantes:
Duración: 20 minutos.
Ejercicios: Postura del gato, perro boca abajo, cobra.
Objetivo: Fortalecer sin gastar demasiadas calorías.

3. Ejercicios con peso corporal:
Flexiones, sentadillas, abdominales suaves (3 veces por semana).
Objetivo: Ganar tono muscular.

4. Bicicleta estática en baja resistencia:
Duración: 15-20 minutos.
Objetivo: Activar el cuerpo sin alto desgaste.

5. Estiramientos y movilidad:
Duración: 10 minutos diarios.
Objetivo: Mejorar la postura y evitar lesiones.

"""
        elif 18.5 <= imc < 25:
            return """EJERCICIOS PARA PESO NORMAL:

1. Cardio moderado:
Duración: 30-45 minutos (3-4 veces por semana).
Ejemplos: correr suave, nadar, bailar.

2. Rutina de fuerza:
Duración: 30 minutos (2-3 veces por semana).
Ejercicios: Flexiones, sentadillas, peso corporal o pesas.

3. HIIT ligero:
Duración: 20 minutos.
Circuito de 30 seg trabajo + 15 seg descanso.
Ejemplo: jumping jacks, abdominales, mountain climbers.

4. Yoga o Pilates:
Duración: 30 minutos.
Objetivo: Mejorar equilibrio y flexibilidad.

5. Caminatas largas o senderismo:
Duración: 1 hora (fines de semana).
Objetivo: Mantener condición física con bajo impacto.

"""
        elif imc >= 25:
            return """EJERCICIOS PARA SOBREPESO:

1. Caminata diaria:
Duración: 30-45 minutos diarios.
Objetivo: Quemar grasa sin impacto fuerte en articulaciones.

2. Ejercicios acuáticos:
Duración: 45 minutos.
Ejemplo: Natación, aquagym.
Objetivo: Bajar peso sin impacto.

3. Bicicleta estática o elíptica:
Duración: 30 minutos (4-5 veces por semana).
Intensidad: Moderada.

4. Ejercicios funcionales de bajo impacto:
Duración: 25 minutos.
Ejemplo: sentadillas al aire, estiramientos, steps suaves.

5. Ejercicios de respiración y movilidad:
Duración: 15 minutos diarios.
Objetivo: Activar el cuerpo, relajar la mente.

"""
        else:
            return "IMC no reconocido. No se pueden mostrar los ejercicios."

    def regresar(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()

class VentanaLogin:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Login")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.pack()

        tk.Label(root, text="Contraseña:").pack()
        self.contraseña_entry = tk.Entry(root, show="*")
        self.contraseña_entry.pack()

        tk.Button(root, text="Entrar", command=self.verificar).pack(pady=10)
        tk.Button(root, text="Regresar", command=self.volver_a_ventana2).pack(pady=10)

    def verificar(self):
        nombre = self.nombre_entry.get()
        contrasena = self.contraseña_entry.get()
        datos = cargar_datos_usuario(nombre, contrasena)
        if datos:
            self.root.destroy()
            Ventana5(tk.Tk(), datos["imc"], datos["sexo"], datos["edad"], from_login=True)
        else:
            tk.Label(self.root, text="Datos incorrectos", fg="red").pack()

    def volver_a_ventana2(self):
        try:
            self.root.destroy()  # Cierra solo la ventana de login
            if self.ventana_anterior:
               self.ventana_anterior.deiconify()  # Muestra la ventana anterior si está viva
        except Exception as e:
            print(f"Error al regresar: {e}")


class VentanaQuizasMasTarde:
    def __init__(self, root, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.root = root
        self.root.title("Objetivo")
        self.root.geometry("360x640")
        self.root.configure(bg="#FFD1DC")

        tk.Label(root, text="¿Qué es lo que deseas?", font=("Arial", 16), bg="#FFD1DC").pack(pady=20)

        tk.Button(root, text="Bajar peso", font=("Arial", 14), width=20, bg="#B0E0E6",
                  command=self.ir_a_bajar_peso).pack(pady=10)

        tk.Button(root, text="Subir peso", font=("Arial", 14), width=20, bg="#B0E0E6",
                  command=self.ir_a_subir_peso).pack(pady=10)

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  bg="#B0E0E6", command=self.volver_a_ventana2).pack(pady=30)

    def ir_a_bajar_peso(self):
        self.root.withdraw()  # en vez de destroy, para poder volver
        VentanaBajarPeso(tk.Toplevel(), self.root)  # o self para pasar la ventana

    def ir_a_subir_peso(self):
        self.root.withdraw()
        VentanaSubirPeso(tk.Toplevel(), self.root)


    def volver_a_ventana2(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()
        

class VentanaBajarPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Elegir inicio - Bajar Peso")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="¿Con qué deseas empezar?", font=("Copperplate Gothic Bold", 18), bg="#D1E7DD").pack(pady=20)

        tk.Button(root, text="Dieta", font=("Engravers MT", 14), width=20, bg="#58D68D",
                  command=self.ir_a_dieta_bajar_peso).pack(pady=40)

        tk.Button(root, text="Ejercicio", font=("Engravers MT", 14), width=20, bg="#58D68D",
                  command=self.ir_a_ejercicio_bajar_peso).pack(pady=40)

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  bg="#58D68D", command=self.volver_a_objetivo).pack(pady=30)

    def ir_a_dieta_bajar_peso(self):
        self.root.withdraw()  # Ocultamos esta ventana pero no la destruimos
        VentanaDietaBajarPeso(tk.Toplevel(self.root), self)  # Pasamos self para poder regresar

    def ir_a_ejercicio_bajar_peso(self):
        self.root.withdraw()
        VentanaEjercicioBajarPeso(tk.Toplevel(self.root), self)
        
    def volver_a_objetivo(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()

class VentanaDietaBajarPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Dietas para Bajar de Peso")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="Opciones de Dieta para Bajar de Peso", font=("Copperplate Gothic Bold", 11), bg="#D1E7DD").pack(pady=10)

        texto_dietas = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_dietas.pack(padx=10, pady=10, expand=True, fill="both")

        dietas_texto = """DIETAS PARA BAJAR DE PESO:

1. Dieta Hipocalórica:
Desayuno: Yogur natural con avena y fresas.
Media mañana: Manzana verde.
Comida: Pechuga de pollo a la plancha con ensalada mixta y arroz integral.
Merienda: Un puñado de nueces o una gelatina light.
Cena: Sopa de verduras y pescado a la plancha.

2. Dieta Cetogénica (Keto):
Desayuno: Huevos revueltos con aguacate.
Media mañana: Almendras o queso bajo en grasa.
Comida: Pollo al horno con brócoli al vapor.
Merienda: Yogur griego sin azúcar con nueces.
Cena: Ensalada con atún, aceite de oliva y huevo cocido.

3. Dieta Mediterránea:
Desayuno: Tostada de pan integral con aceite de oliva y tomate.
Media mañana: Fruta (manzana o pera).
Comida: Pescado con vegetales al vapor y quinoa.
Merienda: Yogur natural y frutos secos.
Cena: Ensalada de vegetales con pollo a la plancha.

4. Dieta Vegetariana para perder peso:
Desayuno: Smoothie verde (espinaca, manzana, plátano y agua).
Media mañana: Zanahorias baby o pepinos con limón.
Comida: Tofu salteado con arroz integral y verduras.
Merienda: Un puñado de semillas de girasol o nueces.
Cena: Crema de calabaza y ensalada mixta.

5. Dieta de Ayuno Intermitente (16:8):
Ventana de alimentación de 12:00 p.m. a 8:00 p.m.
Primera comida (12:00): Ensalada grande con pollo, aguacate y vegetales.
Merienda (4:00): Yogur con semillas de chía y frutos rojos.
Cena (7:30): Sopa de verduras y pescado al vapor.

"""

        texto_dietas.insert("1.0", dietas_texto)
        texto_dietas.config(state="disabled")  # Solo lectura

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.volver_a_bajar_peso,
                  bg="#F5B7B1", fg="white").pack(pady=10)

    def volver_a_bajar_peso(self):
        self.root.destroy()
        self.ventana_anterior.root.deiconify()  # <- Así sí regresas a la pantalla anterior correcta




class VentanaEjercicioBajarPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Ejercicios para Bajar de Peso")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="Rutinas de Ejercicio para Bajar de Peso", font=("Copperplate Gothic Bold", 11), bg="#D1E7DD").pack(pady=10)

        texto_ejercicios = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_ejercicios.pack(padx=10, pady=10, expand=True, fill="both")

        ejercicios_texto = """RUTINAS DE EJERCICIO PARA BAJAR DE PESO:

1. Caminata Rápida:
Duración: 30-45 minutos diarios.
Beneficios: Quema calorías, mejora la circulación y fortalece piernas y glúteos.
Recomendación: Mantener un paso constante e incorporar cuestas o escaleras.

2. Ciclismo:
Duración: 45-60 minutos, 3 a 4 veces por semana.
Beneficios: Excelente para el sistema cardiovascular, quema grasa y fortalece el tren inferior.
Consejo: Alternar entre intensidad baja y alta durante el trayecto.

3. Cardio HIIT (Entrenamiento por intervalos de alta intensidad):
Duración: 20-30 minutos.
Ejemplo: 40 segundos de salto de tijera, 20 segundos de descanso; repetir con sentadillas, burpees y mountain climbers.
Beneficios: Quema grasa rápidamente y mejora la resistencia en poco tiempo.

4. Natación:
Duración: 45-60 minutos, 2 a 3 veces por semana.
Beneficios: Trabajo completo del cuerpo, bajo impacto en las articulaciones, alta quema calórica.
Sugerencia: Alternar estilos (crol, braza, espalda) para trabajar distintos músculos.

5. Entrenamiento Funcional:
Duración: 30-40 minutos por sesión.
Ejercicios: Sentadillas, zancadas, flexiones, saltos, abdominales.
Beneficios: Mejora fuerza, equilibrio y quema grasa corporal con el propio peso.
Ideal para: Personas que prefieren rutinas en casa sin necesidad de equipo.

"""

        texto_ejercicios.insert("1.0", ejercicios_texto)
        texto_ejercicios.config(state="disabled")  # Solo lectura

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.volver_a_bajar_peso,
                  bg="#F5B7B1", fg="white").pack(pady=10)

    def volver_a_bajar_peso(self):
        self.root.destroy()
        self.ventana_anterior.root.deiconify()



        
class VentanaSubirPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Elegir inicio")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="¿Con qué deseas empezar?", font=("Copperplate Gothic Bold", 18), bg="#D1E7DD").pack(pady=20)

        tk.Button(root, text="Dieta", font=("Engravers MT", 14), width=20, bg="#58D68D",
                  command=self.ir_a_dieta_subir_peso).pack(pady=40)

        tk.Button(root, text="Ejercicio", font=("Engravers MT", 14), width=20, bg="#58D68D",
                  command=self.ir_a_ejercicio_subir_peso).pack(pady=40)

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  bg="#58D68D", command=self.volver_a_objetivo).pack(pady=30)

    def ir_a_dieta_subir_peso(self):
        self.root.withdraw()
        VentanaDietaSubirPeso(tk.Toplevel(self.root), self.root)

    def ir_a_ejercicio_subir_peso(self):
        self.root.withdraw()
        VentanaEjercicioSubirPeso(tk.Toplevel(self.root), self.root)

    def volver_a_objetivo(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()

class VentanaDietaSubirPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Dietas para Subir de Peso")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="Opciones de Dieta para Subir de Peso", font=("Copperplate Gothic Bold", 11), bg="#D1E7DD").pack(pady=10)

        texto_dietas = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_dietas.pack(padx=10, pady=10, expand=True, fill="both")

        dietas_texto = """DIETAS PARA SUBIR DE PESO:

1. Dieta Hipercalórica:
Desayuno: Pan integral con aguacate, huevo frito y un batido de plátano con leche entera.
Media mañana: Yogur griego con nueces y miel.
Comida: Pasta con salsa de carne y queso rallado, pan y aguacate.
Merienda: Batido de leche con crema de cacahuate.
Cena: Arroz con pollo al curry, ensalada con aceite de oliva y pan.

2. Dieta Rica en Proteínas:
Desayuno: Huevos revueltos con jamón y pan integral, leche con cacao.
Media mañana: Licuado de proteína con frutas y almendras.
Comida: Lentejas con arroz y carne magra, verduras al vapor.
Merienda: Queso panela con pan y un plátano.
Cena: Tortilla de atún, aguacate, y yogur natural.

3. Dieta con Batidos Nutritivos:
Desayuno: Batido de leche, avena, plátano, miel y crema de cacahuate.
Media mañana: Frutos secos y galletas integrales.
Comida: Arroz con frijoles y carne, con ensalada y aguacate.
Merienda: Batido de yogur, avena y mango.
Cena: Sopa cremosa de verduras, pescado empanizado y pan.

4. Dieta de 5-6 Comidas al Día:
Desayuno: Pan con queso crema y mermelada, jugo natural.
Media mañana: Batido de leche con frutas y frutos secos.
Comida: Pollo con papas, arroz y pan.
Merienda: Yogur con granola y plátano.
Cena: Ensalada con atún, huevo, aguacate y pan integral.
Antes de dormir: Vaso de leche con galletas integrales.

5. Dieta con Grasas Saludables:
Desayuno: Avena con nueces, chía, pasas y leche entera.
Media mañana: Tostadas con aguacate y aceite de oliva.
Comida: Salmón al horno, puré de papas y espinacas.
Merienda: Batido de leche, mango y almendras.
Cena: Arroz integral con huevo frito y ensalada con nueces y aceite de linaza.
"""

        texto_dietas.insert("1.0", dietas_texto)
        texto_dietas.config(state="disabled")  # Solo lectura

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.volver_a_subir_peso,
                  bg="#58D68D", fg="white").pack(pady=10)

    def volver_a_subir_peso(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()


class VentanaEjercicioSubirPeso:
    def __init__(self, root, ventana_anterior):
        self.root = root
        self.ventana_anterior = ventana_anterior
        self.root.title("Ejercicios para Subir de Peso")
        self.root.geometry("360x640")
        self.root.configure(bg="#D1E7DD")

        tk.Label(root, text="Ejercicios para Ganar Masa Muscular", font=("Copperplate Gothic Bold", 11), bg="#D1E7DD").pack(pady=10)

        texto_ejercicios = tk.Text(root, wrap="word", font=("Bahnschrift SemiLight", 13), bg="#D1E7DD", relief="flat")
        texto_ejercicios.pack(padx=10, pady=10, expand=True, fill="both")

        ejercicios_texto = """EJERCICIOS PARA SUBIR DE PESO:

1. Entrenamiento con pesas:
Ejercita con mancuernas o barras para trabajar grupos musculares grandes. Realiza series de 8 a 12 repeticiones con peso progresivo. Ideal para pecho, espalda, brazos y piernas.

2. Sentadillas y peso muerto:
Estos ejercicios compuestos estimulan el crecimiento muscular total. Las sentadillas fortalecen glúteos y muslos, mientras que el peso muerto trabaja toda la cadena posterior (espalda, glúteos y piernas).

3. Ejercicios de resistencia:
Utiliza bandas elásticas o poleas para ofrecer resistencia constante. Ayudan a mejorar la fuerza muscular sin tanto impacto en articulaciones, ideal para principiantes.

4. Rutina de fuerza progresiva:
Aumenta progresivamente el peso o la dificultad de los ejercicios semana tras semana. Esto fuerza al músculo a adaptarse y crecer. Incluye ejercicios como presses, dominadas y zancadas.

5. Entrenamiento dividido (push/pull/legs):
Divide tu rutina semanal en empujes (pecho, tríceps, hombros), jalones (espalda, bíceps) y piernas. Entrena cada grupo 1 o 2 veces por semana para maximizar el volumen muscular.

Recomendación: realiza cada rutina al menos 3-5 días a la semana, acompañada de una dieta rica en calorías y proteínas para ver resultados efectivos.
"""

        texto_ejercicios.insert("1.0", ejercicios_texto)
        texto_ejercicios.config(state="disabled")  # Solo lectura

        tk.Button(root, text="Regresar", font=("Arial", 14), width=20,
                  command=self.volver_a_subir_peso,
                  bg="#58D68D", fg="white").pack(pady=10)

    def volver_a_subir_peso(self):
        self.root.destroy()
        self.ventana_anterior.deiconify()



# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana1(root)
    root.mainloop()
