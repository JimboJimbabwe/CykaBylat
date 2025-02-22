import subprocess
import time
import os
import glob
import signal
import evdev
from evdev import InputDevice, categorize, ecodes
from rich.console import Console

console = Console()

def find_gamepad():
    """Find the USB gamepad."""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "gamepad" in device.name.lower():
            return device
    return None

def run_system():
    # Find and setup gamepad
    gamepad = find_gamepad()
    if not gamepad:
        console.print("[red]No gamepad found! Please connect gamepad and try again.[/red]")
        return
    
    console.print(f"[green]Found gamepad: {gamepad.name}[/green]")
    
    # Start presentation viewer in background
    console.print("\nStarting Presentation viewer...")
    presentation = subprocess.Popen(['python', 'Presentation.py'])
    
    # Start Claude in background
    console.print("Starting Claude processor...")
    claude = subprocess.Popen(['python', 'ClaudeCamd.py'])
    
    console.print("\n[bold green]System ready![/bold green]")
    console.print("Press button 290 to take a photo")
    console.print("Press Ctrl+C to quit")
    
    try:
        # Monitor gamepad events
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_KEY and event.code == 290:  # BTN_THUMB
                if event.value == 1:  # Button press (not release)
                    console.print("\n[yellow]Button pressed - Taking photo...[/yellow]")
                    
                    # Take new photo
                    subprocess.run(['python', 'CamBro.py'])
                    
                    # Wait for image to be processed
                    while glob.glob("ToClaude/*.png"):
                        console.print("[cyan]Waiting for Claude to process image...[/cyan]")
                        time.sleep(1)
                    
                    console.print("[green]Ready for next photo![/green]")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down system...[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
    finally:
        # Clean up processes
        console.print("Stopping Claude processor...")
        claude.terminate()
        claude.wait()
        
        console.print("Stopping Presentation viewer...")
        presentation.terminate()
        presentation.wait()
        
        console.print("[green]System shutdown complete.[/green]")

if __name__ == "__main__":
    console.print("[bold blue]Starting camera system...[/bold blue]")
    run_system()
