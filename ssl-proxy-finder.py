import requests
from bs4 import BeautifulSoup
import socket, time


def getProxies():
    url = 'http://free-proxy-list.net'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application',
        'Connection': 'Close'
    }
    try:
        result = requests.get(url, headers=headers)
        content = BeautifulSoup(result.content, 'html.parser')
        table = content.find('tbody')
        rows = table.find_all('tr')
        cols = [[col.text for col in row.find_all('td')] for row in rows]
        proxies = []
        for col in cols:
            proxies.append(col[0] + ':' + col[1] + '-' + col[3])
        return proxies
    except Exception as e:
        print('Error:', e)
        exit(1)

def checkproxy(proxylist):
    dsthost = 'httpbin.org'
    proxy_index = 0
    req = f"CONNECT {dsthost}:443 HTTP/1.0\r\nHost: {dsthost}\r\n\r\n".encode()
    print(len(proxylist), 'proxies to check')
    while proxy_index < len(proxylist):
            proxy = proxylist[proxy_index].split('-')
            print('Checking proxy:', proxylist[proxy_index], end='-> ', flush=True)
            res = createsocket(proxy[0].split(':'), req)
            checkresult(res[0], res[1])
            proxy_index += 1

def createsocket(proxy, req) -> tuple:
    proxyaddr = proxy[0]
    port = proxy[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    start = time.time()
    try:
        sock.connect((proxyaddr, int(port)))
        sock.send((req))
        response = sock.recv(4096).decode().split('\r').pop(0)
        sock.close()
    except socket.error as err:
        response = f'Error: -1 {str(err)}'
    end = time.time()
    elptime = end - start
    return response, elptime

def checkresult(response, elptime):
    try:
        headers = response.split(' ')
        status = headers[1]
        if status == '200':
            if elptime < 3:
                print('Is ast!')
            else:
                print('Is Good!')
        elif status == '400':
                print('Non-SSL Proxy')
        elif status =='-1':
            del headers[1:2]
            err =' '.join(headers)
            print(err)
        else:
                print('Might Work')
    except IndexError:
            print('Empty Response')

def main():
    try:
        prxlist = getProxies()
        checkproxy(prxlist)
    except KeyboardInterrupt:
        print('\nInterrupted!')
    
if __name__ == '__main__':
    main()
