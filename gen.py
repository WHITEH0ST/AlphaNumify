import cython, os, sys, time, random, json, uuid, argparse, pyfiglet
from tqdm import tqdm
from datetime import datetime

carrier_dict = {
    "1": "at&t,bellsouth,cingular,comcast",
    "2": "verizon",
    "3": "t-mobile",
    "4": "sprint",
    "5": "metropcs",
    "6": "pacific",
    "7": "cingular",
}


@cython.cfunc
def _generator(number: cython.int,
               area_codes: str,
               carriers=None,
               landline=None,
               append_email: bool = None,
               output:bool=False):
    global carrier_dict
    final = []
    name = str(uuid.uuid4()) + ".txt"
    saved_file = os.path.join(os.path.abspath("."), "leads\\")
    area_codes_list = area_codes.split(",")
    carriers_list = carriers.split(",")

    if landline:
        db_filter = [
            x.strip() for x in open('./config/config.ini').readlines()
                if x.split(",")[0] in area_codes_list and 
                any(
                    item in x.split(",")[3].lower().split(" ") for item in [l for x in [
                        i for i in [
                            carrier_dict[k].split(",") for k in carriers_list
                        ]
                    ] for l in x]
                    
            )
        ]

    else:
        db_filter = [
            x.strip() for x in open('./config/config.ini').readlines()
                if x.split(",")[0] in area_codes_list and 
                any(
                    item in x.split(",")[3].lower().split(" ") for item in [l for x in [
                        i for i in [
                            carrier_dict[k].split(",") for k in carriers_list
                        ]
                    ] for l in x]
                    
            ) and x.split(',')[2].lower() != 'landline'
        ]

    if db_filter == []:
        print(
            "\n\nNo data was found in our db for that Area code(s).\nPlease use --no-syntax flag."
        )
        exit(0)

    else:
        with open("config/prefixer.json") as prefixr:
            data = json.load(prefixr)
            pbar = tqdm(total=int(number), desc="Generating Leads")

            while int(number) != len(final):
                cur = random.choice(db_filter).split(",")
                key_list = [k for k, v in data.items()]
                st_key = [
                    k for k in key_list if k in cur[3].lower().split(" ")
                ]

                diq = "+1" + cur[0] + cur[1] + "".join([
                    "{}".format(random.randint(0, 9)) for num in range(0, 4)
                ]) if not append_email else "+1" + cur[0] + cur[1] + "".join(
                    ["{}".format(random.randint(0, 9))
                     for num in range(0, 4)]) + data[st_key]
                if diq not in final:
                    final += [diq]
                    if output:
                        print(diq)
                    pbar.update(1)

            pbar.close()

        with open(saved_file + name, "a+") as cso:
            for line in list(set(final)):
                cso.write(line + "\n")
            cso.close()

    tqdm.write(f"Your File is saved in:  {saved_file + name}")


@cython.cfunc
def gen_no_syntax(count: cython.int,
                  areacodes = None,
                  exchanges: bool = None,
                  output: bool = None):

    number: str
    filename: str
    generated: list
    n: str
    filename = "Instance-" + (str(
        str(str(datetime.now()).replace(
            " ",
            "",
        )).replace(".", "-")).replace(":", "-")) + ".txt"

    if areacodes is not None:
        area_codes = areacodes.split(",") if areacodes is not None else input(
            "Area Codes [Seperated by commas]: ").split(",")
    # exchanges =  exchanges.split(",") if exchanges else input("Exchanges (Seperated by commas): ").split(",")
    if exchanges is not None:
        exchanges = [x.strip().split("-") for x in open(exchanges).readlines()]
    else:
        exchanges = None

    generated = []
    pbar = tqdm(total=int(count), desc="Generating Leads")

    if exchanges is None:
        while count != len(generated):
            number = "+1" + str(random.choice(area_codes)) + ''.join(
                    ["{}".format(random.randint(0, 9)) for num in range(0, 7)])
            if number not in generated:
                generated += [number]
                if output:
                    tqdm.write(number)
                pbar.update(1)

    else:
        if isinstance(exchanges[0], list):
            while count != len(generated):
                number = "+1" + str(random.choice(exchanges)[0]) + str(
                    random.choice(exchanges)[1]) + ''.join(
                        ["{}".format(random.randint(0, 9)) for num in range(0, 4)])
                if number not in generated:
                    generated += [number]
                    if output:
                        tqdm.write(number)
                    pbar.update(1)
    pbar.close()

    with open(f"no_syntax/{filename}", "a+") as writer:
        for n in list(set(generated)):
            writer.write(n + "\n")
        writer.close()

    tqdm.write(
        f"Your File is saved in:  {str(os.path.abspath(f'./no_syntax/{filename}'))}"
    )

logo = lambda: pyfiglet.Figlet(font=random.choice(
        [l for l in pyfiglet.FigletFont.getFonts() if l.endswith("7000")]),
                        direction="center",
                        justify="center",
                        width=100).renderText("\t\tGEN.PY BY HIGH PROGRAMMER")
clear = lambda: os.system("cls" if sys.platform != 'linux' else 'clear')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="THP Generator V2.2 - Added No syntax")
    clear()
    tqdm.write(logo())
    parser.add_argument(
        "-p",
        "--prefix",
        help="Appends SMTP2SMS Extension e.g number@tmomail.net",
        action='store_true')
    parser.add_argument("-nxx",
                        "--exchanges",
                        help="Exchanges [Carrier Code]",
                        action='store',
                        default=None)
    parser.add_argument("-l",
                        "--include-landlines",
                        help="Formats numbers ignoring landline flag",
                        action='store_true')
    parser.add_argument("-o",
                        "--display-generated",
                        help="Display generated numbers on stdin",
                        action='store_true')
    parser.add_argument(
        "-N",
        "--no-syntax",
        help="Random Generation, No form of validation is applied",
        action='store_true')
    parser.add_argument("-a",
                        "--areacodes",
                        help="Area Codes to Be generated",
                        action="store",
                        type=str,
                        default=None)
    parser.add_argument("-c",
                        "--count",
                        help="How many Leads to be generated",
                        action="store",
                        type=int,
                        required=True)
    parser.add_argument(
        "-s",
        "--carriers",
        help=
        "Generate For specific carriers:\n1. AT&T\n2. Verizon\n3. T-Mobile\n4. Sprint\n5. Metro PCS",
        action="store",
        type=str)
    args = parser.parse_args()

    os.system("pip install -r requirements.txt")
    
    colors: list = [36, 32, 34, 35, 31, 37]

    n, y = os.path.abspath(".") + "\\leads\\", os.path.abspath(
        ".") + "\\no_syntax\\"
    if not os.path.isdir(n):
        os.mkdir(n)
    if not os.path.isdir(y):
        os.mkdir(y)

    os.system('title Welcome to THP GENERATOR ★')
    clear()
    tqdm.write(logo())
    tqdm.write("\t\t\t\t\tFOR U.S.A ONLY!")
    x = '\t\t\tPowered by:\t https://t.me/thehighprogrammernetwork'

    for N, line in enumerate(x.split('\n')):
        sys.stdout.write("\t")
        for i in line:
            sys.stdout.write('\x1b[1;%dm%s' % (random.choice(colors), i))
            time.sleep(0.05)
        print()

    if args.no_syntax:
        if args.areacodes is None and args.exchanges is None:
            sys.stdout.write("ERROR: You must specify Area codes you wish to generate or pass in a file containing Exchanges (NXX) for each area code.")
            exit(0)

        gen_no_syntax(count=args.count,
                      areacodes=args.areacodes,
                      exchanges=args.exchanges,
                      output=args.display_generated)
    else:
        if args.areacodes is not None:
            _generator(args.count,
                    area_codes=args.areacodes,
                    append_email=args.prefix,
                    carriers=args.carriers,
                    landline=args.include_landlines,
                    output=args.display_generated)
        else:
            raise TypeError('Cannot get area code, Please pass a list of area codes with the comma sep(",") eg. 214, 312, 667')
