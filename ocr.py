import pygame
import pygame.camera
import numpy as np
from pygame.locals import *
from PIL import Image
import sys
from pyzbar.pyzbar import decode
import cv2
import time

def init_camera():
    pygame.init()
    pygame.camera.init()
    cameras = pygame.camera.list_cameras()
    if not cameras:
        print("Error: No cameras found!")
        return None
    print(f"Found camera: {cameras[0]}")
    return pygame.camera.Camera(cameras[0], (640, 480))


def show_qr_result(screen, qr_data, duration=3):
    """Show QR content directly on camera screen for specified duration"""
    start_time = time.time()

    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 24)

    while time.time() - start_time < duration:
        # Keep displaying camera feed in background
        img = cam.get_image()
        screen.blit(img, (0, 0))

        # Create semi-transparent overlay
        overlay = pygame.Surface((640, 480), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity

        # Draw result box
        pygame.draw.rect(overlay, (30, 30, 50, 200), (50, 50, 540, 180))

        # Title
        title = font.render("QR CODE DETECTED:", True, (0, 255, 255))
        overlay.blit(title, (70, 60))

        # Wrap long text
        wrapped = []
        if len(qr_data) > 50:  # Adjust wrap length for screen
            wrapped = [qr_data[i:i + 50] for i in range(0, len(qr_data), 50)]
        else:
            wrapped = [qr_data]

        # Display content
        for i, line in enumerate(wrapped):
            text = small_font.render(line, True, (220, 220, 255))
            overlay.blit(text, (70, 100 + i * 30))

        # Countdown
        remaining = int(duration - (time.time() - start_time))
        countdown = small_font.render(f"Returning in {remaining}s...", True, (180, 180, 180))
        overlay.blit(countdown, (70, 200))

        screen.blit(overlay, (0, 0))
        pygame.display.flip()

        # Check for exit
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False

    return True

def realtime_qr_scan(cam):
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Auto QR Scanner - ESC to Exit")

    font = pygame.font.Font(None, 36)
    last_scan_time = 0
    scan_interval = 1  # Seconds between scans

    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = time.time()

        # Process exit events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Continuous scanning
        if current_time - last_scan_time > scan_interval:
            img = cam.get_image()
            img_array = np.array(Image.frombytes("RGB", (640, 480), pygame.image.tostring(img, "RGB")))

            # QR Detection
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            qr_codes = decode(gray)

            if qr_codes:
                last_scan_time = current_time
                if not show_qr_result(screen, qr_codes[0].data.decode('utf-8')):
                    running = False
                    break

        # Display live feed
        img = cam.get_image()
        screen.blit(img, (0, 0))

        # Display scanning status
        status_text = font.render("Scanning...", True, (0, 255, 0))
        screen.blit(status_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)


def main():
    global cam
    cam = init_camera()
    if not cam:
        return

    cam.start()
    realtime_qr_scan(cam)
    cam.stop()
    pygame.quit()

if __name__ == "__main__":
    main()