#!/usr/bin/env python3
"""
🚀 Portfolio Server - Serve the Interactive HTML Portfolio with AI Agent Backend
Run this server and open http://localhost:5000 in your browser
"""

import json
import os
import sys
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread


# ANSI Colors for terminal output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class PortfolioServer(ThreadingHTTPServer):
    """Multi-threaded HTTP server that allows quick socket reuse"""
    allow_reuse_address = True


class PortfolioHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve portfolio assets and handle AI agent API requests"""

    def do_GET(self):
        """Serve portfolio.html by default at root"""
        if self.path in ('/', ''):
            self.path = '/portfolio.html'
        return super().do_GET()

    def do_POST(self):
        """Handle AI Agent queries securely on the backend"""
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                payload = json.loads(post_data.decode('utf-8'))
                user_query = payload.get('message', '').strip()

                # --- AI AGENT LOGIC / LLM API CALL GOES HERE ---
                # Example: Call your model provider (Gemini, OpenAI, or local weights)
                agent_reply = self.generate_agent_response(user_query)

                response_bytes = json.dumps({'reply': agent_reply}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)

            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON payload.")
            except Exception as e:
                self.send_error_response(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found.")

    def generate_agent_response(self, query: str) -> str:
        """Agent response placeholder. Plug your LLM client or rules engine here."""
        if not query:
            return "Please provide a question about my portfolio or experience!"
        return f"Agent received your question: '{query}'. Connect your LLM API here to respond."

    def send_error_response(self, code: int, message: str):
        """Helper to send structured JSON error replies"""
        body = json.dumps({'error': message}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        """Add headers to prevent caching during local development"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        """Custom clean logging"""
        print(f"{Colors.GREEN}[{self.client_address[0]}]{Colors.RESET} {format % args}")


def print_banner(port):
    """Print status banner"""
    banner = f"""
{Colors.MAGENTA}╔════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.MAGENTA}║{Colors.CYAN}  🚀 RISHTHIK AYMAN'S PORTFOLIO SERVER v1.0 🚀{Colors.MAGENTA}  ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  Status: Online & Running{Colors.MAGENTA}                          ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.YELLOW}  📍 Server: http://localhost:{port:<27}{Colors.MAGENTA}║{Colors.RESET}
{Colors.MAGENTA}║{Colors.CYAN}  🌐 Opening in browser...{Colors.MAGENTA}                        ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.BOLD}  Features:{Colors.RESET}{Colors.MAGENTA}                                             ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Interactive Portfolio{Colors.MAGENTA}                               ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Resume AI Agent Backend (/api/chat){Colors.MAGENTA}                  ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Project Showcase & Animations{Colors.MAGENTA}                       ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.YELLOW}  Press CTRL+C to stop the server{Colors.MAGENTA}                        ║{Colors.RESET}
{Colors.MAGENTA}╚════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def open_browser(url, delay=1):
    """Open default browser after a brief delay"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"{Colors.GREEN}✓ Browser opened successfully!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠ Could not open browser automatically: {e}{Colors.RESET}")
        print(f"{Colors.CYAN}Please manually open: {url}{Colors.RESET}")


def start_server(port=5000):
    """Start the multi-threaded HTTP server"""
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)

    server_address = ('', port)
    httpd = PortfolioServer(server_address, PortfolioHandler)

    print_banner(port)

    url = f'http://localhost:{port}'
    browser_thread = Thread(target=open_browser, args=(url,), daemon=True)
    browser_thread.start()

    print(f"{Colors.BOLD}{Colors.CYAN}Server Details:{Colors.RESET}")
    print(f"  {Colors.GREEN}Host:{Colors.RESET} localhost")
    print(f"  {Colors.GREEN}Port:{Colors.RESET} {port}")
    print(f"  {Colors.GREEN}Directory:{Colors.RESET} {script_dir}\n")

    try:
        print(f"{Colors.BOLD}{Colors.GREEN}🎉 Server started! Serving files from {script_dir}{Colors.RESET}\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Shutting down server...{Colors.RESET}")
        httpd.shutdown()
        print(f"{Colors.GREEN}✓ Server stopped cleanly.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.MAGENTA}✗ Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    port = 5000

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"{Colors.MAGENTA}✗ Invalid port number. Falling back to default port 5000{Colors.RESET}")

    start_server(port)
