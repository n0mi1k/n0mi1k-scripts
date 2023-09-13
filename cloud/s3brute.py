# Author github.com/n0mi1k
import requests
import argparse
import dns.resolver

"""
S3 Naming: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html

Run with python3 s3brute.py -w wordlist.txt -n <PREFIX> (Only existing buckets are printed)

Use prepend character to prepend characters like - or . before your words in the wordlist.
E.g when using -p "-" flag, before prepend: mys3bucketword, after prepend: mys3bucket-word 

Currently suffix bruteforce depth is only 1, might experiment with multi depth in the future
"""

"""
Checks S3 existence using HTTP (May get rate limited) *Call this func if you wish to use HTTP method
"""
def checkBucketHTTP(bucketName):
    r = requests.head(f"https://{bucketName}.s3.amazonaws.com")
    if r.status_code == 200 or r.status_code == 403:
        print(f"[+] Found bucket via HTTP: {bucketName}")
    else:
        print(f"[-] Bucket not found via HTTP: {bucketName}")


"""
Check S3 existence using DNS (Faster and quieter)
"""
def checkBucketDNS(bucketName):
    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(f"{bucketName}.s3.amazonaws.com",'CNAME')
        for answer in answers:
            if "s3-1-w.amazonaws.com" not in str(answer):
                print(bucketName)
                return True
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(prog='s3brute.py', 
                                    description='An S3 bucket brute force tool focusing on suffix brute force',
                                    usage='%(prog)s -s SUFFIXLIST -n NAME -p PREPEND')

    parser.add_argument("-w", "--wordlist", help="Wordlist file containing suffixes", required=True)
    parser.add_argument("-n", "--name", help="Bucket prefix", required=True)
    parser.add_argument("-p", "--prepend", help="Optional prepend character before each word e.g - or .", required=False)

    args = parser.parse_args()

    suffixFile = args.wordlist
    name = args.name
    prepend = args.prepend

    anyFound = False

    with open (suffixFile, 'r') as f:
        suffixList = [line.strip() for line in f]
    
    for suffix in suffixList:
        if prepend:
            bucketName = name + prepend + suffix
        else:
            bucketName = name + suffix

        if checkBucketDNS(bucketName):
            anyFound = True

    if not anyFound:
        print("[+] No buckets found, use prepend character - or .")
        

if __name__ == "__main__":
    main()