from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data import trello_items as trello


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = trello.get_trello_cards()
    return render_template('index.html', items = items)

@app.route('/items/new', methods=["POST"])
def add_item():
  if request.method == "POST":
    title = request.form['title']
    trello.add_item_trello(title)
    return redirect(url_for('index'))
  

@app.route('/items/<id>/complete')
def complete_item(id):
    trello.complete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
