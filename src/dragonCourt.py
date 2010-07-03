'''
Created on Jul 2, 2010

@author: thomas
'''
import httplib2, random,time

def encrypt(inputStr):
    inLen = len(inputStr)
    outStr = ''
    j = 0
    for i in range(0, inLen):
        num = ord(inputStr[i])
        if (num < 32):
            outStr += chr(num)
            continue
 
        num = num - 32
        tmp = (inLen + j) % 96
        num = (num + tmp) % 96
        num = num + 32
        outStr += chr(num)
        j = j + 1
    return outStr

def decrypt(inputStr):
    inLen = len(inputStr)
    outStr = ""
    j = 0
    for i in inputStr:
        if (ord(i) >= 32):
            j += 1
    
    i = inLen - 1
    while(i >= 0):
        num = ord(inputStr[i])
        
        if (num < 32):
            outStr += chr(num)
            i -= 1
            continue

        j -= 1;
        tmp = (inLen + j) % 96;
        num -= 32;
        num -= tmp;
        while (num < 0):
            num += 96

        num += 32;
        outStr += chr(num)
        i -= 1

    outStrRev = ""
    for i in range(0, len(outStr)):
        outStrRev += outStr[len(outStr) - i - 1]
        
    return outStrRev

def int32(x):
    if x > 0xFFFFFFFF:
        x = x & 0xFFFFFFFF
    if x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
        if x < 2147483648:
            return - x
        else:
            return - 2147483648
    return x


def writeToFile(filename,content):
    fh = open(filename, "wb", 0)
    fh.write(content)
    fh.close()
    
def readFile(filename):
    fh = open(filename, "rb", 0)
    data = fh.read()
    fh.close()
    return data


class DCourt:
    
    h = None
    headers = {'content-type':'text/plain'};
    seed = None
    watermarked = None
    body = None
    baseurl = "http://wild.ffiends.com/cgibin/DCcgi19.exe?cfg=DCourt&act="
    
    username = "USERNAME_HERE"
    password = "PASSWORD_HERE"
    
    
    def __init__(self):
        self.h = httplib2.Http()
        self.h.follow_all_redirects = True
        
        self.seed = random.randint(10000, 10000000)
        self.watermark()
        
    def watermark(self):
        self.watermarked = int32(int32(self.seed >> 11) & 0x1fffff) | int32(int32(self.seed << 24) & 0xffe00000);
    
    def cgiFind(self):
        data = self.username+ "|" + self.password + "|" + str(self.seed)
        self.body = encrypt(data);
        print "POST CgiFind: " + data;
        resp, content = self.h.request(self.baseurl + "cgiFind","POST", body=self.body, headers=self.headers)
        print "RECV CgiFind:"
        print resp
        print decrypt(content)
        print ""
    
    def cgiLoad(self):
        data = self.username+ "|" + str(self.watermarked)
        self.body = encrypt(data);
        print "POST cgiLoad: " + data;
        resp, content = self.h.request(self.baseurl + "cgiLoad","POST", body=self.body, headers=self.headers)
        print "RECV cgiLoad:"
        print resp
        writeToFile("cgiLoad",decrypt(content))
        print ""
    
    #run this when you have a modified cgiLoad file ready (filename: cgiSaveIt)
    def cgiSaveIt(self):
        data = self.username+ "|" + str(self.watermarked) + "\n" + readFile("cgiSaveIt")
        self.body = encrypt(data);
        print "POST cgiSaveIt ";
        resp, content = self.h.request(self.baseurl + "cgiSaveIt","POST", body=self.body, headers=self.headers)
        print "RECV cgiSaveIt:"
        print resp
        print decrypt(content)
        print ""

if __name__ == '__main__':  
     dcourt = DCourt()
     dcourt.cgiFind()
     dcourt.cgiLoad() #creates file cgiLoad
     time.sleep(120)
    
     #modify cgiLoad & save it as cgiSaveIt (within 2 minutes)
    
     dcourt.cgiSaveIt() #uploads modified user file (cgiSaveIt)
     
     
