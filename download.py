
import click
import requests
import threading
import os
from sys import platform
from tqdm import tqdm
from hashlib import sha256
import time

scriptPath = os.getcwd()

def clear_screen():
    if platform == "win64" or platform == "win32":    
        os.system('cls')
    if platform == "linux" or platform == "linux2":
        os.system('clear')
        
def Handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)} 
    r = requests.get(url, headers=headers, stream=True)
    totalSize = end - start
    with open(filename, "r+b") as fp, tqdm(
        desc=f'Downloading from {start} to {end}',
        total=totalSize,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        header = start
        for data in r.iter_content(chunk_size=1024):
            fp.seek(header)
            size = fp.write(data)
            bar.update(size)
            header = fp.tell()
        bar.close()
        clear_screen()
        
@click.command(help="Downloads the file located by the URL and saves it with the specified name.")
@click.option('--threads',default=os.cpu_count(), help="Number of Threads")
@click.option('--name',type=click.Path(),help="Name of the file with extension")
@click.argument('file_url',type=click.Path())
@click.pass_context
def download_file(ctx,file_url,name,threads):
    stime = time.time()
    
    req = requests.head(file_url)
    if name:
        file_name = f'{scriptPath}/{name}'
    else:
        temp = file_url.split('/')[-1]
        file_name = f'{scriptPath}/{temp}' 
    try:
        file_size = int(req.headers['content-length'])
    except:
        print ("Invalid URL")
        return 
    
    part = file_size // threads
    fp = open(file_name, "wb")
    fp.truncate(file_size)
    fp.close()
    
    threadList = []
    for i in range(threads):
        start = part * i
        end = start + part
        if i == (threads - 1):
            end = file_size
        t = threading.Thread(target=Handler,
             kwargs={'start': start, 'end': end, 'url': file_url, 'filename': file_name, })
        t.daemon = True
        threadList.append(t)
    
    clear_screen()
    
    for thread in threadList:
        thread.start()
        time.sleep(0.1)
        
    for thread in threadList:
        thread.join()
    
    clear_screen()    
        
    print('Download Completed.\n')
    hash = ''
    with open(file_name, 'rb') as file:
        bytes = file.read()
        hash = sha256(bytes).hexdigest()
    print(f'SHA256 hash of {file_name}:\n{hash.upper()}')
    
    print("\nscript execution time: {0}\n".format(time.time() - stime))

    
if __name__ == '__main__':
    download_file(obj={})
    
