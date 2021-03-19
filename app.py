import sqlite3
from flask import Flask, request, jsonify
from flask_cors import  CORS


def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def sql_lite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Reg_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, lname TEXT, email TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS Comment_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, email TEXT, comment TEXT)')
    print("Table Created Successfully")


sql_lite_db()
app = Flask(__name__)
CORS(app)

@app.route('/')
def landing():
    return("<p> To view records add /show-acc/ to url </p><p> Nettlify link: https://happy-clarke-59c23c.netlify.app/</p>" )

@app.route('/add-reg/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            lname = post_data['lname']
            email = post_data['email']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Reg_Table (fname, lname, email) VALUES (?, ?, ?)", (fname, lname, email))
                con.commit()
                msg = fname + "Account Successfully Created"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-acc/', methods=["GET"])
def show_accounts():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Reg_Table")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)


@app.route('/add-com/', methods=['POST'])
def add_comment():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            email = post_data['email']
            comment = post_data['comment']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Comment_Table (fname, email, comment) VALUES (?, ?, ?)", (fname, email, comment))
                con.commit()
                msg = fname + "Account has successfully been created"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-com/', methods=["GET"])
def show_comments():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Comment_Table")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)

@app.route('/delete-account/<int:customer_id>/', methods=["DELETE"])
def delete_account(customer_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:

            cur = con.cursor()
            cur.execute("DELETE FROM Comment_Table WHERE  id = " + str(customer_id))

            con.commit()
            msg = "A account was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True)