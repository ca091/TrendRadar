import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# The directory to watch, will be mounted from the host
WATCH_DIRECTORY = "/watch"

class TxtFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".txt"):
            print(f"New text file detected: {event.src_path}", flush=True)
            time.sleep(1)
            self.process_file(event.src_path)

    def process_file(self, file_path):
        """
        Processes the detected .txt file and converts it to a structured, readable HTML file.
        """
        try:
            print(f"Processing {file_path} with corrected readability logic...", flush=True)

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            html_parts = []
            in_list = False  # State variable to track if we are inside an <ol> tag

            # Corrected, more specific regex for list items
            item_pattern = re.compile(r'^\s*\d+\.\s+(.*)\s+\[URL:(.*?)\]\s*(?:[ MOBILE:.*?])?\s*$')

            for line in lines:
                line = line.strip()
                if not line:
                    if in_list:
                        html_parts.append('</ol>')
                        in_list = False
                    continue

                item_match = item_pattern.match(line)

                # First, try to match the most specific pattern: a list item
                if item_match:
                    if not in_list:
                        html_parts.append('<ol>')
                        in_list = True
                    
                    text = item_match.group(1).strip()
                    url = item_match.group(2).strip()
                    
                    html_parts.append(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a></li>')
                
                # If it's not an item, check if it's a title using a simple string split
                elif ' | ' in line:
                    if in_list:
                        html_parts.append('</ol>')
                        in_list = False
                    
                    parts = line.split(' | ', 1)
                    if len(parts) == 2:
                        name, chinese_name = parts
                        html_parts.append(f'<h2>{name.strip()} - {chinese_name.strip()}</h2>')
                    else: # Fallback for malformed title
                        html_parts.append(f'<p>{line}</p>')

                # Fallback for any other non-empty line
                else:
                    if in_list:
                        html_parts.append('</ol>')
                        in_list = False
                    html_parts.append(f'<p>{line}</p>')

            if in_list:
                html_parts.append('</ol>')

            html_body = "\n".join(html_parts)

            base_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(base_name)[0]
            output_path = os.path.join(os.path.dirname(file_path), f"{file_name_without_ext}.html")

            # Basic CSS for better readability
            html_head = f"""<head>
    <meta charset="UTF-8">
    <title>{file_name_without_ext}</title>
    <style>
        body {{ background: #C7EDCC; }}
        ol {{ padding-left: 2em; }}
        li {{ margin-bottom: 0.4em; }}
        a {{ text-decoration: none; color: #3C3C3C; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>"""

            html_content = f"""<!DOCTYPE html>
<html lang="en">
{html_head}
<body>
{html_body}
</body>
</html>"""

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"Successfully converted {file_path} to {output_path}", flush=True)

        except Exception as e:
            print(f"Error processing {file_path}: {e}", flush=True)


if __name__ == "__main__":
    if not os.path.isdir(WATCH_DIRECTORY):
        print(f"Error: Watch directory '{WATCH_DIRECTORY}' does not exist.", flush=True)
        exit(1)

    print(f"Starting file watcher for directory: {WATCH_DIRECTORY}", flush=True)
    event_handler = TxtFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("File watcher stopped.", flush=True)