import cv2
import time
import os

def configure_camera():
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Failed to open camera")
        return
        
    try:
        # Initial camera warm-up
        print("\nInitial camera warm-up...")
        time.sleep(5)
        
        # Set resolution first
        print("\nSetting resolution...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # C270 will automatically adjust to 1280x720
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Refined settings that worked well
        print("\nConfiguring camera settings...")
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)   # Manual exposure mode
        cap.set(cv2.CAP_PROP_EXPOSURE, 108)         # Our good exposure value
        cap.set(cv2.CAP_PROP_GAIN, 0)               # Minimum gain
        cap.set(cv2.CAP_PROP_SHARPNESS, 75)         # Reduced sharpness
        cap.set(cv2.CAP_PROP_CONTRAST, 40)          # Slight contrast boost
        
        # Let settings stabilize
        print("Letting settings stabilize...")
        time.sleep(3)
        
        # Discard initial frames
        print("Discarding initial frames...")
        for _ in range(10):
            cap.read()
            time.sleep(0.2)
        
        # Take test photo
        print("\nTaking test photo...")
        ret, frame = cap.read()
        if ret:
            # Check actual resolution
            height, width = frame.shape[:2]
            print(f"\nActual frame size: {width}x{height}")
            
            if not os.path.exists('webcam_tests'):
                os.makedirs('webcam_tests')
                
            # Apply our successful denoising
            denoised = cv2.fastNlMeansDenoisingColored(frame, None, 5, 5, 7, 21)
            
            # Save both original and denoised versions
            timestamp = time.strftime("%H%M%S")
            cv2.imwrite(f'webcam_tests/full_res_original_{timestamp}.jpg', frame)
            cv2.imwrite(f'webcam_tests/full_res_denoised_{timestamp}.jpg', denoised)
            
            print(f"\nSaved images with resolution {width}x{height}")
            print("\nCurrent settings:")
            print(f"- Resolution: {width}x{height}")
            print("- Exposure: 108")
            print("- Gain: 0")
            print("- Sharpness: 75")
            print("- Contrast: 40")
            
            # Print available resolutions
            print("\nChecking available resolutions...")
            test_resolutions = [
                (640, 480),
                (800, 600),
                (1280, 720),
                (1920, 1080)
            ]
            
            for w, h in test_resolutions:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
                actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"Requested: {w}x{h} -> Got: {actual_w}x{actual_h}")
                
        else:
            print("Failed to capture test frame")
    
    finally:
        cap.release()

if __name__ == "__main__":
    configure_camera()
