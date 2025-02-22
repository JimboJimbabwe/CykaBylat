import os
import base64
import time
from datetime import datetime
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define static prompt
STATIC_PROMPT = "You will receive an image with text on the screen, your goal is to respond with the entirety of the text that is seen to the best of your ability."

class PhotoProcessor:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
            
        # Initialize console for rich output
        self.console = Console()
        
        # Create response directory if it doesn't exist
        if not os.path.exists("response"):
            os.makedirs("response")
            
        # Initialize counter for response files
        self.counter = len([f for f in os.listdir("response") if f.endswith('.txt')])

    def get_latest_photo(self):
        """Get the most recent photo from the ToClaude directory."""
        photos = [f for f in os.listdir("ToClaude") if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not photos:
            return None
        return os.path.join("ToClaude", photos[0])

    def send_to_claude(self, image_path, prompt):
        """Send image to Claude API and save response."""
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # Initialize Claude client
            client = anthropic.Anthropic(api_key=self.api_key)

            # Send request to Claude
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # Save response to file
            self.counter += 1
            response_file = f"response/response_{self.counter:03d}.txt"
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(message.content[0].text)

            # Display response in terminal
            self.console.print("\n")
            self.console.print(Panel(
                Markdown(message.content[0].text),
                title=f"Claude's Response (saved to {response_file})",
                border_style="blue"
            ))

            # Clean up the processed image
            os.remove(image_path)
            self.console.print("[green]Image processed and deleted successfully[/green]")

        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

class PhotoHandler(FileSystemEventHandler):
    def __init__(self, processor):
        self.processor = processor

    def on_created(self, event):
        if (not event.is_directory and 
            event.src_path.endswith(('.png', '.jpg', '.jpeg')) and 
            os.path.exists(event.src_path)):  # Verify file still exists
            # Wait a brief moment to ensure the file is fully written
            time.sleep(1)
            
            # Process the image with static prompt
            self.processor.send_to_claude(event.src_path, STATIC_PROMPT)

def main():
    # Create processor
    processor = PhotoProcessor()
    
    # Set up file system observer
    event_handler = PhotoHandler(processor)
    observer = Observer()
    observer.schedule(event_handler, path="ToClaude", recursive=False)
    observer.start()

    print("Watching ToClaude folder for new images...")
    print("Press Ctrl+C to stop")

    try:
        # Check if there's already an image in the folder
        existing_photo = processor.get_latest_photo()
        if existing_photo:
            processor.send_to_claude(existing_photo, STATIC_PROMPT)

        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping image processor...")
    observer.join()

if __name__ == "__main__":
    main()
