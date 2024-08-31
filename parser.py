import sys, pdb, requests, os, hashlib, shutil, zipfile, json

class Result:
    def __init__(self):
        self.result = dict()
        self.result['data'] = list()
    
    def __str__(self):
        y = json.dumps(self,
            default=lambda o: o.__dict__,
            #sort_keys=True,
            indent=4
            )
        return (y)
    
    def addRepository(self, repo):
        self.result.get('data').append(repo)
        
class Repository:
    def __init__(self, url, dockerfile):
        self.repository = url
        self.dockerfile = dockerfile
            
class Dockerfile:
    def __init__(self, path, baseImages):
        self.path = path
        self.baseImages = baseImages
    
result = Result()

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
    if os.path.exists(filename):
        os.remove(filename)
    
  
def parseDownloadedFile(filename):
    print('Parsing downloaded file {filename}')
    file = open(filename)
    for line in file:
        txt = line.split(' ')
        print(txt[0], "->", txt[1])
        print('Going to download git repo', txt[0])
        downloadGitRepository(txt[0], txt[1])
        #break
    file.close()
        
def downloadGitRepository(url, checksum):
    #path = 'temp'
    #if not os.path.exists(path):
    #    os.mkdir(path)
    newUrlForZipDownload = createDownloadZipUrlFromRepoUrl(url)
    print('New url for zip download is, Downloading zipfile ...', newUrlForZipDownload)
    r = requests.get(newUrlForZipDownload, allow_redirects=True)
    #https://github.com/app-sre/container-images.git -> container-images
    filename = url.split('/')[-1:][0].replace('.git','') + '-master.zip'
    #os.chdir(path)
    print(os.getcwd())
    if os.path.exists(filename):
        print('removing file', filename)
        os.remove(filename)
    file = open(filename,'wb')
    file.write(r.content)
    file.close()
    '''if verifyChecksum(filename, checksum) == False:
        print('Error : Checksum can not verified for file : ', filename, ' checksum  = ', checksum)
        return'''
    dockerfilePath, images = openZipFile(filename)
    dfile = Dockerfile(dockerfilePath, images)
    gitRepo = Repository(url, dfile)
    #breakpoint()
    result.addRepository(gitRepo)
    if (os.path.isfile(filename)):
        print('Information found, Removing zip file')
        os.remove(filename)
    print(result)
    #os.chdir('..\\')
    print(os.getcwd())


def openZipFile(filename):
    dockerfilePath = ''
    baseRepos = set()
    stageNames = set()
    #print(os.getcwd())
    print('Open zipfile ', filename)
    imageName = ''
    with zipfile.ZipFile(filename, mode='r') as zp:
        for info in zp.infolist():
            if info.filename.endswith('Dockerfile'):
                dockerfilePath = info.filename
                #print('----> ', info.filename)
                with zp.open(info) as dockerfile:
                    #print(dockerfile.readlines())
                    for line in dockerfile.readlines():
                        line = line.decode('utf-8').replace('\b','').replace('\n','')
                        index = line.lower().find('from')
                        if index == 0:
                            parts = line.split(' ')
                            if len(parts) > 2:
                                print(parts[3][:-1])
                                stageNames.add(parts[3])
                            if parts[1] not in baseRepos and parts[1] not in stageNames:
                                baseRepos.add(parts[1])
                    repositoriesList = list(baseRepos)
                dockerfile.close()
                break
    zp.close()
    print(repositoriesList)
    return dockerfilePath, repositoriesList


def createDownloadZipUrlFromRepoUrl(url):
    parts = url.split('/')[3:-1]
    lastPart = url.split('/')[-1:][0]
    lastPart = lastPart.replace('.git', '')
    joinParts = '/'.join(parts)
    newUrl = 'https://codeload.github.com/' + joinParts
    newUrl = newUrl + '/' + lastPart + '/zip/refs/heads/master'
    return newUrl
    
  # assuming the assignment had put random checksum, which can be verified
def verifyChecksum(filename, checksum):
    print('Verifying file checksum ', filename, '  ', checksum)
    blocksize = 2**20
    h = hashlib.sha1()
    with open(filename, 'rb') as fh:
        while True:
            data = fh.read(blocksize)
            if len(data) == 0:
                break
            else:
                h.update(data)
    fh.close()
    print('Calculated checksum ', h.hexdigest())
    return checksum == h.hexdigest()
                    

def main():
    print("Hello World")
    r = double(2);
    print("Double of 2 is ", r);


if __name__ == "__main__":
	#main()
    #args = sys.argv
    #globals()[args[1]](args[2])    #downloadFileFromWeb("https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt")
    url = os.getenv('REPOSITORY_LIST_URL')
    print(url)
    downloadFileFromWeb(url)

