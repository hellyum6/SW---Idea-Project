from flask import Flask, render_template, request
from urllib.parse import unquote
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data/kfood.json'), encoding='utf-8') as f:
    kfood_data = json.load(f)
with open(os.path.join(BASE_DIR, 'data/categories.json'), encoding='utf-8') as f:
    categories = json.load(f)

@app.route('/')
def index():
    print(categories)
    return render_template('index.html', categories=categories)

@app.route('/category/<path:name>')
def category(name):
    decoded_name = unquote(name)
    print(f"요청된 카테고리: {decoded_name}")
    foods = [food for food in kfood_data if food['category'] == decoded_name]
    return render_template('category.html', category=decoded_name, foods=foods, categories=categories)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword'].strip().lower()
    results = [
        food for food in kfood_data
        if keyword in food['name'].lower()
        or any(keyword in ingredient.lower() for ingredient in food['ingredients'])
    ]
    return render_template('results.html', results=results, categories=categories)

@app.route('/recipe/<name>')
def recipe(name):
    food = next((f for f in kfood_data if f['name'] == name), None)
    return render_template('recipe.html', food=food)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
