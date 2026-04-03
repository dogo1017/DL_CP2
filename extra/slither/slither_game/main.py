import os
import sys
import asyncio
import subprocess
import site
import importlib
import json
import math

def install_and_import(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"'{import_name}' is already installed.")
    except ImportError:
        print(f"'{import_name}' not found. Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package_name])
        
        # Refresh paths so the current script can see the new module
        importlib.invalidate_caches()
        site.addsitedir(site.getusersitepackages()) 
        print(f"Successfully installed {package_name}.")

# Run the installer
install_and_import("websockets")
install_and_import("pygbag")
install_and_import("pygame")

sys.path.insert(0, site.getusersitepackages())

import websockets
import pygame



async def main():
    pygame.init()
    await asyncio.sleep(0)

    # Use fixed size for WASM - display.Info() is unreliable before canvas is ready
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    PLAYER_BASE_SPEED = 200
    BOOST_SPEED_MULTIPLIER = 1.6
    BOOST_COST_RATE = 100
    INITIAL_PLAYER_RADIUS = 10
    INITIAL_LENGTH = 150
    GROWTH_SLOWDOWN_FACTOR = 0.5
    BG_COLOR = (20, 20, 20)
    MAP_SIZE = 3000

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Slither.io Multiplayer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    await asyncio.sleep(0)


    class NetworkManager:
        # Sets up the network manager with empty state before a connection is made
        def __init__(self):
            self.websocket = None
            self.player_id = None
            self.connected = False
            self.game_state = {'players': [], 'foods': [], 'timestamp': 0}
            self.last_state_time = -9999  # large negative so "Connected" only shows after first real state
            self.outgoing = []

        # Opens the websocket connection, sends join, waits for init, then starts the receive task
        async def connect(self, server_url, player_name, player_color):
            self.websocket = await websockets.connect(
                server_url,
                max_size=10**7,
                ping_interval=20,
                ping_timeout=10
            )
            join_msg = {'type': 'join', 'name': player_name, 'color': player_color}
            await self.websocket.send(json.dumps(join_msg))

            init_msg = await self.websocket.recv()
            init_data = json.loads(init_msg)
            if init_data['type'] == 'init':
                self.player_id = init_data['player_id']
                self.connected = True

            asyncio.ensure_future(self._receive_loop())

        # Continuously reads incoming messages from the server and updates game state
        async def _receive_loop(self):
            try:
                async for message in self.websocket:
                    data = json.loads(message)
                    if data['type'] == 'state':
                        self.game_state = data
                        self.last_state_time = pygame.time.get_ticks()
            except Exception:
                self.connected = False

        # Sends all queued outgoing messages to the server in one flush per frame
        async def flush(self):
            if not self.websocket or not self.connected:
                return
            for msg in self.outgoing:
                try:
                    await self.websocket.send(json.dumps(msg))
                except Exception:
                    self.connected = False
                    break
            self.outgoing.clear()

        # Queues a player state update to be sent on the next flush
        def send_update(self, player_data):
            self.outgoing.append({
                'type': 'update',
                'x': player_data['x'],
                'y': player_data['y'],
                'positions': player_data['positions'],
                'radius': player_data['radius'],
                'length': player_data['length'],
                'score': player_data['score'],
                'alive': player_data['alive'],
                'shed_food': player_data.get('shed_food')
            })

        # Queues a food eaten notification to be sent on the next flush
        def send_eat(self, food_id):
            self.outgoing.append({'type': 'eat', 'food_id': food_id})

        # Queues a respawn request with the player's new chosen color
        def send_respawn(self, color):
            self.outgoing.append({'type': 'respawn', 'color': color})


    class Player:
        # Creates a new player at the given position with default stats
        def __init__(self, x, y, color, is_local=False):
            self.pos = pygame.math.Vector2(x, y)
            self.radius = INITIAL_PLAYER_RADIUS
            self.score = 0
            self.color = color
            self.length = INITIAL_LENGTH
            self.base_speed = PLAYER_BASE_SPEED
            self.speed = self.base_speed
            self.positions = [pygame.math.Vector2(x, y) for _ in range(int(self.length))]
            self.boosting = False
            self.is_local = is_local
            self.name = ""
            self.alive = True

        # Moves the player toward the mouse, handles boost, and updates body positions
        # Returns a shed food item dict if boosting, otherwise None
        def update(self, dt):
            if not self.is_local or not self.alive:
                return None

            speed_multiplier = BOOST_SPEED_MULTIPLIER if self.boosting else 1.0
            size_multiplier = max(0.3, (INITIAL_PLAYER_RADIUS / self.radius) ** 0.8)
            self.speed = self.base_speed * size_multiplier * speed_multiplier

            mouse_x, mouse_y = pygame.mouse.get_pos()
            target = pygame.math.Vector2(mouse_x - SCREEN_WIDTH // 2, mouse_y - SCREEN_HEIGHT // 2)

            if target.length_squared() > 0:
                direction = target.normalize()
                self.pos += direction * self.speed * dt

            self.pos.x = max(self.radius, min(MAP_SIZE - self.radius, self.pos.x))
            self.pos.y = max(self.radius, min(MAP_SIZE - self.radius, self.pos.y))

            shed_food_item = None
            if self.boosting and self.length > 50:
                mass_lost = BOOST_COST_RATE * dt
                self.length -= mass_lost
                self.score = max(0, self.score - mass_lost * 0.1)
                if len(self.positions) > 10:
                    shed_pos = self.positions[-10]
                    shed_food_item = {'x': shed_pos.x, 'y': shed_pos.y}

            self.positions.insert(0, self.pos.copy())
            target_length = int(self.length)
            if len(self.positions) > target_length:
                self.positions = self.positions[:target_length]
            elif len(self.positions) < target_length:
                while len(self.positions) < target_length:
                    self.positions.append(self.positions[-1].copy())

            self.update_radius()
            return shed_food_item

        # Recalculates radius based on current length
        def update_radius(self):
            self.radius = INITIAL_PLAYER_RADIUS + math.sqrt(self.length / 10.0)

        # Increases the player's length and score by the given mass, capped at MAX_LENGTH
        def grow(self, mass_gained):
            effective_gain = mass_gained * GROWTH_SLOWDOWN_FACTOR
            self.length = min(self.length + effective_gain)
            self.score += effective_gain
            self.update_radius()

        # Draws all body segments with tapering radius, and the player's name above their head
        def draw(self, surface, camera_x, camera_y):
            offset_x = -camera_x + SCREEN_WIDTH // 2
            offset_y = -camera_y + SCREEN_HEIGHT // 2

            for i, pos in enumerate(self.positions):
                taper_factor = 1 - (i / len(self.positions)) * 0.7
                segment_radius = max(1, self.radius * taper_factor)
                screen_x = pos.x + offset_x
                screen_y = pos.y + offset_y
                if -segment_radius < screen_x < SCREEN_WIDTH + segment_radius and \
                   -segment_radius < screen_y < SCREEN_HEIGHT + segment_radius:
                    pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), int(segment_radius))

            if self.name and self.alive:
                name_surface = small_font.render(self.name, True, (255, 255, 255))
                name_x = self.pos.x + offset_x - name_surface.get_width() // 2
                name_y = self.pos.y + offset_y - self.radius - 20
                surface.blit(name_surface, (name_x, name_y))


    class Food:
        # Builds a food object from a server-provided dictionary
        def __init__(self, food_data):
            self.pos = pygame.math.Vector2(food_data['x'], food_data['y'])
            self.radius = food_data['radius']
            self.value = food_data['value']
            self.color = tuple(food_data['color'])
            self.id = food_data['id']

        # Draws the food dot if it is within the visible screen area
        def draw(self, surface, camera_x, camera_y):
            screen_x = self.pos.x - camera_x + SCREEN_WIDTH // 2
            screen_y = self.pos.y - camera_y + SCREEN_HEIGHT // 2
            if -self.radius < screen_x < SCREEN_WIDTH + self.radius and \
               -self.radius < screen_y < SCREEN_HEIGHT + self.radius:
                pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), self.radius)


    # Shows a grid of color swatches and returns the chosen color as a list, or None if cancelled
    async def show_color_picker():
        colors = [
            (255, 0, 0),   (0, 255, 0),   (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (255, 128, 0), (128, 0, 255), (0, 255, 128),
            (255, 192, 203), (128, 128, 128), (255, 255, 255)
        ]

        selected_color = colors[1]
        color_boxes = []
        start_x = SCREEN_WIDTH // 2 - 300
        start_y = SCREEN_HEIGHT // 2 - 50

        for i, color in enumerate(colors):
            x = start_x + (i % 6) * 100
            y = start_y + (i // 6) * 100
            color_boxes.append((pygame.Rect(x, y, 80, 80), color))

        while True:
            screen.fill(BG_COLOR)
            title = font.render('Choose Your Color', True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, start_y - 100))

            for box, color in color_boxes:
                pygame.draw.rect(screen, color, box)
                border_color = (255, 255, 255) if color == selected_color else (100, 100, 100)
                border_width = 5 if color == selected_color else 2
                pygame.draw.rect(screen, border_color, box, border_width)

            inst = small_font.render('Click a color, then press ENTER to continue', True, (200, 200, 200))
            screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, start_y + 230))
            pygame.display.flip()
            await asyncio.sleep(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for box, color in color_boxes:
                        if box.collidepoint(pygame.mouse.get_pos()):
                            selected_color = color
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return list(selected_color)
                    if event.key == pygame.K_ESCAPE:
                        return None


    # Shows the server address and name input screen and returns both strings, or (None, None) if cancelled
    async def show_connection_screen():
        # Set your permanent server address here
        PERMANENT_SERVER = "ws://localhost:8765" 
        
        # Position the name box in the center
        name_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 20, 600, 40)
        color_active = pygame.Color('dodgerblue2')
        name_text = ''
        
        title_font = pygame.font.Font(None, 72)

        while True:
            screen.fill(BG_COLOR)
            
            # Title
            title = title_font.render('SLITHER.IO MULTIPLAYER', True, (0, 255, 0))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            # Instructions
            inst1 = font.render('Enter Your Name', True, (255, 255, 255))
            inst2 = small_font.render('Press ENTER to play, ESC to quit', True, (150, 150, 150))
            screen.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(inst2, (SCREEN_WIDTH // 2 - inst2.get_width() // 2, SCREEN_HEIGHT - 100))

            # Name Input Box
            name_label = small_font.render('Your Name:', True, (255, 255, 255))
            screen.blit(name_label, (name_box.x, name_box.y - 25))
            pygame.draw.rect(screen, color_active, name_box, 2)
            
            name_surface = font.render(name_text, True, (255, 255, 255))
            screen.blit(name_surface, (name_box.x + 5, name_box.y + 5))

            pygame.display.flip()
            await asyncio.sleep(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None, None
                    
                    elif event.key == pygame.K_RETURN:
                        if name_text.strip(): # Ensure they entered something
                            return PERMANENT_SERVER, name_text
                    
                    elif event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    
                    else:
                        # Filter for actual characters and limit length
                        if len(name_text) < 20 and event.unicode.isprintable():
                            name_text += event.unicode



    # Shows a death screen counting down, then returns True to respawn or False to quit
    async def show_death_screen(score, respawn_time):
        while respawn_time > 0:
            screen.fill(BG_COLOR)
            screen.blit(font.render('YOU DIED!', True, (255, 0, 0)),
                        (SCREEN_WIDTH // 2 - font.size('YOU DIED!')[0] // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(font.render(f'Final Score: {int(score)}', True, (255, 255, 255)),
                        (SCREEN_WIDTH // 2 - font.size(f'Final Score: {int(score)}')[0] // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(small_font.render(f'Respawning in {int(respawn_time)} seconds...', True, (200, 200, 200)),
                        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30))
            pygame.display.flip()
            await asyncio.sleep(0.1)
            respawn_time -= 0.1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        return True


    # Main game loop - handles connection, input, server sync, drawing, and HUD each frame
    async def run():
        server_address, player_name = await show_connection_screen()
        if not server_address:
            pygame.quit()
            return

        player_color = await show_color_picker()
        if not player_color:
            pygame.quit()
            return

        network = NetworkManager()

        server_url = f"ws://localhost:8765"

        # Show connecting screen while waiting for handshake
        connect_task = asyncio.ensure_future(network.connect(server_url, player_name, player_color))
        waiting_start = pygame.time.get_ticks()

        while not network.connected:
            screen.fill(BG_COLOR)
            elapsed = (pygame.time.get_ticks() - waiting_start) // 1000
            msg = font.render(f'Connecting to server... ({elapsed}s)', True, (255, 255, 255))
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            await asyncio.sleep(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return

            if elapsed > 15:
                screen.fill(BG_COLOR)
                msg = font.render('Connection failed. Check server address.', True, (255, 0, 0))
                screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                await asyncio.sleep(3)
                pygame.quit()
                return

        local_player = Player(MAP_SIZE // 2, MAP_SIZE // 2, player_color, is_local=True)
        local_player.name = player_name
        other_players = {}
        foods = []
        running = True

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and local_player.alive:
                        local_player.boosting = True
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        local_player.boosting = False

            if local_player.alive:
                shed_food = local_player.update(dt)
                network.send_update({
                    'x': local_player.pos.x,
                    'y': local_player.pos.y,
                    'positions': [[p.x, p.y] for p in local_player.positions],
                    'radius': local_player.radius,
                    'length': local_player.length,
                    'score': local_player.score,
                    'alive': local_player.alive,
                    'shed_food': shed_food
                })

            await network.flush()

            game_state = network.game_state.copy()

            # Check if local player was killed server-side
            for player_data in game_state.get('players', []):
                if player_data['id'] == network.player_id and not player_data['alive'] and local_player.alive:
                    local_player.alive = False
                    if await show_death_screen(local_player.score, 5.0):
                        new_color = await show_color_picker()
                        if new_color:
                            network.send_respawn(new_color)
                            await asyncio.sleep(0.5)
                            local_player = Player(MAP_SIZE // 2, MAP_SIZE // 2, new_color, is_local=True)
                            local_player.name = player_name
                    else:
                        running = False

            foods = [Food(f) for f in game_state.get('foods', [])]

            if local_player.alive:
                for food in foods:
                    if local_player.pos.distance_to(food.pos) < local_player.radius + food.radius:
                        local_player.grow(food.value)
                        network.send_eat(food.id)

            other_players.clear()
            for player_data in game_state.get('players', []):
                if player_data['id'] != network.player_id and player_data.get('alive', True):
                    other = Player(player_data['x'], player_data['y'], tuple(player_data['color']))
                    other.radius = player_data['radius']
                    other.score = player_data['score']
                    other.name = player_data['name']
                    other.alive = player_data.get('alive', True)
                    if player_data.get('positions'):
                        other.positions = [pygame.math.Vector2(p[0], p[1]) for p in player_data['positions']]
                    else:
                        other.positions = [other.pos.copy()] * int(player_data.get('length', 150))
                    other_players[player_data['id']] = other

            camera_x = local_player.pos.x
            camera_y = local_player.pos.y

            screen.fill(BG_COLOR)

            map_left = -camera_x + SCREEN_WIDTH // 2
            map_top = -camera_y + SCREEN_HEIGHT // 2
            pygame.draw.rect(screen, (100, 100, 100), (map_left, map_top, MAP_SIZE, MAP_SIZE), 5)

            for x in range(0, MAP_SIZE, 100):
                start_x = x - camera_x + SCREEN_WIDTH // 2
                pygame.draw.line(screen, (40, 40, 40), (start_x, map_top), (start_x, map_top + MAP_SIZE), 1)
            for y in range(0, MAP_SIZE, 100):
                start_y = y - camera_y + SCREEN_HEIGHT // 2
                pygame.draw.line(screen, (40, 40, 40), (map_left, start_y), (map_left + MAP_SIZE, start_y), 1)

            for food in foods:
                food.draw(screen, camera_x, camera_y)
            for other in other_players.values():
                other.draw(screen, camera_x, camera_y)
            local_player.draw(screen, camera_x, camera_y)

            screen.blit(font.render(f'Score: {int(local_player.score)}', True, (255, 255, 255)), (10, 10))
            total_players = len(other_players) + (1 if local_player.alive else 0)
            screen.blit(small_font.render(f'Players: {total_players}', True, (255, 255, 255)), (10, 50))
            screen.blit(small_font.render(f'Length: {int(local_player.length)}', True, (255, 255, 255)), (10, 80))

            time_since_state = pygame.time.get_ticks() - network.last_state_time
            conn_color = (255, 0, 0) if time_since_state > 2000 else (0, 255, 0)
            conn_label = 'Connection Lost!' if time_since_state > 2000 else 'Connected'
            screen.blit(small_font.render(conn_label, True, conn_color), (SCREEN_WIDTH - 150, 10))

            all_scores = [(local_player.name, int(local_player.score))] + \
                         [(p.name, int(p.score)) for p in other_players.values()]
            all_scores.sort(key=lambda x: x[1], reverse=True)
            screen.blit(small_font.render('Leaderboard:', True, (255, 255, 0)), (10, 120))
            for i, (name, score) in enumerate(all_scores[:5]):
                screen.blit(small_font.render(f'{i+1}. {name}: {score}', True, (255, 255, 255)), (10, 150 + i * 25))

            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()

    await run()

asyncio.run(main())