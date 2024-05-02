import pygame
import heapq
import random

# Inisialisasi Pygame
pygame.init()

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ukuran grid dan ukuran tile
GRID_SIZE = 15
TILE_SIZE = 30

# Inisialisasi layar
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dijkstra Pathfinding Animation")

# Fungsi untuk menggambar grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(SCREEN, BLACK, (x,0), (x,SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(SCREEN, BLACK, (0,y), (SCREEN_WIDTH,y))

# Fungsi untuk menggambar kotak pada posisi (x, y) dengan warna color
def draw_tile(x, y, color):
    pygame.draw.rect(SCREEN, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Fungsi untuk mendapatkan tetangga dari sebuah titik
def get_neighbors(node):
    x, y = node
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < GRID_SIZE - 1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < GRID_SIZE - 1:
        neighbors.append((x, y+1))
    return neighbors

# Algoritma Dijkstra
def dijkstra(start, end, obstacles):
    visited = set()
    queue = [(0, start)]
    distances = {start: 0}
    came_from = {}  # Untuk melacak jalur yang ditemukan
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            path = []
            while current_node != start:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            return distances[end], path
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor in get_neighbors(current_node):
            if neighbor not in obstacles:
                new_distance = current_distance + 1 # asumsi jarak antar tile adalah 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    heapq.heappush(queue, (new_distance, neighbor))
                    came_from[neighbor] = current_node
    return float('inf'), None

# Fungsi untuk membuat rintangan secara acak
def generate_obstacles():
    obstacles = []
    for _ in range(int(GRID_SIZE * GRID_SIZE * 0.2)):  # 20% dari total tile sebagai rintangan
        obstacle = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if obstacle not in obstacles:
            obstacles.append(obstacle)
    return obstacles

# Fungsi utama
def main():
    start = (0, 0)
    end = (GRID_SIZE - 1, GRID_SIZE - 1)
    obstacles = generate_obstacles()

    # Loop utama
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(WHITE)  # Bersihkan layar
        draw_grid()         # Gambar grid

        # Gambar rintangan
        for obstacle in obstacles:
            draw_tile(obstacle[0], obstacle[1], BLACK)

        draw_tile(start[0], start[1], GREEN)   # Gambar titik awal
        draw_tile(end[0], end[1], RED)         # Gambar titik akhir

        pygame.display.update()

        # Hitung jarak terdekat dan tampilkan animasi pergerakan
        distance, path = dijkstra(start, end, obstacles)
        if path:
            for i, node in enumerate(path):
                draw_tile(node[0], node[1], BLUE) # Tampilkan jalur yang ditemukan
                pygame.display.update()
                pygame.time.delay(200)  # Delay untuk efek animasi
            print("Langkah yang digunakan untuk mencapai tujuan:", len(path))

    pygame.quit()

if __name__ == "__main__":
    main()
