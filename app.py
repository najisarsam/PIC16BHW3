from flask import Flask, render_template, request, g
import sqlite3



# giving the app the name of the file
app = Flask(__name__)



# function to access database
def get_message_db():
    # if the connection to the database already exists, we return it
    try:
        return g.message_db

    # otherwise, we create the database for the first time
    except:
        # creates database connection
        g.message_db = sqlite3.connect("messages_db.sqlite")
        
        # creates table in database for storing messages
        cmd = '''
        CREATE TABLE IF NOT EXISTS messages
        (num INT,message TEXT,alias TEXT)
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db



# function to add a message to the database
def insert_message(request):
    # open a connection to message database 
    conn = get_message_db()
    cursor = conn.cursor()
    
    # obtain data for new message
        # id for the message is one plus its row number
    cursor.execute("SELECT COUNT(*) FROM messages")
    num = cursor.fetchone()[0] + 1
        # obtaining submitted message
    message = request.form['message']
        # obtaining submitted alias
    alias = request.form['alias']

    # store the new message
    cmd = f'''
    INSERT INTO messages (num,message,alias)
    VALUES ({num},'{message}','{alias}')
    '''
    cursor.execute(cmd)
    conn.commit()
    
    # close the connection
    conn.close()



# accessing submissions page
@app.route('/', methods=['POST','GET'])
def render_main():
    # if they submit a message 
    if request.method == 'POST':
        # store the message in the database
        insert_message(request)
        # display the thank you message
        return render_template('submit.html', submitted=True)
    # otherwise display the standard page
    else:
        return render_template('submit.html', submitted=False)
        


# function for randomly choosing n-many messages
def random_messages(n):
    # open a connection to message database 
    conn = get_message_db()
    cursor = conn.cursor()
    
    # obtain list of n radomly chosen messages
    cmd = f'''
    SELECT * FROM messages ORDER BY
    RANDOM() LIMIT {n}
    '''
    cursor.execute(cmd)
    randomlist = cursor.fetchall()

    # close the connection
    conn.close()

    return randomlist


# accessing viewing page
@app.route("/view/")
def render_view():
    return render_template("view.html", randomlist = random_messages(3))