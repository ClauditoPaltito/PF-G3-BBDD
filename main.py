# Proyecto final Bases de datos
# Integrantes: Catalina Gallego, Mónica Sein, Enrique Araneda, Claudio Canales
# Grupo 3
'''
drop table if exists producto;
CREATE TABLE producto(
    Id Serial primary key,
    Producto varchar(255) not null,
    Talla varchar(255) not null,
    Descripcion varchar(255) not null,
    Tempo varchar(255) not null,
    Cantidad int not null,
    Precio numeric CHECK (Precio > 0) not null
);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Vestido','M','Color rosa pastel con flores','Primavera',1,35000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Polera','L','Manga corta color verde','Verano',2, 15000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Polar','XL','Peludito de color cafe','Invierno',1,30000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Pantalón','XXL','Marca generica de alta calidad','Primavera',1,20000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Chaqueta','M','Color negro de cuero','Otoño',1,60000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Camisa','S','Escolar de color blanco','Invierno',3,15000);

INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio)
VALUES ('Polera','XS','Color celeste con un Osito bordado','Invierno',2,10000);
'''

from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__) 
app.secret_key = 'keep it secret, keep it safe'

conn = psycopg2.connect(
    database="d1unrldo6bdpru",
    user="lsavinpbkiamhb",
    password="f41ee70603d7aef0926a09619eba7e349d47b5f83059504a6d086315e9e0175a",
    host="ec2-35-168-80-116.compute-1.amazonaws.com",
    port="5432")
conn.autocommit = True

cur = conn.cursor()
@app.route('/')
def index():
    cur.execute("Delete from producto where cantidad<1")
    cur.execute("SELECT * from producto order by Precio asc limit 10")
    rows = cur.fetchall()
    my_list = []
    for row in rows:
        my_list.append(row)
    codes = [["XS"], ['S'], ['M'], ['L'], ['XL'], ['XXL']]
    tempo = [['Invierno'],['Primavera'],['Verano'],['Otoño']]
    ordby = [['Precio'],['Cantidad'],['Id']]
    return render_template('index.html',  results=my_list , codes = codes, tempo = tempo, ordby=ordby)

@app.route('/filters',methods = ['POST'])
def filter():
    cur.execute("Delete from producto where cantidad<1")

    cur.execute("SELECT count(*) from producto")
    ro = cur.fetchall()

    cant = str(request.form.get("cantdisplay"))
    if cant == "":
        cant = f"{ro[0][0]}"

    ordby = str(request.form.get("ordby"))
    talla = str(request.form.get("talla"))

    if talla=='Filtrar Talla':
        if ordby == 'Ordenar por':
            sql="SELECT * from producto order by Precio asc limit "+cant
        else:
            sql=f"SELECT * from producto order by {ordby} asc limit {cant}"
    else:
        if ordby == 'Ordenar por':
            sql=f"SELECT * from producto where Talla='{talla}' order by Precio asc limit "+cant
        else:
            sql=f"SELECT * from producto where Talla='{talla}' order by {ordby} asc limit {cant}"

    cur.execute(sql)
    rows = cur.fetchall()

    my_list = []
    for row in rows:
        my_list.append(row)

    codes = [["XS"], ['S'], ['M'], ['L'], ['XL'], ['XXL']]
    tempo = [['Invierno'],['Primavera'],['Verano'],['Otoño']]
    ordby = [['Precio'],['Cantidad'],['Id']]

    return render_template('index.html',  results=my_list , codes = codes, tempo = tempo, ordby=ordby)


@app.route('/show/<id>')
def show(id):
    sql = "SELECT * from producto where id = "+id+" limit 1"
    cur.execute(sql)
    rows = cur.fetchall()
    producto = []
    for row in rows:
        producto.append(row)
    codes = [["XS"], ['S'], ['M'], ['L'], ['XL'], ['XXL']]
    tempo = [['Invierno'],['Primavera'],['Verano'],['Otoño']]

    return render_template('show.html',  producto=producto[0], codes=codes, tempo=tempo)


@app.route('/insert',methods = ['POST'])
def insert():    
    prod = str(request.form.get("prod"))
    desc = str(request.form.get("desc"))
    talla = str(request.form.get("talla"))
    tempo = str(request.form.get("tempo"))
    cant = str(request.form.get("cantidad"))
    price = str(request.form.get("price"))
    # En caso de existir algún campo vacio no hace nada.
    if prod == "" or desc == "" or talla == "" or tempo == "" or cant == "":
        return redirect('/')
    else:
        sql = "INSERT INTO producto (Producto, Talla, Descripcion,Tempo, Cantidad, Precio) VALUES ('"+prod+"','"+talla+"','"+desc+"','"+tempo+"','"+cant+"','"+price+"');"
        cur.execute(sql)

        return redirect('/')
    
@app.route('/search',methods = ['POST'])
def search():
    search = request.form.get("search")
    cur.execute("SELECT * from producto where producto like '%"+search+"%' order by Precio asc")
    rows = cur.fetchall()
    my_list = []
    for row in rows:
        my_list.append(row)
    codes = [["XS"], ['S'], ['M'], ['L'], ['XL'], ['XXL']]
    tempo = [['Invierno'],['Primavera'],['Verano'],['Otoño']]
    ordby = [['Precio'],['Cantidad'],['Id']]
    return render_template('index.html',  results=my_list, codes = codes, tempo = tempo, ordby=ordby)

@app.route('/delete/<id>')
def delete(id):
    sql = "Delete from producto where id = "+id
    cur.execute(sql)
    return redirect('/')

@app.route('/delete2/<id>',methods=['POST'])
def delete2(id):
    cur.execute("Delete from producto where id = "+id)
    cur.execute("Delete from producto where cantidad<1")
    cur.execute("SELECT * from producto order by cantidad asc limit 10")
    rows = cur.fetchall()
    my_list = []
    for row in rows:
        my_list.append(row)
    codes = [["XS"], ['S'], ['M'], ['L'], ['XL'], ['XXL']]
    tempo = [['Invierno'],['Primavera'],['Verano'],['Otoño']]

    return render_template('index.html',  results=my_list , codes = codes, tempo = tempo)

@app.route('/update0/<id>',methods = ['POST'])
def update0(id):
    cant = request.form.get("prod")
    if cant=='':
        return redirect('/show/'+id)
    sql = f"Update producto set Producto ='{str(cant)}' where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)

@app.route('/update1/<id>',methods = ['POST'])
def update1(id):
    cant = request.form.get("talla")
    if cant=='Modificar Talla':
        return redirect('/show/'+id)
    sql = f"Update producto set Talla ='{str(cant)}' where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)

@app.route('/update2/<id>',methods = ['POST'])
def update2(id):
    cant = request.form.get("desc")
    if cant=='':
        return redirect('/show/'+id)
    sql = f"Update producto set Descripcion ='{str(cant)}' where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)

@app.route('/update3/<id>',methods = ['POST'])
def update3(id):
    cant = request.form.get("tempo")
    if cant=='Modificar Temporada':
        return redirect('/show/'+id)
    sql = f"Update producto set Tempo ='{str(cant)}' where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)

@app.route('/update4/<id>',methods = ['POST'])
def update4(id):
    cant = request.form.get("cantidad")
    if cant=='':
        return redirect('/show/'+id)
    sql = "Update producto set Cantidad ="+ str(cant) +" where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)

@app.route('/update5/<id>',methods = ['POST'])
def update5(id):
    cant = request.form.get("price")
    if cant=='':
        return redirect('/show/'+id)
    sql = "Update producto set Precio ="+ str(cant) +" where id = "+str(id)
    cur.execute(sql)
    return redirect('/show/'+id)




#Usted solo modifique de aqui para arriba

if __name__=="__main__":
    app.run(debug=True)

