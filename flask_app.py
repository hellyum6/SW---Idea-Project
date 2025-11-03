from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import unquote
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data/kfood.json'), encoding='utf-8') as Kfood:
    Kfood_data = json.load(Kfood)
with open(os.path.join(BASE_DIR, 'data/categories.json'), encoding='utf-8') as Category:
    Categories = json.load(Category)

@app.route('/')
def index():
    return render_template('index.html', categories = Categories)

@app.route('/category/<path:name>')
def category(name):
    decoded_name = unquote(name)
    Foods = [food for food in Kfood_data if food['category'] == decoded_name]
    return render_template('category.html', category = decoded_name, foods = Foods, categories = Categories)

@app.route('/search', methods = ['POST'])
def search():
    Keyword = request.form['keyword'].strip().lower()

    if not Keyword:
        return redirect(url_for('index'))

    Results = [
        food for food in Kfood_data
        if Keyword in food['name'].lower()
        or any(Keyword in ingredient.lower() for ingredient in food['ingredients'])
    ]
    return render_template('results.html', results=Results, categories=Categories)

@app.route('/recipe/<name>')
def recipe(name):
    food = next((f for f in Kfood_data if f['name'] == name), None)
    return render_template('recipe.html', food=food, categories=Categories)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)