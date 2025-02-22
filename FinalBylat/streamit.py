import cv2

def find_max_resolution(cap):
    # Common resolutions to test (width, height)
    resolutions = [
        (4096, 2160),  # 4K
        (3840, 2160),  # 4K UHD
        (2560, 1440),  # 2K
        (1920, 1080),  # Full HD
        (1280, 720),   # HD
        (640, 480)     # VGA
    ]
    
    for width, height in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Get actual resolution
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # If we got a valid resolution, return it
        if actual_width > 0 and actual_height > 0:
            return actual_width, actual_height
            
    return 640, 480  # Default fallback

# Open camera
cap = cv2.VideoCapture(0)

# Find and set the maximum supported resolution
width, height = find_max_resolution(cap)
print(f"Camera resolution: {width}x{height}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Add resolution text to frame
    resolution_text = f"{width}x{height}"
    cv2.putText(frame, resolution_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
    # Show frame in window that matches camera resolution
    cv2.namedWindow('Camera Test (Press Q to quit)', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera Test (Press Q to quit)', width, height)
    cv2.imshow('Camera Test (Press Q to quit)', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
