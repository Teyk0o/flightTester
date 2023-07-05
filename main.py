import pygame
import sys

# Constantes / Options

# Fenêtre de simulation
WIDTH = 800
HEIGHT = 600
FPS = 60

# Simulateur
GROUND_HEIGHT = 100
GROUND_COLOR = (152, 251, 152)  # Vert clair

OBJECT_WIDTH = 50
OBJECT_HEIGHT = 100
OBJECT_COLOR = (255, 0, 0)  # Rouge

AIR_COLOR = (0, 0, 0)  # Noir

LAUNCHING = False

PROPULSOR_TOTAL_IMPULSE = 200 # Impulsion totale en N-sec
PROPULSOR_AVERAGE_THRUST = 144 # Poussée moyenne en Newton
PROPULSOR_MAX_THRUST = 186 # Poussée maximale en Newton

# Initialisation de PyGame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulation de décollage')
clock = pygame.time.Clock()

# Classe de l'objet
class Object:
    def  __init__(self, x, y, mass, drag_coefficient):
        self.x = x
        self.y = y
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.velocity = 0.0
        self.max_height = 0.0
        self.falling = False

    def update(self, thrust, dt):

        # Calcul de la force résultante
        gravity = self.mass * 9.8 # Force Gravitationnelle
        drag = 0.5 * self.drag_coefficient* self.velocity**2 # Force de traction
        net_force = thrust - gravity - drag

        # Calcul de l'accélération
        acceleration = net_force / self.mass

        # Mise à jour de la vitesse et de la position
        if thrust == 0:
            self.falling = True
            self.velocity -= gravity * dt
        else:
            self.velocity += acceleration * dt

        self.y -= self.velocity * dt

        # Mise à jour de la hauteur maximale atteinte
        if ((HEIGHT - GROUND_HEIGHT - self.y) - 100) > self.max_height:
            self.max_height = ((HEIGHT - GROUND_HEIGHT - self.y) - 100)

        # Vérifier si l'objet a touché le sol et arrêter la simulation
        if self.y >= HEIGHT - GROUND_HEIGHT - OBJECT_HEIGHT and self.velocity <= 0 and self.falling and LAUNCHING:
            self.y = HEIGHT - GROUND_HEIGHT - OBJECT_HEIGHT
            self.velocity = 0
            # Afficher la hauteur maximale atteinte
            height_in_meters = self.max_height / 0.7444 # (100px = 1m)

            print("Hauteur maximale atteinte :", height_in_meters)

        print("Hauteur (en px) : " + str(self.max_height))

    def draw(self):
        pygame.draw.rect(screen, OBJECT_COLOR, (self.x, self.y, OBJECT_WIDTH, OBJECT_HEIGHT))

# Événements de simulation
def handle_events():
    global LAUNCHING

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                LAUNCHING = True

# Boucle de simulation
def main():
    PROPULSOR_THRUST_DURATION = 1.5 # Durée de poussée en secondes

    obj = Object(WIDTH // 2 - OBJECT_WIDTH // 2, HEIGHT - GROUND_HEIGHT - OBJECT_HEIGHT, 0.1, 0.5)

    # Calcul de la poussée totale en fonction de la poussée moyenne et de la durée de propulsion
    total_thrust = PROPULSOR_AVERAGE_THRUST * PROPULSOR_THRUST_DURATION

    # Calcul de la poussée maximale en fonction de la poussée totale et de la durée
    if total_thrust > PROPULSOR_MAX_THRUST:
        total_thrust = PROPULSOR_MAX_THRUST

    # Calcul de la poussée par seconde
    thrust_per_second = total_thrust / PROPULSOR_THRUST_DURATION

    # Variable pour la hauteur maximale atteinte
    max_height = 0

    # Boucle principale de simulation
    while True:

        screen.fill(AIR_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Calcul du temps écoulé depuis la dernière frame
        dt = clock.tick(FPS) / 1000.0

        obj.draw()
        handle_events()

        if LAUNCHING:
            obj.update(thrust_per_second, dt)

        # Vérifier si la durée de propulsion est écoulée
        if PROPULSOR_THRUST_DURATION <= 0:
            thrust_per_second = 0

        # Mettre à jour la hauteur maximale
        if obj.y > max_height:
            max_height = obj.y

        # Vérifier si l'objet a touché le sol et arrêter la simulation
        # if obj.y >= HEIGHT - GROUND_HEIGHT - OBJECT_HEIGHT and obj.velocity >= 0 and obj.falling:
        #     break

        # Réduire la durée de propulsion
        PROPULSOR_THRUST_DURATION -= dt

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()