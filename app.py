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
    print("Table Created Successfully")


sql_lite_db()
app = Flask(__name__)
CORS(app)

@app.route('/')

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


if __name__ == '__main__':
    app.run(debug=True)