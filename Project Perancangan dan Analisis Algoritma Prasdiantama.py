import tkinter as tk  # Membuat alias untuk tkinter sebagai tk
import random  # Import modul random untuk membuat angka random
import math  # Import modul math untuk melakukan perhitungan matematika
from tkinter import messagebox  # Membuat peringatan berupa message box / kotak

# Konfigurasi peta
CELL_SIZE = 40  # Membuat ukuran size sel sebanyak 40
ROWS = 10  # Membuat baris sebanyak 10
COLS = 10  # Membuat colom sebanyak 10
WIDTH = CELL_SIZE * COLS  # Membuat lebar 
HEIGHT = CELL_SIZE * ROWS  # Membuat panjang 


class HideAndSeekGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hide And Seek Game")

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.red_droids = []
        self.green_droids = []

        self.green_droid_vision = False 
        self.red_droid_vision = False

        self.vision_droid = None  

        self.vision_range = 3
        self.is_game_over = False

        self.start_button = tk.Button(
            self, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        self.pause_button = tk.Button(
            self, text="Pause", command=self.pause_game, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT)
        self.shuffle_map_button = tk.Button(
            self, text="Shuffle Map", command=self.shuffle_map)
        self.shuffle_map_button.pack(side=tk.LEFT)
        self.shuffle_red_droid_button = tk.Button(
            self, text="Shuffle Red Droid", command=self.shuffle_red_droid)
        self.shuffle_red_droid_button.pack(side=tk.LEFT)
        self.shuffle_green_droid_button = tk.Button(
            self, text="Shuffle Green Droid", command=self.shuffle_green_droid)
        self.shuffle_green_droid_button.pack(side=tk.LEFT)
        self.add_red_droid_button = tk.Button(
            self, text="Add Red Droid", command=self.add_red_droid)
        self.add_red_droid_button.pack(side=tk.LEFT)
        self.view_red_droid_vision_button = tk.Button(
            self, text="View Red Droid Vision", command=self.view_red_droid_vision)
        self.view_red_droid_vision_button.pack(side=tk.LEFT)
        self.view_green_droid_vision_button = tk.Button(
            self, text="View Green Droid Vision", command=self.view_green_droid_vision)
        self.view_green_droid_vision_button.pack(side=tk.LEFT)

        self.vision_slider = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL, label="Vision Range",
                                      command=self.update_vision_range)
        self.vision_slider.set(self.vision_range)
        self.vision_slider.pack(side=tk.LEFT)

        self.bind("<Key>", self.key_pressed)
        self.bind("<Escape>", self.exit_game)

        self.generate_map()
        self.create_red_droid()
        self.create_green_droid()
        self.draw_map()

    def generate_map(self): # Generate peta
        self.map = [[1] * COLS for _ in range(ROWS)]

        def create_maze(row, col): # Membuat peta
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)

            for d_row, d_col in directions:
                n_row, n_col = row + d_row, col + d_col

                if 0 <= n_row < ROWS and 0 <= n_col < COLS and self.map[n_row][n_col] == 1:
                    self.map[n_row][n_col] = 0
                    self.map[row + d_row // 2][col + d_col // 2] = 0
                    create_maze(n_row, n_col)

        create_maze(0, 0)

    def draw_map_green(self): # Mengambar peta kembali untuk green droid vision
        self.canvas.delete("map")
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if self.map[row][col] == 0:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="black", tags="map")
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="black", tags="map")
                    
    def draw_map(self): # Mengambar peta kembali untuk red droid vision
        self.canvas.delete("map")
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if self.map[row][col] == 0:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="white", tags="map")
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="black", tags="map")

        if self.vision_droid == "green": # Menampilkan green droid vision
            for red_droid in self.red_droids:
                for green_droid in self.green_droids:
                    if self.get_distance(red_droid, green_droid) <= self.vision_range:
                        x1 = green_droid["x"] * CELL_SIZE
                        y1 = green_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightgreen", tags="map")
                    else:
                        x1 = green_droid["x"] * CELL_SIZE
                        y1 = green_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightgreen", tags="map")

            for green_droid in self.green_droids:
                for red_droid in self.red_droids:
                    if self.get_distance(green_droid, red_droid) <= self.vision_range:
                        x1 = red_droid["x"] * CELL_SIZE
                        y1 = red_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightcoral", tags="map")
                    else:
                        x1 = red_droid["x"] * CELL_SIZE
                        y1 = red_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightcoral", tags="map")
                        
        elif self.vision_droid == "red": # Menampilkan red droid vision
            for green_droid in self.green_droids:
                for red_droid in self.red_droids:
                    if self.get_distance(green_droid, red_droid) <= self.vision_range:
                        x1 = red_droid["x"] * CELL_SIZE
                        y1 = red_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightcoral", tags="map")
                    else:
                        x1 = red_droid["x"] * CELL_SIZE
                        y1 = red_droid["y"] * CELL_SIZE
                        x2 = x1 + CELL_SIZE
                        y2 = y1 + CELL_SIZE

                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="lightcoral", tags="map")

    def create_red_droid(self): # Membuat red droid
        row = random.randint(0, ROWS -1)
        col = random.randint(0, COLS -1)
        self.red_droids.append({"x": col, "y": row})

    def create_green_droid(self): # Membuat green droid
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        self.green_droids.append({"x": col, "y": row})

    def draw_droids(self): # Menggambar droid pada peta
        self.canvas.delete("droids")
        for red_droid in self.red_droids:
            x1 = red_droid["x"] * CELL_SIZE
            y1 = red_droid["y"] * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_oval(x1, y1, x2, y2, fill="red", tags="droids")
        for green_droid in self.green_droids:
            x1 = green_droid["x"] * CELL_SIZE
            y1 = green_droid["y"] * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_oval(
                x1, y1, x2, y2, fill="green", tags="droids")

    def update_vision_range(self, value): # Mengupdate vision range
        self.vision_range = int(value)

    def key_pressed(self, event): # Hotkey untuk permainan
        if not self.is_game_over:
            if event.keysym == "space":
                self.start_game()
            elif event.keysym == "p":
                self.pause_game()
            elif event.keysym == "s":
                self.shuffle_map()
            elif event.keysym == "r":
                self.shuffle_red_droid()
            elif event.keysym == "g":
                self.shuffle_green_droid()
            elif event.keysym == "a":
                self.add_red_droid()
            elif event.keysym == "1":
                self.view_red_droid_vision()
            elif event.keysym == "2":
                self.view_green_droid_vision()

    def start_game(self): # Memulai game
        self.is_game_over = False
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.shuffle_map_button.config(state=tk.DISABLED)
        self.shuffle_red_droid_button.config(state=tk.DISABLED)
        self.shuffle_green_droid_button.config(state=tk.DISABLED)
        self.add_red_droid_button.config(state=tk.DISABLED)
        self.view_red_droid_vision_button.config(state=tk.DISABLED)
        self.view_green_droid_vision_button.config(state=tk.DISABLED)
        self.move_droids()

    def pause_game(self): # Mempause game
        self.is_game_over = True
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.shuffle_map_button.config(state=tk.NORMAL)
        self.shuffle_red_droid_button.config(state=tk.NORMAL)
        self.shuffle_green_droid_button.config(state=tk.NORMAL)
        self.add_red_droid_button.config(state=tk.NORMAL)
        self.view_red_droid_vision_button.config(state=tk.NORMAL)
        self.view_green_droid_vision_button.config(state=tk.NORMAL)

    def shuffle_map(self): # Mengacak peta
        self.generate_map()
        self.draw_map()

    def shuffle_red_droid(self): # Mengacak letak red droid
        self.red_droids.clear()
        self.create_red_droid()
        self.draw_droids()

    def shuffle_green_droid(self): # Mengacak letak green droid
        self.green_droids.clear()
        self.create_green_droid()
        self.draw_droids()

    def add_red_droid(self): # Menambahkan red droid
        self.create_red_droid()
        self.draw_droids()

    def view_red_droid_vision(self): # Menampilkan red droid vision
        self.red_droid_vision = not self.red_droid_vision
        self.vision_droid = "red" if self.red_droid_vision else None
        self.draw_map()

    def view_green_droid_vision(self): # Menampilkan green droid vision
        self.green_droid_vision = not self.green_droid_vision
        self.red_droid_vision = not self.red_droid_vision
        self.vision_droid = "green" if self.red_droid_vision else None
        self.draw_map_green()

    def move_droids(self): # Mengatur pergerakan red droid dan green droid
        if not self.is_game_over:
            self.move_red_droids()
            self.move_green_droids()
            self.draw_droids()
            self.check_game_over()
            self.after(500, self.move_droids)

    def move_red_droids(self): # Pergerakan red droid
        for i in range(len(self.red_droids)):
            red_droid = self.red_droids[i]
            move_row = random.randint(-1, 1)
            move_col = random.randint(-1, 1)
            new_row = red_droid["y"] + move_row
            new_col = red_droid["x"] + move_col
            if self.is_valid_move(new_row, new_col):
                self.red_droids[i] = {"x": new_col, "y": new_row}

    def move_green_droids(self): # Pergerakan green droid
        for i in range(len(self.green_droids)):
            green_droid = self.green_droids[i]
            move_row = random.randint(-1, 1)
            move_col = random.randint(-1, 1)
            new_row = green_droid["y"] + move_row
            new_col = green_droid["x"] + move_col
            if self.is_valid_move(new_row, new_col):
                self.green_droids[i] = {"x": new_col, "y": new_row}

    def is_valid_move(self, row, col): # Pergerakan droid saat mengecek jika ada tembok atau tidak
        if row >= 0 and row < ROWS and col >= 0 and col < COLS and self.map[row][col] != 1:
            return True
        return False

    def check_game_over(self): # Pengecekan jika red droid telah menangkap green droid
        for red_droid in self.red_droids:
            if red_droid in self.green_droids:
                self.game_over(
                    "GAME OVER...Red droid collided with a green droid!")

    def game_over(self, message): # Permainan selesai
        self.is_game_over = True
        messagebox.showinfo("Game Over", message)

    def exit_game(self, event): # Keluar game
        self.destroy()

    def get_distance(self, droid1, droid2): # jarak antara red droid dan green droid
        x1 = droid1["x"]
        y1 = droid1["y"]
        x2 = droid2["x"]
        y2 = droid2["y"]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


if __name__ == "__main__":
    game = HideAndSeekGame()
    game.mainloop()
