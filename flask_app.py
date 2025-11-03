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

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword'].strip().lower()

    if not keyword:
        return redirect(url_for('index'))

    # 검색어를 쉼표로 분리하고 공백 제거
    keywords = [k.strip() for k in keyword.split(',') if k.strip()]

    # 각 음식의 매칭 점수 계산
    scored_results = []
    for food in Kfood_data:
        score = 0
        food_name = food['name'].lower()
        food_ingredients = [ing.lower() for ing in food['ingredients']]
        
        for kw in keywords:
            # 이름에 포함되면 높은 점수
            if kw in food_name:
                score += 10
            # 재료에 포함되면 기본 점수
            elif any(kw in ingredient for ingredient in food_ingredients):
                score += 1
        
        if score > 0:
            scored_results.append((food, score))
    
    # 점수가 높은 순으로 정렬
    scored_results.sort(key=lambda x: x[1], reverse=True)
    Results = [food for food, score in scored_results]

    return render_template('results.html', results=Results, categories=Categories)

@app.route('/recipe/<name>')
def recipe(name):
    food = next((f for f in Kfood_data if f['name'] == name), None)
    return render_template('recipe.html', food=food, categories=Categories)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)