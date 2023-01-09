import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set the window size
window_size = (600, 950)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Procedural Catching Game")

# Set the font and size for the score
font = pygame.font.Font(None, 36)

# Set the speed of the notes
note_speed = 1

# Set the dimensions of the notes
note_width = 20
note_height = 20

# Set the dimensions of the target
target_width = 80
target_height = 30

# Set the initial position of the target
target_x = window_size[0] // 2 - target_width // 2
target_y = window_size[1] - target_height

# Set the maximum length of the trail
trail_length = 100

# Set the width and height of the trail
trail_width = 5
trail_height = 5

# Set the color of the trail
trail_color = (255, 255, 255)

# Set the initial score
score = 0

# Set the initial amount of misses
misses = 0

# Initialize the notes and the target
notes = []
target = pygame.Rect(target_x, target_y, target_width, target_height)

# Initialize the trail
trail = []
trail_delay = 0

# Initialize the game loop
running = True
while running:
  # Initialize the keys that are currently pressed
  keys_pressed = pygame.key.get_pressed()

  # Handle player input
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False

  # Set the base movement speed
  movement_speed = 1

  # Increase the movement speed if the left shift key is pressed
  if keys_pressed[pygame.K_LSHIFT]:
    movement_speed *= 2

  # Update the position of the target based on the keys that are currently pressed
  if keys_pressed[pygame.K_LEFT]:
    target_x -= movement_speed
  if keys_pressed[pygame.K_RIGHT]:
    target_x += movement_speed

  # Clamp the position of the target to the screen boundaries to prevent it from leaving the window
  if target_x < 0:
    target_x = 0
  elif target_x > window_size[0] - target_width:
    target_x = window_size[0] - target_width

  # Update the position of the target
  target.x = target_x

  # Set the maximum distance from the target at which a note can be generated
  max_distance = 100

  # Generate a new note every few frames
  if random.randint(0, 300) == 0:
    # Generate a random position within the maximum distance of the target
    note_x = random.randint(target_x - max_distance, target_x + max_distance)
    note_y = 0

    for note in notes:
      if note.x < 0 or note.x > window_size[0] - note_width or (note.y + note_height) > window_size[1]:
        notes.remove(note)
        misses += 1

    # Create a new note at the generated position
    notes.append(pygame.Rect(note_x, note_y, note_width, note_height))

  # Update the position of the notes
  for note in notes:
    note.y += note_speed

  # Check if any of the notes have reached the target
  for note in notes:
    if note.colliderect(target):
      notes.remove(note)
      score += 1

  # Set the initial alpha value for the trail
  trail_alpha = 255

  # Set the amount by which the alpha value decreases each frame
  trail_alpha_decay = 5

  # Increment the trail delay
  trail_delay += 1
    
  # Update the trail
  if keys_pressed[pygame.K_LSHIFT] and trail_delay >= 10:
        # Reset the trail delay
        trail_delay = 0

        # Add the current position of the target to the trail
        trail.append((target_x, target_y))

   # Keep the length of the trail within the maximum length
   if len(trail) > trail_length:
            trail.pop(0)

  # Draw the trail
  for i, (x, y) in enumerate(trail):
        # Calculate the alpha value for the current trail segment
        alpha = trail_alpha - (trail_alpha_decay * i)

        # Make sure the alpha value is within the valid range
        alpha = max(0, min(255, alpha))

        #Create a surface with the current alpha value
        surface = pygame.Surface((trail_width, trail_height))
        surface.set_alpha(alpha)

        # Set the color of the surface
        surface.fill(trail_color)

        # Draw the surface on the screen
        screen.blit(surface, (x, y))

  
  # Check if any of the notes have reached the bottom of the screen
  for note in notes:
       if note.y > window_size[1]:
        notes.remove(note)
        misses += 1


  # Clear the screen
  screen.fill((0, 0, 0))
  
  # Draw the notes
  for note in notes:
    pygame.draw.rect(screen, (255, 0, 0), note)
  


  # Draw the target
  pygame.draw.rect(screen, (0, 255, 0), target)
  

  
  # Draw the score
  score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
  screen.blit(score_text, (10, 10))

    # Draw the Misses
  misses_text = font.render("Misses: {}".format(misses), True, (255, 255, 255))
  screen.blit(misses_text, (window_size[0] - 150, 10))
  
 pygame.display.flip()




