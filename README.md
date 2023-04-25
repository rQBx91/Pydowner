# Pydowner: A Multithreaded Terminal Downloader

A simple terminal program writen in Python for downloading files with support for multi-threaded downloading.

## Dependencies

* click
* requests
* tqdm

Install the requirements:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python download.py [FLAGS] URL
```

## Flags

```plaintext
     --threads <int>
         Number of threads to use for download (default: number of cpu cores in the system)

     --name <string>
         Name to use for saving file to the filesystem (default: name of the file in the URL)
```

## Examples

```bash
python download.py https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.1.tar.xz
```

```bash
python download.py --threads 8 https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.1.tar.xz
```

```bash
python download.py --threads 4 --name linux https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.1.tar.xz
```
