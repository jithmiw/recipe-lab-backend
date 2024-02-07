from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommend import generation_function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recipes")
async def get_recipes(ingredients: str):
    generated = generation_function(ingredients)
    formatted_recipes = []
    for text in generated:
        sections = text.split("\n")
        recipe = {
            "title": None,
            "ingredients": [],
            "directions": [],
        }
        for section in sections:
            section = section.strip()
            if section.startswith("title:"):
                recipe["title"] = section.replace("title:", "").strip().capitalize()
            elif section.startswith("ingredients:"):
                recipe["ingredients"] = [
                    item.strip().capitalize() for item in section.replace("ingredients:", "").split("--")
                ]
            elif section.startswith("directions:"):
                recipe["directions"] = [
                    item.strip() for item in section.replace("directions:", "").split("--")
                ]
        formatted_recipes.append(recipe)
    print(formatted_recipes)
    return formatted_recipes
