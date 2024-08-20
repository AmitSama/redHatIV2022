import sys, pdb, requests, os

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

def main():
    print("Hello World")
    r = double(2);
    print("Double of 2 is ", r);

if __name__ == "__main__":
	#main()
    #args = sys.argv
    #globals()[args[1]](args[2])
    downloadFileFromWeb("https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt")