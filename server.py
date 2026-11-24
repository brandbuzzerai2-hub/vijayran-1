import os, sys, http.server, socketserver

class RangeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_head(self):
        self.range_length = None
        if 'Range' not in self.headers:
            return super().send_head()
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().send_head()
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(http.HTTPStatus.NOT_FOUND, "File not found")
            return None
        size = os.path.getsize(path)
        range_header = self.headers.get('Range', '').strip()
        if not range_header.startswith('bytes='):
            return super().send_head()
        bytes_range = range_header[6:].strip()
        parts = bytes_range.split('-')
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if len(parts) > 1 and parts[1] else size - 1
        if start >= size:
            self.send_error(http.HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            return None
        end = min(end, size - 1)
        length = end - start + 1
        self.range_length = length
        self.send_response(http.HTTPStatus.PARTIAL_CONTENT)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(length))
        self.end_headers()
        f.seek(start)
        return f

    def copyfile(self, source, outputfile):
        if getattr(self, 'range_length', None) is not None:
            bytes_left = self.range_length
            bufsize = 64 * 1024
            while bytes_left > 0:
                chunk = source.read(min(bufsize, bytes_left))
                if not chunk:
                    break
                try:
                    outputfile.write(chunk)
                except (ConnectionResetError, BrokenPipeError):
                    break
                bytes_left -= len(chunk)
        else:
            try:
                super().copyfile(source, outputfile)
            except (ConnectionResetError, BrokenPipeError):
                pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(RangeHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == '__main__':
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Serving {DIRECTORY} with Range and Multi-threading support at http://localhost:{PORT}")
        httpd.serve_forever()
