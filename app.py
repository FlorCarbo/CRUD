from flask import Flask #Importamos flask 
from flask import render_template, request, redirect #Importamos render_template 
from flaskext.mysql import MySQL
from datetime import datetime
import os

mysql = MySQL() #Inicializo la variable mysql 
app= Flask(__name__)

#Configuro la BD indicandole el Host, usuario, pass y DB
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema_fullstack'
mysql.init_app(app)


@app.route("/") #Aca hago que redireccione la ruta principal
def index(): #cuando alguien entre a la raiz llama a la funcion index y que vaya a index.html
    #con cada llamada quiero que se guarden los datos en la BD
    sql="SELECT * FROM `empleados`;" #Aca le estoy haciendo el select para mostrar la info en el index
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute(sql) #Comando para ejecutar el insert
    empleados= cursor.fetchall() #fetchall es para que traiga todos los datos en la variable empleados
    #print(empleados) Aca era para revisar que se imprima por consola y este OK la query
    conn.commit() #Comando para guardar el insert 
    return render_template('empleados/index.html', empleados=empleados) #agrego los empleados en forma de lista para que se pueda llamar desde el index


@app.route("/destroy/<int:id>") #Destroy 
def destroy(id): #Le mandamos que tiene que recibir un parametro
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id)) #Ejecutamos directamente el delete
    conn.commit() #Comando para guardar el insert 
    return redirect('/') #hacemos una redireccion al index para que vuelva a cargar

@app.route("/edit/<int:id>") #Editar 
def edit(id):
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados= cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados) #En el front le mando la variable empleados

@app.route("/update", methods=['POST']) #POR DEFECTO LOS METODOS QUE TRAE ES EL GET SINO HAY QUE AVISARLE QUE ES POST 
def update():
    _nombre= request.form['txtNombre'] #creo variables para que recibir los datos del form
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']
    id = request.form['txtID']
    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    datos= (_nombre, _correo, id) 
    conn=mysql.connect()
    cursor=conn.cursor()
    '''    if _foto.filename!='':
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)

        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) #Entramos al sistema Operativo y lo borramos la fila de la carpeta de las fotos
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
    '''
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')





@app.route("/create") #Aca hago que redireccione la ruta principal
def create(): 
    return render_template('empleados/create.html')


@app.route("/store", methods=['POST']) #busco la ruta /store que es el action del form para traer los datos que se envian por el metodo post
def storage():
    _nombre= request.form['txtNombre'] #creo variables para que recibir los datos del form
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']
    now = datetime.now()  
    tiempo = now.strftime("%Y%H%M%S")
    nuevoNombreFoto= tiempo + _foto.filename #Nueva variable para renombrar las fotos
    
    if _foto.filename!='':  #Pregunto si se esta seleccionando una foto para que no guarde NADA cuando no se selecciona
        _foto.save("uploads/"+nuevoNombreFoto) #Aca guardo la foto renombrada en la carpeta uploads



    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);" #Le mando los valores de las variables _nombre, _correo, _foto en orden.
    datos= (_nombre, _correo, nuevoNombreFoto) #Aca le voy poniendo el orden. Antes guardabamos _foto.filename
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute(sql, datos) #Comando para ejecutar el insert INGRESANDO LOS DATOS
    conn.commit() #Comando para guardar el insert
    return render_template('empleados/index.html')



#punto de entrada para que corra
if __name__=='__main__':
    app.run(debug=True)

