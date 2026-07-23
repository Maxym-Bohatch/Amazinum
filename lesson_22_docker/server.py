import http.server
import socketserver
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9090

class DynamicVideoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Якщо запитують головну сторінку
        if self.path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Шукаємо .mp4 у папці videos або поточній
            video_name = ""
            search_dir = "videos" if os.path.exists("videos") else "."
            
            for file in os.listdir(search_dir):
                if file.lower().endswith('.mp4'):
                    video_name = file
                    break

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Local YouTube</title>
                <style>
                    body {{ background: #0f0f0f; color: white; font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
                    h1 {{ color: #ff0000; }}
                    video {{ background: black; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
                </style>
            </head>
            <body>
                <h1>🔴 My Local YouTube Hub</h1>
                {'<p>Знайдено файл: <b>' + video_name + '</b></p>' if video_name else '<p>⚠️ Не знайдено жодного .mp4 файлу у папці videos!</p>'}
                <div style="margin-top: 20px;">
                    {'<video width="720" height="405" controls autoplay muted><source src="/' + (('videos/' + video_name) if os.path.exists("videos") else video_name) + '" type="video/mp4"></video>' if video_name else ''}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            # Для відтворення самого mp4 файлу викликаємо базовий SimpleHTTPRequestHandler
            super().do_GET()

# Запускаємо сервер
with socketserver.TCPServer(("", PORT), DynamicVideoHandler) as httpd:
    print(f"Server started on port {PORT}...")
    httpd.serve_forever()