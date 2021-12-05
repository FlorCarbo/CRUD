from flask import Flask #Importamos flask 
from flask import render_template, request #Importamos render_template 
from flaskext.mysql import MySQL

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
    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Gonzalo Cabrera', 'gonza@gmail.com', 'foto.jpeg');"
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute(sql) #Comando para ejecutar el insert
    conn.commit() #Comando para guardar el insert
    return render_template('empleados/index.html')

@app.route("/create") #Aca hago que redireccione la ruta principal
def create(): 
    return render_template('empleados/create.html')


@app.route("/store", methods=['POST'])
def storage():
    _nombre= request.form['txtNombre'] #creo variables para que recibir los datos del form
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']

    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);" #Le mando los valores de las variables _nombre, _correo, _foto en orden.
    datos= (_nombre, _correo, _foto) #Aca le voy poniendo el orden.
    conn=mysql.connect() #Comando para conectarse con la BBDD
    cursor=conn.cursor() #Comando para almacenar lo que ejecutamos
    cursor.execute(sql, datos) #Comando para ejecutar el insert INGRESANDO LOS DATOS
    conn.commit() #Comando para guardar el insert
    return render_template('empleados/index.html')



#punto de entrada para que corra
if __name__=='__main__':
    app.run(debug=True)

