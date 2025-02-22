import subprocess
import time
import os
import glob
import signal

def run_system():
    # Start presentation viewer in background
    print("Starting Presentation viewer...")
    presentation = subprocess.Popen(['python', 'Presentation.py'])
    
    # Start Claude in background
    print("Starting Claude processor...")
    claude = subprocess.Popen(['python', 'ClaudeCamd.py'])
    
    try:
        while True:
            # Take new photo
            print("\nTaking new photo...")
            subprocess.run(['python', 'CamBro.py'])
            
            # Wait for image to be processed (check for deletion)
            while glob.glob("ToClaude/*.png"):
                print("Waiting for Claude to process image...")
                time.sleep(1)
            
            # Wait for user input before next photo
            input("\nPress Enter to take another photo or Ctrl+C to quit...")
            
    except KeyboardInterrupt:
        print("\nShutting down system...")
    finally:
        # Clean up processes
        print("Stopping Claude processor...")
        claude.terminate()
        claude.wait()
        
        print("Stopping Presentation viewer...")
        presentation.terminate()
        presentation.wait()
        
        print("System shutdown complete.")

if __name__ == "__main__":
    print("Starting camera system...")
    print("Press Ctrl+C at any time to stop all processes and exit.")
    run_system()
