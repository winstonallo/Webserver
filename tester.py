#! /bin/python3

url = 'http://localhost:8080'

# Test 1 send wrong method 
import time
import socket
import os
from time import sleep
test_desc = []
test_input = []
test_output = []

test_desc.append("Test 1 send wrong method")
test_input.append("GOT / HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 405 Method Not Allowed")

test_desc.append("Test 2 send wrong path")
test_input.append("GET /sanoj1 HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 404 Not Found")

test_desc.append("Test 3 send wrong protocol")
test_input.append("GET / HTTP/1.0\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 505 HTTP Version Not Supported")

test_desc.append("Test 4 send wrong host")
test_input.append("GET / HTTP/1.1\r\nHost:notexist.com\r\n\r\n")
test_output.append("HTTP/1.1 404 Not Found")

test_desc.append("Test 5 send path goind out of root")
test_input.append("GET /../../../../../etc/passwd HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 404 Not Found")

test_desc.append("Test 6 send request without host")
test_input.append("GET / HTTP/1.1\r\n\r\n")
test_output.append("HTTP/1.1 400 Bad Request")

test_desc.append("Test 7 send request without path")
test_input.append("GET HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 400 Bad Request")


test_desc.append("Test 9 send POST request without Content-Length or Transfer-Encoding")
test_input.append("POST / HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 411 Length Required")

test_desc.append("Test 10 send POST request with Content-Length 0")
test_input.append("POST /file HTTP/1.1\r\nHost:domain1.com\r\nContent-Length: 0\r\n\r\n")
test_output.append("HTTP/1.1 200 OK")

test_desc.append("Test 11 send POST request with Content-Length  and Transfer-Encoding")
test_input.append("POST /file HTTP/1.1\r\nHost:domain1.com\r\nContEnt-Length: 10\r\nTransfer-Encoding: chunked\r\n\r\n")
test_output.append("HTTP/1.1 400 Bad Request")

test_desc.append("Test 12 send request with too long uri")
test_input.append("GET /" + "a" * 2000 + " HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 414 URI Too Long")

test_desc.append("Test 13 send request with too long header")
test_input.append("GET / HTTP/1.1\r\nHost:domain1.com" + "a" * 6000  + "\r\n\r\n")
test_output.append("HTTP/1.1 431 Request Header Fields Too Large")

test_desc.append("Test 15 send request with wrong header syntax")
test_input.append("GET / HTTP/1.1\r\nHost:domain1.com\r\nwrong\theader: 1\r\n\r\n")
test_output.append("HTTP/1.1 400 Bad Request")

test_desc.append("Test 16 send a valid get request")
test_input.append("GET / HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 200 OK")

test_desc.append("Test 17 send a delete request")
test_input.append("DELETE /file HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
test_output.append("HTTP/1.1 200 OK")

test_desc.append("Test 18 send a request with special prcnt sign in uri")
test_input.append("PUT /file%20with%20spaces HTTP/1.1\r\nHost:domain1.com\r\nContent-Length: 5\r\n\r\n lobok")
test_output.append("HTTP/1.1 200 OK")


host = "domain1.com"
url = 'http://localhost:8080'
ip = "localhost"
port = 8080

def send_string_to_ip( string):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(string.encode())
        response = s.recv(10240)
        s.close()
        return response.decode()

def test_timeout(string):
    print('\033[93m' + "Timeout test" '\033[0m')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(string.encode())
        response = s.recv(10240)
        s.close()
        try:
            assert "HTTP/1.1 408 Request Timeout" in response.decode()
            print('\033[92m' + 'Test Passed\n' + '\033[0m')
        except AssertionError:
            print('\033[91m' + 'Test Failed' + '\033[0m')
            print('Expected:', "HTTP/1.1 408 Request Timeout")
            print('Got:', response)

def test_errcodes():
    for i in range(len(test_desc)):
        print('\033[93m' + test_desc[i] + '\033[0m')
        response = send_string_to_ip(test_input[i])
        print('Response from server:', response.split('\r\n')[0])
        try:
            assert test_output[i] in response
            print('\033[92m' + 'Test Passed\n' + '\033[0m')
        except AssertionError:
            print('\033[91m' + 'Test Failed' + '\033[0m')
            print('Expected:', test_output[i])
            print('Got:', response)
            if response == "":
                #make red
                print('\033[91m' +"Server did not respond - probably crashed" + '\033[0m')
                #turn on the server again
                exit(1)

if __name__ == "__main__":
    test_timeout("PUT /file1 HTTP/1.1\r\nHost:domain1.com\r\nContent-Length: 1000\r\n\r\n")
    test_timeout("PUT /file1 HTTP/1.1\r\nHost:domain1.com\r\nTransfer-encoding: chunked\r\n\r\n")
    test_timeout("GET /cgi-bin/loop.py HTTP/1.1\r\nHost:domain1.com\r\n\r\n")
    test_timeout("GET / HTTP/1.1\r\nHost:domain1.com\r\n")
    while True:
        test_errcodes()