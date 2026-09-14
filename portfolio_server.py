#!/usr/bin/env python3
"""
🚀 Portfolio Server - Serve the Interactive HTML Portfolio with AI Agent
Run this server and open http://localhost:5000 in your browser
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import webbrowser
from threading import Thread
import time

# ANSI Colors for terminal output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class PortfolioHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve portfolio.html"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '':
            self.path = '/portfolio.html'
        return super().do_GET()
    
    def end_headers(self):
        """Add headers to prevent caching"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"{Colors.GREEN}[{self.client_address[0]}]{Colors.RESET} {format % args}")


def print_banner():
    """Print a fancy banner"""
    banner = f"""
{Colors.MAGENTA}╔════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.MAGENTA}║{Colors.CYAN}  🚀 RISHTHIK AYMAN'S PORTFOLIO SERVER v1.0 🚀{Colors.MAGENTA}  ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  Status: Online & Running{Colors.MAGENTA}                          ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.YELLOW}  📍 Server: http://localhost:5000{Colors.MAGENTA}               ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.CYAN}  🌐 Opening in browser...{Colors.MAGENTA}                        ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.BOLD}  Features:{Colors.RESET}{Colors.MAGENTA}                                         ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Interactive Portfolio{Colors.MAGENTA}                       ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Resume AI Agent Chatbot{Colors.MAGENTA}                    ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Project Showcase{Colors.MAGENTA}                          ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Smooth Animations{Colors.MAGENTA}                        ║{Colors.RESET}
{Colors.MAGENTA}║{Colors.GREEN}  ✓ Responsive Design{Colors.MAGENTA}                        ║{Colors.RESET}
{Colors.MAGENTA}╠════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.MAGENTA}║{Colors.YELLOW}  Press CTRL+C to stop the server{Colors.MAGENTA}                    ║{Colors.RESET}
{Colors.MAGENTA}╚════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def open_browser(url, delay=1):
    """Open browser after a short delay"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"{Colors.GREEN}✓ Browser opened successfully!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠ Could not open browser automatically: {e}{Colors.RESET}")
        print(f"{Colors.CYAN}Please manually open: {url}{Colors.RESET}")


def start_server(port=5000):
    """Start the HTTP server"""
    # Change to the directory where portfolio.html is located
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Create server
    server_address = ('', port)
    httpd = HTTPServer(server_address, PortfolioHandler)
    
    # Print banner
    print_banner()
    
    # Open browser in a separate thread
    url = f'http://localhost:{port}'
    browser_thread = Thread(target=open_browser, args=(url,), daemon=True)
    browser_thread.start()
    
    # Server info
    print(f"{Colors.BOLD}{Colors.CYAN}Server Details:{Colors.RESET}")
    print(f"  {Colors.GREEN}Host:{Colors.RESET} localhost")
    print(f"  {Colors.GREEN}Port:{Colors.RESET} {port}")
    print(f"  {Colors.GREEN}URL:{Colors.RESET} http://localhost:{port}")
    print(f"  {Colors.GREEN}Directory:{Colors.RESET} {script_dir}\n")
    
    try:
        print(f"{Colors.BOLD}{Colors.GREEN}🎉 Server started! Serving files from {script_dir}{Colors.RESET}\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Shutting down server...{Colors.RESET}")
        httpd.shutdown()
        print(f"{Colors.GREEN}✓ Server stopped. Goodbye!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.MAGENTA}✗ Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    port = 5000
    
    # Allow custom port via command line
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"{Colors.MAGENTA}✗ Invalid port number. Using default port 5000{Colors.RESET}")
    
    start_server(port)
