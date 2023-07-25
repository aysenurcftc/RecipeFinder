
import tkinter as tk
from PIL import Image, ImageTk
import requests


url = 'https://api.edamam.com/search'
app_id = ""
app_key = ""

def get_recipe():

    target_recipe = search_text.get("1.0","end")

    # API isteği gönderme
    params = {
        'q': target_recipe,
        'app_id': app_id,
        'app_key': app_key,
    }

    response = requests.get(url, params=params)


    if response.status_code == 200:
        data = response.json()
        hits = data['hits']

        if hits:
            for i, hit in enumerate(hits[:3]):
                recipe = hit['recipe']

                # Tarif adı ve malzemeleri
                recipe_name = recipe['label']
                recipe_ingredients = recipe['ingredientLines']


                if len(recipe_labels) <= i:
                    label = tk.Label(recipe_frame, background="white", foreground="green", font=("Helvetica", 12, "bold"))
                    recipe_labels.append(label)
                    label.pack(fill="x", padx=20, pady=(5, 0), side="top")

                # Tarif adı ve malzemelerini etikete ekle
                recipe_labels[i].config(
                    text=f"\n Recipe Name: {recipe_name}\nIngredients:\n" + "\n".join(recipe_ingredients))


            if len(hits) < len(recipe_labels):
                for j in range(len(hits), len(recipe_labels)):
                    recipe_labels[j].config(text="")

        else:
            for label in recipe_labels:
                label.config(text="No recipe found.")

    else:
        for label in recipe_labels:
            label.config(text="Failed to fetch recipes.")





window = tk.Tk()
window.title("Recipes")
window.geometry("450x600")

#set window color
window.configure(bg="white")



title_label = tk.Label(window, text="Search recipes",background="white", foreground="green", font=("Helvetica", 30, "bold"))
title_label.pack(pady=30)

image1 = Image.open("assets/veggie.jpg")
resize_image = image1.resize((150, 150))
test = ImageTk.PhotoImage(resize_image)

label1 = tk.Label(image=test)
label1.image = test
label1.pack()

search_text = tk.Text(window, height=2, width=40,background="white smoke")
search_text.pack(pady=[10, 10], padx=[20, 20])

search_button = tk.Button(window, text ="Search",command=get_recipe,background="green",foreground="white",font=("Helvetica", 12, "bold"))
search_button.pack()


# Create a frame to hold the recipe labels and make it scrollable
frame = tk.Frame(window, background="white")
frame.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(frame, background="white", highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

recipe_frame = tk.Frame(canvas, background="white")
canvas.create_window((0, 0), window=recipe_frame, anchor="nw")


recipe_labels = [tk.Label(recipe_frame, background="white", foreground="green", font=("Helvetica", 11, "bold")) for _ in range(3)]
for i, label in enumerate(recipe_labels):
    label.grid(row=i, column=0, padx=20, pady=(5, 0), sticky="w")  #


recipe_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

window.mainloop()