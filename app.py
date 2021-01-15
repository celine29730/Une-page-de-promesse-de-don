from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
# importation des bibliothèques: render-template permet de rendre propre une page HTML et permet de mélanger
#HTML et Python

from pymongo import MongoClient

client = MongoClient("mongodb+srv://cguill21:cguill21@cluster0.85lxk.mongodb.net/?retryWrites=true&w=majority")

db = client.don_diab.don

#db.don.insert_one ({'prenom': 'Benoît', 'nom': 'Martin', 'mail': 'bm@gmail.com', 'adresse': '15 allee des tulipes', 'montant': 200})



app = Flask(__name__)
#utilisation de Flask , name correspond au init dasn les classes python



#CONNECTION POUR LA PREMIERE PAGE
@app.route('/')
#positionnement sur le chemin de l'adresse IP
def hello():
    return render_template("info.html")


#CONNECTION POUR LA DEUXIEME PAGE
#@app.route('/suivante')
#def suivante():
#    return render_template("form.html")



@app.route('/suivante',methods=['GET', 'POST'])
def suivante():
    if request.method == 'POST':
        result = request.form
        prenom = result['prenom']
        nom = result['nom']
        mail = result['mail']
        adresse = result['adresse']
        montant = float(result['montant'])

        db.insert_one ({'prenom': prenom, 'nom': nom, 'mail': mail, 'adresse': adresse, 'montant': montant})


    #data = request.form.to_dict()
    #data['exampleInputPassword1'] = int(data['exampleInputPassword1'])
    #db.insert_one(data)
        #return render_template('info.html')
    return render_template('form.html')


#CONNECTION POUR LA troisieme PAGE
#@app.route('/bilan')
#def bilan():
#    return render_template("bilan.html")

@app.route('/bilan',methods =['GET'])
def bilan():
    
    sommedon = [{'$group': {'_id': 0, 'total': {'$sum': '$montant'}}}]
    cursor = db.aggregate(pipeline=sommedon)
    for group in cursor:
        money = group['total']
    d = db.find().count()
    return render_template("bilan.html", montanttotal = money, nbdons = d)







if __name__ == "__main__" :
    app.run(debug=True)