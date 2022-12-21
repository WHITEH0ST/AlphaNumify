import argparse, uuid, os, sys

def formatter(file):
    'Adds +1 In Front of your leads'
    filename = str(uuid.uuid4()) + ".txt"
    list_file = open(file, "r")
    new_file = open(filename, "a+")
    num_lst = [line.strip() for line in list_file]
    for line in num_lst:
        if not line.startswith('+1'):
            new_file.write("+1" + line + "\n")
    new_file.close()

def proxy_fmt(file):
    'Adds HTTP, SOCKS4, SOCK5 In Front of your PROXIES'
    prename = input("New File Name [Press enter for Default]:     ")
    filename = str(uuid.uuid4()) + ".txt" if prename == "" else prename
    proxy_type = input("Proxy type [HTTP, SOCKS4, SOCKS5]:  ").lower()
    list_file = open(file, "r")
    new_file = open(filename, "a+")
    num_lst = [line.strip() for line in list_file]
    for line in num_lst:
        new_file.write(f"{proxy_type}|" + line + "\n")
    new_file.close()

def whitespace_remover(file):
    prename = input("New File Name [Press enter for Default]:     ")
    filename = str(uuid.uuid4()) + ".txt" if prename == "" else prename
    list_file = [x.strip() for x in open(file).readlines() if x.strip()]
    with open(filename, "w") as handler:
        [handler.write("{}\n".format(str(x))) for x in list_file]
        handler.close()
    

    sys.stdout.write("Your File: {}".format(os.path.abspath(".") + '\\' + filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--formatter" , help="Launches the formatter application", action='store_true')
    parser.add_argument("-t", "--file" , help="File to format", action="store", type=str)
    parser.add_argument("-pf", "--proxyformat" , help="Launches the formatter application", action='store_true')
    parser.add_argument("-wr", "--whitespace-remover" , help="Launches the Whitespace remover application", action="store_true")
    args = parser.parse_args()

    if args.formatter:
        formatter(args.file)

    elif args.proxyformat:
        proxy_fmt(args.file)
    
    elif args.whitespace_remover:
        whitespace_remover(args.file)
