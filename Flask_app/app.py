from flask import Flask, render_template
import json
from random import randint

recipes = {
    'Spaghetti Carbonara': {
        'Ingredients:': ['200g spaghetti', '100g pancetta', '2 eggs', '50g Parmesan cheese', 'Salt & Pepper'],
        'Instructions:': ['Cook spaghetti, fry pancetta, mix eggs with cheese, combine all.',
                          'In a pan, fry the pancetta until crispy.',
                          'In a bowl, whisk the eggs with grated Parmesan cheese.',
                          'Combine the hot pasta with the pancetta, then mix in the egg mixture off the heat.',
                          'Stir quickly to create a creamy sauce. Add salt and pepper to taste.',
                          'Serve immediately with extra Parmesan.']
    },
    'Classic Pancakes': {
        'Ingredients:': ['1 cup flour', '100g pancetta', '1 cup milk', '1 egg', '1 tbsp sugar', '1 tsp baking powder'],
        'Instructions:': ['In a bowl, mix the flour, sugar, baking powder, and salt.',
                          'Add the milk and egg, then whisk until smooth.',
                          'Heat a pan over medium heat and melt a little butter.',
                          'Pour in small amounts of batter and cook until bubbles form on the surface.',
                          'Flip the pancake and cook until golden brown on both sides.',
                          'Serve warm with syrup, fruits, or butter.']
    },
    'Easy Chicken Stir-Fry': {
        'Ingredients:': ['2 chicken breasts, thinly sliced', '1 tablespoon olive oil (or any oil you prefer)', '1 bell pepper, sliced', '1 medium onion, sliced', '1 zucchini, sliced', '1 cup broccoli florets',
                         '2 tablespoons soy sauce', '1 tablespoon honey or brown sugar', '1 tablespoon rice vinegar (optional)', '2 cloves garlic, minced', '1 teaspoon grated ginger (optional)', 'Cooked rice (for serving)'],
        'Instructions:': ['Prepare the Sauce: In a small bowl, mix together soy sauce, honey (or brown sugar), rice vinegar, garlic, and ginger. Set aside.',
                          'Cook the Chicken: Heat the olive oil in a large pan or wok over medium-high heat. Add the sliced chicken and cook until browned and cooked through (about 5-7 minutes). Remove from the pan and set aside.',
                          'Sauté the Veggies: In the same pan, add a little more oil if necessary. Add the onion, bell pepper, zucchini, and broccoli. Stir-fry for about 5 minutes, or until the vegetables are tender but still crisp.',
                          'Combine: Add the chicken back into the pan with the vegetables. Pour the sauce over everything and toss to coat evenly. Cook for another 2-3 minutes until everything is heated through.',
                          'Flip the pancake and cook until golden brown on both sides.',
                          'Serve: Serve the stir-fry over cooked rice and enjoy!']
    }
    }
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello, world!</h1>"

@app.route("/about")
def about():
    return json.dumps({'user': 'user'})

@app.route("/random/<a>/<b>")
def rand_user_int(a, b):
    return f'<h1>Случайное число: {randint(int(a), int(b))}</h1>'

@app.route("/recipe/<id>")
def recipe(id):
    rec = recipes[id]

    if rec:
        body = f'''<h1>Delicious Recipes</h1>
        <h2>{id}</h2>
        <p><strong>Ingredients:</strong></p>
        <ul>'''
        ingredients = rec.get('Ingredients:')

        print(f'Ingredients: {ingredients}')

        for el in ingredients:
            body += f'<li>{el}</li>'

        body += '</ul>'
        body += '<p><strong>Instructions:</strong></p>'
        instructions = rec.get('Instructions:')

        print(f'Instructions: {instructions}')

        body += '<ol>'

        for el in instructions:
            body += f'<li>{el}</li>'

        body += '</ol>'

        return body

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

app.run(host='localhost', port=5000, debug=True)
