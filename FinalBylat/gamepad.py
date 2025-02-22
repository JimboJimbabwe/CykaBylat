import evdev
from evdev import InputDevice, categorize, ecodes
from rich.console import Console

console = Console()

def find_gamepad():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "gamepad" in device.name.lower():
            return device
    return None

def main():
    gamepad = find_gamepad()
    if not gamepad:
        console.print("[red]No gamepad found![/red]")
        return

    console.print(f"[green]Found gamepad: {gamepad.name}[/green]")
    console.print("Press Ctrl+C to stop\n")

    # Dictionary to store current state
    state = {
        'ABS_X': 127,
        'ABS_Y': 127,
        'Buttons': set()
    }

    try:
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_X:
                    direction = "CENTER"
                    if event.value < 127:
                        direction = "LEFT"
                    elif event.value > 127:
                        direction = "RIGHT"
                    console.print(f"X-Axis: {direction} ({event.value})")
                    
                elif event.code == ecodes.ABS_Y:
                    direction = "CENTER"
                    if event.value < 127:
                        direction = "UP"
                    elif event.value > 127:
                        direction = "DOWN"
                    console.print(f"Y-Axis: {direction} ({event.value})")

            elif event.type == ecodes.EV_KEY:
                if event.value == 1:  # Button pressed
                    console.print(f"[red]Button {event.code} pressed[/red]")
                elif event.value == 0:  # Button released
                    console.print(f"[blue]Button {event.code} released[/blue]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")

if __name__ == "__main__":
    main()
