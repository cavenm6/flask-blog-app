import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'Secret Key'


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#Function to retrieve a post from the db
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM post WHERE id = ?', (post_id,)).fetchone()
    conn.close

    if post is None:
        abort(404)
    return post 

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #Get a connection to the database
    conn = get_db_connection()

    #Execute a query to read all posts
    posts = conn.execute('SELECT * from posts').fetchall()

    #Close connection
    conn.close()

    #send the post to index.html template to be displayed
    return render_template('index.html', posts = posts)

    return "<h1>Welcome to Menezes's Blog</h1>"


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #Determine if the page is being requested with a POST or GET request
    if request.method == 'POST':
        #get the title and content submitted
        title = request.form['title']
        content = request.form['content']

        #display an error message if title or content not submitted
        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            #Insert data to db
            conn.execute('INSERT INTO posts (title, content) VALUES (? , ?)', (title, content))
            conn.commit
            conn.close()
            return redirect(url_for('index'))

        #make a db conenction and insert the blog post content

    return render_template('create.html')

#Create a route to edit a post. Load post with either get or post
#pass the post as url parameter
@app.route('/<int:id>/edit/', methods=('GET', 'POST' ))
def edit(id):
    #get the post from the database with a select query for that post with id
    post = get_post(id)
    
    #Determine if post was selected with GET or POST
    #If POST, process the form data, get the data and validate it, and redirect for homepage
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            #Insert data to db
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE ID = ?', (title, content, id))
            conn.commit
            conn.close()
            return redirect(url_for('index'))        
    #If GET, then display page
    return render_template('edit.html', post=post)




app.run()