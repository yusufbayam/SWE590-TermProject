#!/usr/bin/env python3
"""
Generate test images of different sizes for Locust performance testing.
"""
import os
from PIL import Image, ImageDraw
import random
import numpy as np

def create_test_image(name, width, height, complexity=10):
    """Create a test image with specified dimensions and visual complexity.
    
    Args:
        name: Filename for the test image
        width: Image width in pixels
        height: Image height in pixels
        complexity: Number of shapes to draw (affects file size)
    """
    # Create a blank image with a white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (128, 128, 128), (64, 64, 64), (192, 192, 192)
    ]
    
    # Add text
    draw.text((width//2 - 50, 10), f"{name} test image", fill=(0, 0, 0))
    
    for _ in range(complexity * 10):
        # Random rectangles
        x1 = random.randint(0, width - 10)
        y1 = random.randint(0, height - 10)
        x2 = random.randint(x1 + 1, width)
        y2 = random.randint(y1 + 1, height)
        color = random.choice(colors)
        draw.rectangle([x1, y1, x2, y2], outline=color)
        
        # Random circles
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(5, min(50, width//8, height//8))  
        color = random.choice(colors)
        left = max(0, x-r)
        top = max(0, y-r)
        right = min(width-1, x+r)
        bottom = min(height-1, y+r)
        if left < right and top < bottom:
            draw.ellipse((left, top, right, bottom), outline=color)
        
        # Random lines
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = random.choice(colors)
        draw.line([x1, y1, x2, y2], fill=color, width=2)
    
    if name != "small":
        img_array = np.array(img)
        noise_level = 10 if name == "medium" else 20
        noise = np.random.randint(-noise_level, noise_level, img_array.shape, dtype=np.int16)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        
        img = Image.fromarray(img_array)
    
    img.save(f"test_images/{name}.png", quality=95 if name == "large" else 85)
    
    file_size = os.path.getsize(f"test_images/{name}.png") / 1024  # KB
    print(f"Created {name}.png ({file_size:.2f} KB)")

def main():
    """Generate test images of different sizes."""
    os.makedirs("test_images", exist_ok=True)
    
    # Create small image (~50KB)
    create_test_image("small", 200, 150, complexity=5)
    
    # Create medium image (~500KB)
    create_test_image("medium", 400, 300, complexity=10)
    
    # Create large image (~2MB)
    create_test_image("large", 600, 450, complexity=20)

if __name__ == "__main__":
    main() 