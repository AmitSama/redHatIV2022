import sys, pdb, requests

def double(x):
    x = int(x)
    r = x * 2;
    #breakpoint()
    print('Double of ', x , 'is ', r);

def downloadFileFromWeb(url):
    r = requests.get(url, allow_redirects=True)
    open('gitreposts.txt', 'wb').write(r.content) 
    

def main():
    print("Hello World")
    r = double(2);
    print("Double of 2 is ", r);

if __name__ == "__main__":
	#main()
    #args = sys.argv
    #globals()[args[1]](args[2])
    downloadFileFromWeb("https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt")