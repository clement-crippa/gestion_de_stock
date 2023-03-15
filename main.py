import mysql.connector
from tkinter import *
from tkinter import ttk

admin = mysql.connector.connect(host="localhost", user="root", password="rootmdp", database="boutique")
cursor = admin.cursor()
# Fenêtre principale
Stockage = Tk()
Stockage.title("Stock boutique")
Stockage.geometry("800x800")
# Variable
Nom = StringVar()
Description = StringVar()
Prix = StringVar()
Quantite = StringVar()
ID_CATEGORIE = StringVar()


# Remplis toutes les cases automatiquement quand une sélection est effectuée
def Selection(event):
    id = tableau_stock.selection()[0]
    Nom.set(tableau_stock.item(id, "values")[1])
    Description.set(tableau_stock.item(id, "values")[2])
    Prix.set(tableau_stock.item(id, "values")[3])
    Quantite.set(tableau_stock.item(id, "values")[4])
    ID_CATEGORIE.set(tableau_stock.item(id, "values")[5])


# Petite fenêtre
tableau = LabelFrame(Stockage, text="Stock")
tableau.place(x=30, width=750, height=450)

labelNom = Label(tableau, text="Nom")
labelNom.grid(column=0, row=0, padx=5, pady=5)
texteNom = Entry(tableau, textvariable=Nom)
texteNom.grid(column=1, row=0)

labelDescription = Label(tableau, text="Description")
labelDescription.grid(column=0, row=2, pady=5, padx=5)
texteDescription = Entry(tableau, textvariable=Description)
texteDescription.grid(column=1, row=2)

labelPrix = Label(tableau, text="Prix")
labelPrix.grid(column=2, row=0, pady=5, padx=5)
textePrix = Entry(tableau, textvariable=Prix)
textePrix.grid(column=3, row=0)

labelQuantite = Label(tableau, text="Quantité")
labelQuantite.grid(column=2, row=1, pady=5, padx=5)
texteQuantite = Entry(tableau, textvariable=Quantite)
texteQuantite.grid(column=3, row=1)

labelID_CATEGORIE = Label(tableau, text="ID Catégorie")
labelID_CATEGORIE.grid(column=2, row=2, pady=5, padx=5)
texteID_CATEGORIE = Entry(tableau, textvariable=ID_CATEGORIE)
texteID_CATEGORIE.grid(column=3, row=2)
# Taille des colonnes
tableau_stock = ttk.Treeview(tableau)
tableau_stock.grid(column=0, row=3, columnspan=7, padx=5)
tableau_stock["columns"] = ("ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie", "Nom Catégorie")
tableau_stock.column("#0", width=0, stretch=NO)
tableau_stock.column("ID", width=75, anchor=CENTER)
tableau_stock.column("Nom", width=75, anchor=CENTER)
tableau_stock.column("Description", width=100, anchor=CENTER)
tableau_stock.column("Quantité", width=100, anchor=CENTER)
tableau_stock.column("Prix", width=75, anchor=CENTER)
tableau_stock.column("ID Catégorie", width=100, anchor=CENTER)
tableau_stock.column("Nom Catégorie", width=150, anchor=CENTER)
# Header de chaque élément de la table
tableau_stock.heading("#0", text="")
tableau_stock.heading("ID", text="ID", anchor=CENTER)
tableau_stock.heading("Nom", text="Nom", anchor=CENTER)
tableau_stock.heading("Description", text="Description", anchor=CENTER)
tableau_stock.heading("Prix", text="Prix", anchor=CENTER)
tableau_stock.heading("Quantité", text="Quantité", anchor=CENTER)
tableau_stock.heading("ID Catégorie", text="ID Catégorie", anchor=CENTER)
tableau_stock.heading("Nom Catégorie", text="Nom Catégorie", anchor=CENTER)
tableau_stock.bind("<<TreeviewSelect>>", Selection)
# Bouton Supprimer
boutonSupprimer = Button(tableau, text="Supprimer", command=lambda: Supprimer())
boutonSupprimer.grid(column=3, row=4)
# Bouton Ajouter
boutonAjouter = Button(tableau, text="Ajouter", command=lambda: Ajouter())
boutonAjouter.grid(column=1, row=4)
# Bouton Modifier
boutonModifier = Button(tableau, text="Modifier", command=lambda: Modifier())
boutonModifier.grid(column=2, row=4)


# Permet d'actualiser la table en cas de modification
def ActualiseTable():
    stocks = tableau_stock.get_children()
    for stock in stocks:
        tableau_stock.delete(stock)


# Affiche la table
def AfficherTable():
    ActualiseTable()
    cursor.execute("select p.*, c.nom from produit p inner join categorie c on p.id_categorie = c.id;")
    stocks = cursor.fetchall()
    for stock in stocks:
        id = stock[0]
        tableau_stock.insert("", END, id, text=id, values=stock)


# Permet de supprimer un produit de la base de donnée
def Supprimer():
    id = tableau_stock.selection()[0]
    commande = "delete from produit where id=" + id
    cursor.execute(commande)
    admin.commit()
    tableau_stock.delete(id)


# Permet d'ajouter un produit a la base de donnée
def Ajouter():
    valeur = (Nom.get(), Description.get(), Prix.get(), Quantite.get(), ID_CATEGORIE.get())
    commande = "insert into produit (nom,description,prix,quantite,id_categorie) values (%s,%s,%s,%s,%s)"
    cursor.execute(commande, valeur)
    admin.commit()
    AfficherTable()


# Permet de modifier un produit de la base de donnée
def Modifier():
    id = tableau_stock.selection()[0]
    valeur = (Nom.get(), Description.get(), Prix.get(), Quantite.get(), ID_CATEGORIE.get())
    commande = "update produit set nom=%s,description=%s,prix=%s,quantite=%s,id_categorie=%s where id=" + id
    cursor.execute(commande, valeur)
    admin.commit()
    ActualiseTable()
    AfficherTable()


AfficherTable()
Stockage.mainloop()
