from flask import *   ##importing all classes(Flask, render_
                     ##template) from flask
import sqlite3

## creation of object
app = Flask(__name__)   #main

@app.route("/")
def index():
    return render_template("index.html");

## if we give /add open the add.html file
@app.route("/add")
def add():   
    return render_template("add.html")

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("addressDB.db") as con:
                cur = con.cursor()   
                cur.execute("INSERT into Address (name, email, address) values (?,?,?)",(name,email,address))
                con.commit()
                msg = "Contact successfully Added"   
        except:
            con.rollback()
            msg = "We can not add Contact to the list"
        finally:
            return render_template("success.html",msg = msg)
            con.close()

@app.route("/view")
def view():
    con = sqlite3.connect("addressDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Address")   
    rows = cur.fetchall()
    return render_template("view.html",rows = rows)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])   
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("addressDB.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Address where id = ?",id)
            msg = "Contact successfully deleted"   
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html",msg = msg)

if __name__ == "__main__":
    app.run(debug = True)  #127.0.0.1:5000/ python decorator