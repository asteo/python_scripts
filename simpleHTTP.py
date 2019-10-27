from http.server import BaseHTTPRequestHandler, HTTPServer
import json
#import psutil
html = '''<html>
              <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                 .button_led {display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
              </style>
              <script type="text/javascript" charset="utf-8">
                    function httpPostAsync(method, params, callback) {
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.onreadystatechange = function() { 
                            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                                callback(xmlHttp.responseText);
                            else
                                callback(`Error ${xmlHttp.status}`)
                        }
                        xmlHttp.open("POST", window.location.href + method, true);
                        xmlHttp.setRequestHeader("Content-Type", "application/json");
                        xmlHttp.send(params);
                    }

                    function ledOn() {
                        document.getElementById("textstatus").textContent = "Making LED on...";
                        httpPostAsync("led", JSON.stringify({ "on": true }), function(resp) { 
                            document.getElementById("textstatus").textContent = `Led ON: ${resp}`;
                        });
                    }

                    function ledOff() {
                        document.getElementById("textstatus").textContent = "Making LED off...";
                        httpPostAsync("led", JSON.stringify({ "on": false }), function(resp) { 
                            document.getElementById("textstatus").textContent = `Led OFF: ${resp}`;
                        });
                    }                            
              </script>
              <body>
                 <h2>Hello from the Raspberry Pi!</h2>
                 <p><button class="button button_led" onclick="ledOn();">Led ON</button></p>
                 <p><button class="button button_led" onclick="ledOff();">Led OFF</button></p>
                 <span id="textstatus">Status: Ready</span>
              </body>
            </html>'''


# def cpu_temperature():
#     return psutil.sensors_temperatures(fahrenheit=False)

# def disk_space():
#     st = psutil.disk_usage(".")
#     return st.free, st.total

# def cpu_load():
#     return int(psutil.cpu_percent())

# def ram_usage():
#     return int(psutil.virtual_memory().percent)

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, path:", self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            health = {'CPUTemp': cpu_temperature(), 'CPULoad': cpu_load(), "DiskFree": disk_space()[0], "DiskTotal": disk_space()[1], "RAMUse": ram_usage()}
            self.wfile.write(json.dumps(health).encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            print("POST request, path:", self.path, "body:", body.decode('utf-8'))
            if self.path == "/led":
                data_dict = json.loads(body.decode('utf-8'))
                if 'on' in data_dict:
                    print("rasperrypi_pinout(led_pin, On)")
                else:
                    print("rasperrypi_pinout(led_pin, OFF)")
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(400, 'Bad Request: Method does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        except Exception as err:
            print("do_POST exception: %s" % str(err))

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':

    port = 8000
    print("Starting server at port %d" % port)

    # raspberrypi_init()

    server_thread(port)

    # rasperrypi_cleanup()