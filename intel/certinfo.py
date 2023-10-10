# Author github.com/n0mi1k
# A python script to extract certificate data from an endpoint
# python3 certinfo.py -e "www.google.com, www.apple.com, censys.io"
# Tool currently returns a list containing dictionaries of endpoint outputs
# Ideally, results can be fed to other APIs such as Censys, Shodan, etc.
# Requires pip install pyOpenSSL

import socket
import ssl
import OpenSSL.crypto as crypto
import datetime
import argparse

def getCertInfo(endpoint):
    certInfo = {}

    dst = (endpoint, 443)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5) # Set 5s timeout for unreachable hosts

    try:
        s.connect(dst)
    except TimeoutError:
        return None

    # Upgrade the socket to SSL (Try, Except to detect non SSL sites and handshake errors)
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=dst[0])
    except:
        return None

    # Obtaining certificate
    cert_bin = s.getpeercert(True)
    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert_bin)

    CommonName = x509.get_subject().CN

    if x509.get_subject().C != None:
        CountryState = x509.get_subject().C
        if x509.get_subject().ST != None:
            CountryState = CountryState + " " + x509.get_subject().ST
    else:
        CountryState = "Not part of certificate"
    
    if x509.get_subject().O:
        Organisation = x509.get_subject().O
    else:
        Organisation = "Not part of certificate"

    ValidFrom = datetime.datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%S%fZ').strftime("%b %d %H:%M:%S %Y GMT")
    ValidTo = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%S%fZ').strftime("%b %d %H:%M:%S %Y GMT")
    Issuer = x509.get_issuer().CN
    ExpiryStatus = x509.has_expired()

    certInfo = {
        "Endpoint" : endpoint,
        "Common Name" : CommonName,
        "Country State" : CountryState,
        "Organisation" : Organisation,
        "Valid From" : ValidFrom,
        "Valid To" : ValidTo,
        "Issuer" : Issuer,
        "Has Expired" : ExpiryStatus 
    }

    # Close socket when done
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return certInfo


def main():
    parser = argparse.ArgumentParser(prog='certinfo.py', 
                                    description='A tool to grab certificate information of endpoints.',
                                    usage='%(prog)s -e ENDPOINTS')

    parser.add_argument("-e", "--endpoints", help="endpoints to scan separated by commas", required=True)
    parser.add_argument("-p", "--print", default=False, action=argparse.BooleanOptionalAction) # If set, it will print result
    args = parser.parse_args()

    endpoints = args.endpoints.split(",")

    certData = [] # List containing dict of endpoints

    for endpoint in endpoints:
        if 'http://' in endpoint:
            endpoint = endpoint.replace("http://", "")
        elif 'https://' in endpoint:
            endpoint = endpoint.replace("https://", "")

        certResult = getCertInfo(endpoint.strip())
        if certResult: # Append only positive results
            certData.append(certResult)
        else:
            print(f"Error: {endpoint} timeout or not an SSL endpoint!")
    
    if args.print: 
        for cert in certData:
            print(f"\n--Certificate Info for {cert['Endpoint']}--")
            for params, value in cert.items():
                print(f"{params} : {value}")  

    # The results are saved into certData dict, ready to implement on other tools
    # print(certData)

if __name__ == '__main__':
    main()