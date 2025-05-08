
from tkinter import *
import random
from tkinter import ttk
from PIL import Image, ImageTk
import os

PuzzleWindow = Tk()
PuzzleWindow.title('Memory Puzzle Game')

try:
    bg_image = Image.open("фон.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(PuzzleWindow, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("Фоновое изображение не найдено!")

current_category = StringVar()
current_category.set("Cats")
current_difficulty = StringVar()
current_difficulty.set("Easy")
CARD_BACK_IMAGE_PATH = "задник.jpg"
card_back_image = None
game_over = False
moves1 = 0 
CARD_SIZE = 100  
CARD_SPACING = 5 


def load_image(image_path, width, height):
    try:
        img = Image.open(image_path)
        img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"Изображение не найдено: {image_path}")
        return None


image_cache = {}

def draw(image_name, l, m):
    global base1, image_cache, current_category, card_count, board1, card_back_image, CARD_SIZE, CARD_SPACING
    if card_back_image is None:
        print("Загрузка картинки для задника.")
        return  

    if board1[l][m] == '.':  
        base1.create_image(CARD_SIZE * l + CARD_SIZE // 2 + CARD_SPACING * l, CARD_SIZE * m + CARD_SIZE // 2 + CARD_SPACING * m, image=card_back_image)  
    else:
        category = current_category.get()
        category_path = os.path.join("images", category)
        image_path = os.path.join(category_path, image_name)

        if image_path not in image_cache:
            image = load_image(image_path, CARD_SIZE, CARD_SIZE)
            if image:
                image_cache[image_path] = image
            else:
                return

        image = image_cache[image_path]
        base1.create_image(CARD_SIZE * l + CARD_SIZE // 2 + CARD_SPACING * l, CARD_SIZE * m + CARD_SIZE // 2 + CARD_SPACING * m, image=image)  

def quizboard():
    global base1, ans1, board1, card_count, game_over, moves1, moves_label

    count = 0
    for i in range(card_count):
        for j in range(card_count):
            if card_back_image:
                draw(ans1[i][j], i, j)
            if board1[i][j] != '.':
                count += 1  
    if count == card_count ** 2:
        game_over = True  
        moves_label.config(text=f"The game is over! Moves: {moves1}")
    else:
        moves_label.config(text=f"Moves: {moves1}") 

def call(event):
    global base1, ans1, board1, moves1, prev1, card_count, game_over, CARD_SIZE, CARD_SPACING

    if game_over:  
        return

    i = event.x // (CARD_SIZE + CARD_SPACING)
    j = event.y // (CARD_SIZE + CARD_SPACING)

    if i >= card_count or j >= card_count:  
        return
    if board1[i][j] != '.':
        return
    moves1 += 1
    quizboard() 
    if prev1[0] > card_count:
        prev1[0] = i
        prev1[1] = j
        board1[i][j] = ans1[i][j]
        quizboard()
    else:
        board1[i][j] = ans1[i][j]
        quizboard()
        if ans1[i][j] == ans1[prev1[0]][prev1[1]]:
            prev1 = [card_count + 1, card_count + 1]  
            quizboard()
            return
        else:
            board1[prev1[0]][prev1[1]] = '.'
            quizboard()
            prev1 = [i, j]
            return

def choose_category(category):
    global ans1, board1, image_cache, card_count, game_over, moves1
    current_category.set(category)
    image_cache = {}
    category_path = os.path.join("images", category)
    try:
        image_files = [f for f in os.listdir(category_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        needed_images = (card_count**2) // 2
        if len(image_files) < needed_images:
            print(f"Недостаточно изображений в категории {category}.  Нужно минимум {needed_images}.")
            return
        selected_images = random.sample(image_files, needed_images)  
        ans1 = selected_images * 2
        random.shuffle(ans1)
        ans1 = [ans1[i*card_count:(i+1)*card_count] for i in range(card_count)]
        board1 = [list('.' * card_count) for count in range(card_count)]
        game_over = False 
        moves1 = 0 
        quizboard()
        print(f"Выбрана категория: {category}")

    except FileNotFoundError:
        print(f"Папка категории не найдена: {category_path}")
    except Exception as e:
        print(f"Ошибка при выборе категории: {e}")

def set_difficulty(difficulty):
    global CARD_SIZE, CANVAS_WIDTH, CANVAS_HEIGHT, base1, ans1, board1, prev1, image_cache, card_count, card_back_image, game_over, CARD_SPACING, moves1

    current_difficulty.set(difficulty)
    image_cache = {}

    if difficulty == "Easy":
        card_count = 4
        CARD_SIZE = 140
    elif difficulty == "Medium":
        card_count = 6
        CARD_SIZE = 111
    elif difficulty == "Hard":
        card_count = 8
        CARD_SIZE = 82
    else:
        card_count = 4
        CARD_SIZE = 140

    CANVAS_WIDTH = ((CARD_SIZE + CARD_SPACING) * card_count) - CARD_SPACING  
    CANVAS_HEIGHT = ((CARD_SIZE + CARD_SPACING) * card_count) - CARD_SPACING

    try:
        base1.destroy()
    except:
        pass

    base1 = Canvas(PuzzleWindow, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0, background = "#BBDEFB") 
    base1.pack()
    base1.bind("<Button-1>", call)

    try:
        card_back_image_temp = Image.open(CARD_BACK_IMAGE_PATH)
        card_back_image = ImageTk.PhotoImage(card_back_image_temp.resize((CARD_SIZE, CARD_SIZE), Image.LANCZOS))
    except FileNotFoundError:
        print(f"Изображение для задней стороны карточки не найдено: {CARD_BACK_IMAGE_PATH}")
        card_back_image = None

    ans1 = []
    board1 = []
    moves1 = 0 
    prev1 = [card_count + 1, card_count + 1]  
    game_over = False

    choose_category(current_category.get())  
    print(f"Установлен уровень сложности: {difficulty}")

categories_frame = Frame(PuzzleWindow, bg="#e0e0e0", padx=4, pady=4, borderwidth=2, relief=SOLID) 
categories_frame.pack(pady=3)  

categories = ["Cats", "Dogs", "Cars", "Flowers", "Fruits", "Mountains",
              "Rivers", "Birds", "Fish", "Trees", "Cities", "Planets"]

for i, category in enumerate(categories):
    button = Button(categories_frame, text=category, command=lambda c=category: choose_category(c), width=8,
                    height=1, font=('Arial', 10), bg="#4CAF50", fg="white", bd=0, relief=FLAT)  
    button.pack(side=LEFT, padx=3)  

difficulty_frame = Frame(PuzzleWindow, bg="#e0e0e0", padx=2, pady=2, borderwidth=2, relief=SOLID)
difficulty_frame.pack(pady=3)

difficulties = ["Easy", "Medium", "Hard"]

for i, difficulty in enumerate(difficulties):
    button = Button(difficulty_frame, text=difficulty, command=lambda d=difficulty: set_difficulty(d), width=8,
                    height=1, font=('Arial', 10),  bg="#2196F3", fg="white", bd=0, relief=FLAT) 
    button.grid(row=0, column=i, padx=2, pady=2)

moves_label = Label(PuzzleWindow, text="Ходы: 0", font=('Arial', 14), bg="#e0e0e0")
moves_label.pack()

try:
    card_back_image_temp = Image.open(CARD_BACK_IMAGE_PATH)
    card_back_image = ImageTk.PhotoImage(card_back_image_temp.resize((CARD_SIZE, CARD_SIZE), Image.LANCZOS))
except FileNotFoundError:
    print(f"Изображение для задней стороны карточки не найдено: {CARD_BACK_IMAGE_PATH}")
    card_back_image = None

card_count = 4  
set_difficulty(current_difficulty.get())
choose_category(current_category.get())

PuzzleWindow.configure(bg="#e0e0e0") 
PuzzleWindow.mainloop()
