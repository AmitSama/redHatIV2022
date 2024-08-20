import sys, pdb, requests, os, hashlib, shutil
import urllib.request

def double(x):
    x = int(x)
    r = x * 2;
    #breakpoint()
    print('Double of ', x , 'is ', r);

def downloadFileFromWeb(url):
    filename = 'gitreposts.txt'
    r = requests.get(url, allow_redirects=True)
    if os.path.exists(filename):
        print('Deleting existing file {filename}')
        os.remove(filename)
    open(filename, 'wb').write(r.content)
    parseDownloadedFile(filename)
  
def parseDownloadedFile(filename):
    print('Parsing downloaded file {filename}')
    file = open(filename)
    for line in file:
        txt = line.split(' ')
        print(txt[0], "->", txt[1])
        print('Going to download git repo', txt[0])
        downloadGitRepository(txt[0])
        break
        
def downloadGitRepository(url):
    path = '.\\temp\\'
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
    newUrlForZipDownload = createDownloadZipUrlFromRepoUrl(url)
    print('New url for zip download is ', newUrlForZipDownload)
    r = requests.get(newUrlForZipDownload, allow_redirects=True)
    #breakpoint()
    filename = url.split('/')[-1:][0] + '-master.zip' # https://github.com/app-sre/container-images.git -> container-images
    completeFilePath = os.path.join(path, filename)
    #os.makedirs(completeFilePath)
    open(completeFilePath,'wb').write(r.content)
    
def createDownloadZipUrlFromRepoUrl(url):
    parts = url.split('/')[3:-1]
    lastPart = url.split('/')[-1:][0]
    lastPart = lastPart.replace('.git', '')
    joinParts = '/'.join(parts)
    newUrl = 'https://codeload.github.com/' + joinParts
    #breakpoint()
    #newUrl = newUrl.join(parts)
    newUrl = newUrl + '/' + lastPart + '/zip/refs/heads/master'
    return newUrl
    
  
def verifyChecksum(filename, checksum):
    hash = hashlib.sha256()
    with open(filename, 'rt') as fh:
        while True:
            data = fh.read(4096)
            if len(data) == 0:
                break
            else:
                h.update(data)
    return checksum == h.hexdigest()
                    

def main():
    print("Hello World")
    r = double(2);
    print("Double of 2 is ", r);

if __name__ == "__main__":
	#main()
    #args = sys.argv
    #globals()[args[1]](args[2])
    downloadFileFromWeb("https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt")