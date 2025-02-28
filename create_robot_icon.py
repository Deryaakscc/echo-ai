from PIL import Image, ImageDraw
import os

def create_circle_icon(size, color, robot=False):
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw the circle
    draw.ellipse([0, 0, size-1, size-1], fill=color)
    
    if robot:
        # Draw robot face
        eye_color = (255, 255, 255)
        eye_size = size // 6
        eye_spacing = size // 4
        eye_y = size * 0.35
        
        # Left eye
        draw.ellipse([size//2 - eye_spacing - eye_size, eye_y,
                     size//2 - eye_spacing + eye_size, eye_y + eye_size*2],
                    fill=eye_color)
        
        # Right eye
        draw.ellipse([size//2 + eye_spacing - eye_size, eye_y,
                     size//2 + eye_spacing + eye_size, eye_y + eye_size*2],
                    fill=eye_color)
        
        # Mouth
        mouth_y = size * 0.65
        mouth_width = size * 0.4
        draw.rectangle([size//2 - mouth_width//2, mouth_y,
                       size//2 + mouth_width//2, mouth_y + size//10],
                      fill=eye_color)
        
        # Antenna
        antenna_width = size // 20
        draw.rectangle([size//2 - antenna_width//2, 0,
                       size//2 + antenna_width//2, size//4],
                      fill=eye_color)
        draw.ellipse([size//2 - size//10, size//4 - size//10,
                     size//2 + size//10, size//4 + size//10],
                     fill=eye_color)
    
    return image

def create_logo():
    # Create logo with robot face
    logo = create_circle_icon(400, (76, 91, 224), robot=True)  # Modern blue color
    logo.save('assets/logo.png')

def create_avatars():
    # Create user avatar (simple circle)
    user = create_circle_icon(200, (76, 91, 224))  # Same blue as logo
    user.save('assets/user.png')
    
    # Create bot avatar (circle with robot face)
    bot = create_circle_icon(200, (76, 91, 224), robot=True)  # Same blue as logo
    bot.save('assets/bot.png')
    
    # Create coin icon
    coin = create_circle_icon(100, (255, 200, 50))  # Gold color
    coin.save('assets/coin.png')
    
    # Create send icon
    send = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(send)
    
    # Draw send arrow
    points = [(20, 50), (80, 20), (80, 80)]
    draw.polygon(points, fill=(255, 255, 255))
    
    send.save('assets/send.png')

if __name__ == '__main__':
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    create_logo()
    create_avatars() 