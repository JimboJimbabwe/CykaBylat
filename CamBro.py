import cv2
import time
import os

def capture_photo():
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Failed to open camera")
        return
        
    try:
        # Initial camera warm-up
        print("\nInitial camera warm-up...")
        time.sleep(5)
        
        # Set resolution and our known good settings
        print("\nConfiguring camera settings...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, 108)
        cap.set(cv2.CAP_PROP_GAIN, 0)
        cap.set(cv2.CAP_PROP_SHARPNESS, 75)
        cap.set(cv2.CAP_PROP_CONTRAST, 40)
        
        # Let settings stabilize
        print("Letting settings stabilize...")
        time.sleep(3)
        
        # Discard initial frames
        print("Discarding initial frames...")
        for _ in range(10):
            cap.read()
            time.sleep(0.2)
        
        # Create directories if they don't exist
        for directory in ['ToBackup', 'ToClaude']:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"\nCreated directory: {directory}")
        
        # Take photo
        print("\nTaking photo...")
        ret, frame = cap.read()
        if ret:
            # Apply denoising
            denoised = cv2.fastNlMeansDenoisingColored(frame, None, 5, 5, 7, 21)
            
            # Generate timestamp for filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # Save to both directories with PNG format
            backup_path = f'ToBackup/image_{timestamp}.png'
            claude_path = f'ToClaude/image_{timestamp}.png'
            
            cv2.imwrite(backup_path, denoised)
            cv2.imwrite(claude_path, denoised)
            
            print(f"\nSaved denoised image to:")
            print(f"- {backup_path}")
            print(f"- {claude_path}")
        else:
            print("Failed to capture photo")
    
    finally:
        cap.release()
        print("\nCamera released")

if __name__ == "__main__":
    capture_photo()
