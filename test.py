area_codes_list = '662'
carrier_dict = {
    "1": "at&t,bellsouth,cingular",
    "2": "verizon",
    "3": "t-mobile",
    "4": "sprint",
    "5": "metropcs",
    "6": "pacific",
    "7": "cingular",
}
carriers_list = '1'

db_filter = [
            x.strip() for x in open('./config/config.ini').readlines()
            if x.split(",")[0] in area_codes_list
            and any(
                item in x.split(",")[3].lower().split(" ") for item in [
                    carrier_dict[k]
                    for k in carriers_list
                ])
]

db_filter1 = [
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

filer = [ 
    x.strip() for x in open('./config/config.ini').readlines() if any(
                item in x.split(",")[3].lower().split(" ") for item in [
                    carrier_dict[k]
                    for k in carriers_list
                ])
]


print(db_filter1)
# print(db_filter)