class HttpParserException(Exception):
    pass


class HttpParser:
    def __init__(self):
        self.req = {}

    def parse_req(self, http_data: bytes):
        try:
            remaining = self.parse_start_line(http_data)
            body = self.parse_headers(remaining)
            self.parse_body(body)
        except Exception as e:
            raise HttpParserException(e)

    def parse_start_line(self, http_data: bytes):
        start_line, remaining = http_data.split(b"\r\n", 1)
        method, path, http_version = start_line.split(b" ")
        request_type, version = http_version.split(b"/")
        self.req["method"] = method
        self.req["path"] = path
        self.req["type"] = request_type
        self.req["http_version"] = version
        return remaining

    def parse_headers(self, remaining: bytes):
        *headers, body = remaining.split(b"\r\n")
        formatted_headers = []
        for header in headers:
            if not header:
                continue
            key, val = header.split(b":", 1)
            formatted_headers.append((key, val.strip()))
        self.req["headers"] = formatted_headers
        return body

    def parse_body(self, body: bytes):
        self.req["body"] = body

    def serialize_http_response(self, asgi_responses):
        http_response = b""
        headers = {}

        for response in asgi_responses:
            response_type = response.get("type")

            if response_type == "http.response.start":
                status_code = response.get("status", 200)
                http_response += f"HTTP/1.1 {status_code} OK\r\n".encode()

                for header in response.get("headers", []):
                    key, value = header
                    headers[key] = value

            elif response_type == "http.response.body":
                http_response += b"\r\n".join(
                    [
                        f"{key.decode()}: {value.decode()}".encode()
                        for key, value in headers.items()
                    ]
                )
                http_response += b"\r\n\r\n" + response.get("body", b"")

        return http_response
