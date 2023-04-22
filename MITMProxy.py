import json #Module to work with JSON data.
from pathlib import Path #Module to work with file paths.
import asyncio #Module to work with asynchronous code.
from mitmproxy.tools.web import master as WebMaster #Module to work with the web interface.
from mitmproxy import options #Module to work with the proxy server options.
from mitmproxy.tools import dump #Module to work with the proxy server.


listenHost = input("Enter host: ex.192.168.1.1\n ")
listenPort = input("Enter port: ex.8080\n ")


# This custom class will be used to intercept the requests and responses.
class InterceptAddon:
    # Initialize the class and set empty list for intercepted requests.
    def __init__(self):
        self.intercepted_requests = []
    
    # This method will be called when a request is intercepted.    
    def response(self, flow):
        # Set the file name and path to save the intercepted requests.
        file_name = "intercepted_requests.json"
        output_path = Path.cwd() / file_name
        
        # Get the request and response objects.
        request = flow.request
        response = flow.response
        
        # Create a dictionary with the request and response data.
        intercepted_data = {
            "host": request.host,
            "url": request.url,
            "http_type": request.scheme,
            "query_params": dict(request.query.items()),
            "response_data": response.text
        }
        
        # Check if the request is HTTP or HTTPS.
        if request.scheme == "https" or request.scheme == "http":
            self.intercepted_requests.append(intercepted_data)
            with output_path.open("w") as f:
                json.dump(self.intercepted_requests, f, indent=2)
            print(f"Saving request to {output_path}")
        

# Function used to run the proxy server.
async def run_proxy_server(listenHost=listenHost, listenPort=listenPort):
    # Create the options for the proxy server.
    opts = options.Options(listen_host=listenHost, listen_port=int(listenPort))

    print(f"Starting proxy server on port {listenPort}")
    
    # Create instance with the specified options
    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    
    # Add the options to the proxy server instance.
    master.addons.add(InterceptAddon())
    
    # Start the proxy server.
    await master.run()
    return master

# Checks to make sure script is being run as main.
if __name__ == "__main__":
    # Run the proxy server.
    asyncio.run(run_proxy_server())