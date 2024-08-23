import sys, pdb, requests, os, hashlib, shutil, zipfile

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
    file = open(filename, 'wb')
    file.write(r.content)
    file.close()
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
    file.close()
        
def downloadGitRepository(url):
    path = 'temp'
    if not os.path.exists(path):
        os.mkdir(path)
    newUrlForZipDownload = createDownloadZipUrlFromRepoUrl(url)
    print('New url for zip download is ', newUrlForZipDownload)
    r = requests.get(newUrlForZipDownload, allow_redirects=True)
    #https://github.com/app-sre/container-images.git -> container-images
    filename = url.split('/')[-1:][0].replace('.git','') + '-master.zip'
    os.chdir(path)
    print(os.getcwd())
    if os.path.exists(filename):
        print('removing file', filename)
        os.remove(filename)
    file = open(filename,'wb')
    file.write(r.content)
    file.close()
    os.chdir('..\\')
    print(os.getcwd())
    image = openZipFile(filename, path)

def openZipFile(filename, dirname):
    os.chdir(dirname)
    print(os.getcwd())
    print('Open zipfile ', filename)
    imageName = ''
    with zipfile.ZipFile(filename, mode='r') as zp:
        for info in zp.infolist():
            if info.filename.endswith('Dockerfile'):
                print('----> ', info.filename)
                #dockerFileName = 'docker_' + filename + '_' + info.filename
                #file = open(dockerFileName, 'wt')
                with zp.open(info) as dockerfile:
                    #print(dockerfile.readlines())
                    for line in dockerfile.readlines():
                        line = line.decode('utf-8')
                        index = line.lower().find('from')
                        #breakpoint()
                        if index >= 0:
                            parts = line.split(' ')
                            imageName = parts[1]
                            print(parts[1])
                            break
                    '''#
                        #if line[0].strip().startswith('From'):
                        print(line.decode('utf-8').replace('\\b', ''))
                        print('\\n')
                        print('\\n')
                    #'''
                dockerfile.close()
    zp.close()
    return imageName


def createDownloadZipUrlFromRepoUrl(url):
    parts = url.split('/')[3:-1]
    lastPart = url.split('/')[-1:][0]
    lastPart = lastPart.replace('.git', '')
    joinParts = '/'.join(parts)
    newUrl = 'https://codeload.github.com/' + joinParts
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
    fh.close()
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