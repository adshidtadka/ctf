import urllib
import hashlib
import urllib.error
import urllib.request

url = 'http://ksnctf.sweetduet.info:10080/~q9/flag.html'

#md5 = hashlib.md5()
username = "q9"
realm = "secret"
nonce = ""
uri = "/~q9/flag.html"
algorithm = "MD5"
response = ""
qop = "auth"
nc = "00000001"
cnonce = "9691c249745d94fc"
md5a1 = "c627e19450db746b739f41b64097d449"
a2 = 'GET:' + uri

def getNonce():
	try:
		data = urllib.request.urlopen(url)
		html = data.read()
	except urllib.error.HTTPError as e:
		nonce = e.info()['WWW-Authenticate'].split('"')[3]
		return nonce

def genMD5(str):
	m = hashlib.md5()
	bstr = str.encode()
	m.update(bstr)
	return m.hexdigest()

def genResponse(nonce):
	response = genMD5(md5a1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + genMD5(a2))
	return response


def genAuthorized(nonce, response):
	authorized = 'Digest username="' + username + '", realm="' + realm + '", nonce="' + nonce + '",uri="' + uri + '", algorithm=' + algorithm + ', response="' + response + '", qop=' + qop + ', nc=' + nc + ', cnonce="' + cnonce + '"'
	return authorized



def main():
	nonce = getNonce()
	response = genResponse(nonce)
	auth = genAuthorized(nonce, response)
	header = {'Authorization' : auth}
	req = urllib.request.Request(url, None, header)
	try:
		data = urllib.request.urlopen(req)
		html = data.read()
		print(html)
	except urllib.error.HTTPError as e:
		print(e.code)
		print(e.info())

if __name__ == '__main__':
	main()
