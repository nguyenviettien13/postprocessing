# encoding: utf-8
# Read numb
import datetime
import json
import re
from random import random, shuffle, randrange

# from concurrent.futures import ProcessPoolExecutor

dict_digit = {
    "0": "không",
    "1": "một",
    "2": "hai",
    "3": "ba",
    "4": "bốn",
    "5": "năm",
    "6": "sáu",
    "7": "bảy",
    "8": "tám",
    "9": "chín"
}
dict_alpha = {
    'a': ["a"],
    'b': ["bê", "bờ"],
    'c': ["sê", "cờ"],
    'd': ["dê", "dờ"],
    'e': ["e"],
    'f': ["ép"],
    'g': ["gờ"],
    'h': ["hắt"],
    'i': ["i"],
    'j': ["di"],
    'k': ["ca"],
    'l': ["lờ"],
    'm': ["mờ"],
    'n': ["nờ"],
    'o': ["o"],
    'p': ["pê", "pờ"],
    'q': ["quy", "qờ"],
    'r': ["rờ"],
    's': ["ét", "sờ"],
    't': ["tê", "tờ"],
    'u': ["u"],
    'v': ["vê", "vờ"],
    'w': ["vê kép", "đáp bờ liu"],
    'x': ["ích xì", "xờ"],
    'y': ["y"],
    'z': ["dét"],
    '.': ["chấm"],
    '+': ["cộng"]
}


def read_1_digit(n):
    if n in dict_digit:
        return dict_digit[n]
    else:
        return ""


def read_2_digits(n):
    if len(n) == 2:
        a = read_1_digit(n[0])
        b = read_1_digit(n[1])
        if n[0] == '1':
            a = "mười"
        elif n[0] != '0':
            a += " mươi"
            if n[1] == '1':
                b = "mốt"
        elif n[1] != '0':
            a = "linh"
        else:
            a = ""
        if n[1] == '0':
            b = ""
        result = (a + " " + b).strip()
        if result.endswith("mươi năm"):
            result = result.replace("mươi năm", "mươi lăm")
        if result == "mười năm":
            result = "mười lăm"
        other_result = [result]
        if "linh" in result:
            other_result.append(result.replace("linh", "lẻ"))
        if result.endswith("mươi"):
            other_result.append(result.replace("mươi", "chục"))
        if "mươi " in result:
            other_result.append(result.replace("mươi ", ""))
        for other in other_result:
            if " mốt" in other:
                other_result.append(other.replace(" mốt", " một"))
            if " bốn" in other:
                other_result.append(other.replace(" bốn", " tư"))
            if "bảy" in other:
                other_result.append(other.replace("bảy", "bẩy"))
        return list(set(other_result))
    else:
        result = read_1_digit(n)
        other_result = [result]
        if "bốn" in result:
            other_result.append(result.replace("bốn", "tư"))
        return other_result


def read_3_digits(n):
    if len(n) == 3:
        a = read_1_digit(n[0])
        b = read_2_digits(n[1:])
        if a == dict_digit['0'] and len(b[0]) == 0:
            return ['']
        other_result = []
        for b_ in b:
            other_result.append((a + " trăm " + b_).strip())
            if a == "không":
                other_result.append(b_)
        return other_result
    else:
        return read_2_digits(n)


def read_6_digits(n):
    if len(n) > 3:
        a = read_3_digits(n[:-3])
        b = read_3_digits(n[-3:])
        if len(a[0]) == 0: return b
        other_result = []
        for a_ in a:
            for b_ in b:
                other_result.append((a_ + " nghìn " + b_).strip())
                other_result.append((a_ + " ngàn " + b_).strip())
        return other_result
    else:
        return read_3_digits(n)


def read_9_digits(n):
    if len(n) > 6:
        a = read_3_digits(n[:-6])
        b = read_6_digits(n[-6:])
        if len(a[0]) == 0: return b
        other_result = []
        for a_ in a:
            for b_ in b:
                other_result.append((a_ + " triệu " + b_).strip())
        return other_result
    else:
        return read_6_digits(n)


def read_12_digits(n):
    if len(n) > 9:
        a = read_9_digits(n[:-9])
        b = read_9_digits(n[-9:])
        if len(a[0]) == 0: return b
        other_result = []
        for a_ in a:
            for b_ in b:
                other_result.append((a_ + " tỷ " + b_).strip())
        return other_result
    else:
        return read_9_digits(n)


def read_number(n):
    return [x for x in read_12_digits(str(n)) if sentence_to_numb(x)]
    # return [x for x in read_12_digits(str(n))]


def read_character(n, type='random'):
    list_read = []
    if type == 'random':
        rand_pos = 0 if random() < 0.5 else -1
    elif type == 'standard':
        rand_pos = 0
    else:
        return False
    for x in n.lower():
        if x in dict_digit:
            list_read.append(dict_digit[x])
        elif x in dict_alpha:
            list_read.append(dict_alpha[x][rand_pos])
    return ' '.join(list_read)


# Rules for some data types
def is_whole_number(n, type='Formal'):
    if type == 'Standard':
        if len(n) == 1:
            if re.fullmatch(r"[0-9]", n):
                return read_number(n)
        elif len(n) > 1:
            a = n[0]
            b = n[1:]
            if re.fullmatch(r"[1-9]", a) and re.fullmatch(r"[0-9]+", b):
                return read_number(n)
    elif type == 'Formal':
        if "." not in n:
            return is_whole_number(n, 'Standard')
        else:
            parts = n.split(".")
            if len(parts[0]) <= 3 and all(len(x) == 3 for x in parts[1:]):
                return is_whole_number(''.join(parts), 'Standard')
    return False


def is_positive_integer_number(n):
    return n != "0" and is_whole_number(n)


def is_negative_integer_number(n):
    if len(n) > 1 and n[0] == "-":
        ans = is_positive_integer_number(n[1:])
        if ans:
            return ["âm " + x for x in ans]
    return False


def is_integer_number(n):
    return is_whole_number(n) or is_negative_integer_number(n)


def is_positive_float_number(n):
    if "," in n:
        parts = n.split(",", 1)
        first = is_whole_number(parts[0])
        second = re.fullmatch(r"[0-9]+", parts[1])
        if first and second:
            other_result = []
            for first_ in first:
                other_result.append(first_ + " phẩy " + " ".join([read_number(x)[0] for x in parts[1]]))
            return other_result
    return False


def is_negative_float_number(n):
    if len(n) > 1 and n[0] == "-":
        ans = is_positive_float_number(n[1:])
        if ans: return ["âm " + x for x in ans]
    return False


def is_number(n):
    return is_integer_number(n) or is_positive_float_number(n) or is_negative_float_number(n)


def is_valid_date(date_str, format):
    try:
        return datetime.datetime.strptime(date_str, format)
    except ValueError:
        return False


def is_long_datetime(n):
    parts = re.compile("[/\-.]").split(n)
    if len(parts) == 3:
        dd = parts[0]
        MM = parts[1]
        yyyy = parts[2]
        if len(dd) == 1: dd = "0" + dd
        if len(MM) == 1: MM = "0" + MM
        if len(dd) == 2 and len(MM) == 2 and len(yyyy) == 4 and yyyy >= "1000":
            ans = is_valid_date(dd + "/" + MM + "/" + yyyy, '%d/%m/%Y')
            if ans:
                other_result = []
                for day_ in read_number(ans.day):
                    for month_ in read_number(ans.month):
                        for year_ in read_number(ans.year):
                            other_result.append("ngày {} tháng {} năm {}".format(day_, month_, year_))
                            other_result.append("mùng {} tháng {} năm {}".format(day_, month_, year_))
                            if month_ == "bốn":
                                other_result.append("ngày {} tháng {} năm {}".format(day_, "tư", year_))
                                other_result.append("mùng {} tháng {} năm {}".format(day_, "tư", year_))
                return other_result
    return False


def is_short_datetime_type_1(n):
    parts = n.split("/")
    if len(parts) == 2:
        dd = parts[0]
        MM = parts[1]
        if len(dd) == 1: dd = "0" + dd
        if len(MM) == 1: MM = "0" + MM
        if len(dd) == 2 and len(MM) == 2:
            ans = is_valid_date(dd + "/" + MM, '%d/%m')
            if ans:
                other_result = []
                for day_ in read_number(ans.day):
                    for month_ in read_number(ans.month):
                        other_result.append("ngày {} tháng {}".format(day_, month_))
                        other_result.append("mùng {} tháng {}".format(day_, month_))
                        other_result.append("hôm {} tháng {}".format(day_, month_))
                        if month_ == "bốn":
                            other_result.append("ngày {} tháng {}".format(day_, "tư"))
                            other_result.append("mùng {} tháng {}".format(day_, month_))
                            other_result.append("hôm {} tháng {}".format(day_, month_))
                return other_result
    return False


def is_short_datetime_type_2(n):
    parts = n.split("/" if "/" in n else "-")
    if len(parts) == 2:
        MM = parts[0]
        yyyy = parts[1]
        if len(MM) == 1: MM = "0" + MM
        if len(MM) == 2 and len(yyyy) == 4 and yyyy > "1000":
            ans = is_valid_date(MM + "/" + yyyy, '%m/%Y')
            if ans:
                other_result = []
                for month_ in read_number(ans.month):
                    for year_ in read_number(ans.year):
                        other_result.append("tháng {} năm {}".format(month_, year_))
                        if month_ == "bốn":
                            other_result.append("tháng {} năm {}".format("tư", year_))
                return other_result
    return False


def is_currency(n):
    str = n.lower()
    for symbols, reading in list_currency_symbols.items():
        if str.endswith(symbols):
            str = str[:-len(symbols)]
            ans = is_number(str)
            if ans:
                return [" ".join([x, reading]) for x in ans]
    return False


def is_percentage(n):
    ans = is_number(n[:-1])
    if len(n) > 1 and n[-1] == '%' and ans:
        return [" ".join([x, "phần trăm"]) for x in ans]
    return False


def is_license_plate(n):
    if "-" in n:
        parts = n.split("-", 1)
        left = parts[0]
        right = parts[1]
        if len(left) == 3: left += "1"
        if len(left) == 4 and len(right) > 3:
            if re.fullmatch(r"[1-9]", left[0]) and re.fullmatch(r"[0-9]", left[1]):
                if re.fullmatch(r"[a-z]", left[2]) and re.fullmatch(r"[1-9]", left[3]):
                    if "." in right:
                        if right.count(".") == 1 and right[0] != "." and right[-1] != ".":
                            right = right.replace(".", "")
                    if all(re.fullmatch(r"[0-9]", x) for x in right):
                        return [" ".join([x, read_character(n[2:], 'standard')]) for x in read_number(n[:2])]
    return False


def is_phone_number(n):
    if 9 <= len(n) <= 13:
        y = n
        if n[0] == "+":
            if not re.fullmatch(r"[1-9]", n[1]):
                return False
            y = n[1:]
        elif n[0] != "0":
            return False
        if "." in y:
            if y.count(".") <= 4 and y[0] != "." and y[-1] != ".":
                y = y.replace(".", "")
        return all(re.fullmatch(r"[0-9]", x) for x in y) and [read_character(n)]


list_domain_name = [".com", ".vn", ".tv", ".biz", ".net"]


def is_url(n):
    if n.startswith("http"):
        return bool(re.fullmatch(r"https?://([\w./-])+(:[\d]+)?([\w=&#?\-.]+)?", n))
    else:
        return any(n.endswith(x) and len(n) - len(x) > 2 for x in list_domain_name)


def is_email(n):
    part = n.split('@')
    if len(part) == 2 and len(part[0]) > 5 and len(part[1]) > 5:
        if '.' in part[1] and '..' not in part[1]:
            return True
    return False


def is_short_form_number(n):
    parts = n.split('k')
    if len(parts) == 2 and is_positive_integer_number(n.replace('k', '')):
        other_result = []
        for part0_ in read_number(parts[0]):
            for part1_ in read_number(parts[1]):
                other_result.append(' '.join([part0_, "nghìn", part1_]).strip())
        return other_result


def is_time(n):
    if n == "16:9": return False
    if n.endswith("ph"): n = n[:-2]
    if n.endswith("p"): n = n[:-1]
    numbers = re.compile(r'[hg:]').split(n)
    if len(numbers) == 2:
        for i in range(0, 2):
            if len(numbers[i]) == 2 and numbers[i][0] == '0':
                numbers[i] = numbers[i][1]
    try:
        hour = int(numbers[0])
        minute = int(numbers[1])
        if 0 <= hour <= 24 and 0 <= minute <= 60:
            other_result = []
            for hour_ in read_number(hour):
                for minute_ in read_number(minute):
                    other_result.append(hour_ + " giờ " + minute_ + " phút")
                    other_result.append(hour_ + " tiếng " + minute_ + " phút")
                    other_result.append(hour_ + " giờ " + minute_)
            return other_result
    except Exception:
        pass
    return False


def is_metric(n):
    if n.count("m") == 1:
        part = n.split("m")
        if re.fullmatch(r"[0-9]", part[0]):
            if re.fullmatch(r"[0-9]{1,2}", part[1]):
                other_result = []
                for part0_ in read_number(part[0]):
                    for part1_ in read_number(part[1]):
                        other_result.append(' '.join([part0_, "mét", part1_]).strip())
                return other_result
    for metric, name in list_metric.items():
        number = is_number(n[:-len(metric)])
        if n.endswith(metric) and number:
            return [x + " " + y for x in number for y in name]
    if any(x.isdigit() for x in n) and n in list_metric:
        return [x for x in list_metric[n]]
    return False


list_currency_symbols = {'₽'   : 'rúp',
                         '$'   : 'đô la',
                         '£'   : 'pao',
                         '¥'   : 'yên',
                         '₭'   : 'kíp',
                         '₩'   : 'guôn',
                         '฿'   : 'bát',
                         '€'   : 'ơ rô',
                         '₫'   : 'đồng',
                         '₿'   : 'bít coi',
                         "vnd" : 'việt nam đồng',
                         "vnđ" : 'việt nam đồng',
                         "đ"   : 'đồng',
                         "dola": 'đô la',
                         "euro": 'ơ rô'
                         }

list_metric = {"kg"         : ["ki lô gam", "ki lô gờ gam"],
               "g"          : ["gam"],
               "g"          : ["gờ"],  # Custom: 3G, 4G, 5G, ...
               "m"          : ["mét"],
               "m2"         : ["mét vuông"],
               "m3"         : ["mét khối"],
               "km"         : ["ki lô mét"],
               "km2"        : ["ki lô mét vuông"],
               "ml"         : ["mi ni lít", "mi li lít"],
               "km/s"       : ["ki lô mét trên giây"],
               "gb"         : ["gi ga bai", "ghi ga bai"],
               "ft"         : ["phít"],
               "ts"         : ["tê ét"],
               "m/s"        : ["mét trên giây"],
               "đ/sms"      : ["đồng trên ét em ét", "đồng trên một ét em ét"],
               "đ/phút"     : ["đồng trên phút", "đồng trên một phút"],
               "mb"         : ["mê ga bai", "mờ bê", "mê ga bít"],
               "kbps"       : ["ki lô bít trên giây", "ki lô bai trên giây"],
               "mb/phút"    : ["mê ga bai trên phút", "mê ga bít trên phút"],
               "ms"         : ["mi li giây", "mi ni giây"],
               "gb/ngày"    : ["gi ga bai trên ngày", "ghi ga bai trên ngày"],
               "mm"         : ["mi li mét", "mi ni mét"],
               "h/tuần"     : ["giờ trên tuần"],
               "cm"         : ["xen ti mét", "sen ti mét"],
               "usd/tuần"   : ["u ét đê trên tuần", "đô la trên tuần", "iu ét đê trên tuần", "iu ét đi trên tuần"],
               "m2sàn/người": ["mét vuông sàn trên người"],
               "/nq-cp"     : ["nghị quyết chính phủ"],
               "/qđ-syt"    : ["quyết định sở y tế"],
               "km/h"       : ["ki lô mét trên giờ"],
               "kb/s"       : ["ki lô bai trên giây", "ki lô bít trên giây"],
               "/qđ-ubnd"   : ["quyết định ủy ban nhân dân"],
               "%/cổ"       : ["phần trăm trên một cổ", "phần trăm trên cổ"],
               "v"          : ["vôn"],
               "s"          : ["giây"],
               "h"          : ["giờ"],
               "ph"         : ["phút"],
               "ha"         : ["héc ta", "hét ta", "hắt a", "ha"],
               "đồng/m3"    : ["đồng trên mét vuông", "đồng trên một mét vuông"],
               "m3/ngày"    : ["mét vuông trên ngày", "mét vuông trên một ngày"],
               "gr"         : ["gờ ram"],
               "đ/học"      : ["đồng trên một lần học"],
               "usd/1kg"    : ["u ét đê trên một ki lô gam"],
               "/qđ-bhxh"   : ["quy định bảo hiểm xã hội"],
               "mp"         : ["mê ga pích xeo"],
               "oc"         : ["độ xê", "độ sê"],
               "mbps"       : ["mê ga bít trên giây", "mê ga bai trên giây"],
               "px"         : ["pích xeo", "pích seo", "pít xeo", "pít seo"],
               "usd"        : ["u ét đê", "đô la"],
               "/cp"        : ["trên một cổ phiếu"],
               "%/năm"      : ["phần trăm trên năm", "phần trăm trên một năm"],
               "hz"         : ["héc"],
               "inch"       : ["inh"]
               }
list_special_string = {
    "vtv" : ["vê tê vê"],
    "h5n" : ["hát năm en nờ", "hắt năm en nờ"],
    "mp"  : ["mờ pê"],
    "u"   : ["u"],
    "u."  : ["u"],
    "u-"  : ["u"],
    "s"   : ["ét", "ét xì", "ét sì"],
    "a"   : ["a"],
    "w"   : ["vê kép", "đáp bờ diu"],
    "e"   : ["e"],
    "f"   : ["ép"],
    "q."  : ["quận"],
    "note": ["nốt"],
    "vov" : ["vê o vê", "vê ô vê"],
    "pc"  : ["pê xê", "pê sê", "pi xi", "pi si"],
    "vtc" : ["vê tê xê", "vê tê sê"],
    "bet" : ["bét"],
    "sctv": ["ét sê tê vê", "ét xê tê vê"],
}
list_static_string = {
    "3.0"   : ["ba chấm không"],
    "4.0"   : ["bốn chấm không"],
    "3d"    : ["ba đê"],
    "24/24" : ["hai tư trên hai tư", "hai bốn trên hai bốn"],
    "24/7"  : ["hai tư trên bảy", "hai tư trên bẩy"],
    "m/s2"  : ["mét trên giây bình phương"],
    "802.11": ["tám không hai chấm mười một", "tám không hai chấm một một"],
    "6/55"  : ["sáu trên năm lăm"],
    "6/45"  : ["sáu trên bốn lăm"],
    "4.7"   : ["bốn phẩy bẩy", "bốn phẩy bảy", "bốn chấm bẩy", "bốn chấm bảy"],
    "t.ư"   : ["trung ương"],
    "ubnd"  : ["ủy ban nhân dân"],
    "pccc"  : ["phòng cháy chữa cháy"],
    "tq"    : ["trung quốc"],
    "lđbđ"  : ["liên đoàn bóng đá"],
    "sn"    : ["sinh năm"],
}


def is_special_string(n):
    for x in list_special_string:
        if n.startswith(x):
            number = is_positive_integer_number(n[len(x):])
            if number:
                return [z + " " + y for y in number for z in list_special_string[x]]
    if n in list_special_string:
        return [x for x in list_special_string[n]]
    elif n in list_static_string:
        return [x for x in list_static_string[n]]
    else:
        return False


def normalize(n):
    n = n.replace("–", "-")
    n = n.replace("²", "2")
    n = n.replace("³", "3")
    n = n.replace(";", "")
    n = n.replace("(", "")
    n = n.replace(")", "")
    n = n.replace("\"", "")
    n = n.replace("'", "")
    if n.endswith(":"):
        n = n[:-1]
    if n.startswith(":"):
        n = n[1:]
    if n.endswith(",") or n.endswith("."):
        n = n[:-1]
    return n


# list_function = [is_metric, is_time, is_short_form_number, is_email, is_url, is_phone_number, is_license_plate,
#                  is_percentage, is_currency, is_short_datetime_type_1, is_short_datetime_type_2, is_long_datetime,
#                  is_number, is_special_string]


def run_all_function():
    list_digit = []
    with open("C:\\Users\\vietbt\\Documents\\VLSP Data\\all_output.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split("\t")
            word = parts[0]
            if any(x.isdigit() for x in word):
                list_digit.append(word)
    dict = {}
    for x in list_digit:
        if x not in dict:
            dict[x] = 0
        dict[x] += 1

    print("Word\tTimes\t" + "\t".join(func.__name__ for func in list_function) + "\tResult")
    count = 0
    for x in dict:
        word = normalize(x)
        list_ans = [convert(func(word)) for func in list_function]
        result = "\t".join([result for result in list_ans if result != "_"])
        if len(result) == 0: result = "_"
        if result != "_":
            count += 1
        print(x + "\t" + str(dict[x]) + "\t" + "\t".join(list_ans) + "\t" + result)
    print(str(count) + "/" + str(len(dict)))


def is_long_datetime_update(n):
    parts = re.compile("[/\-.]").split(n)
    if len(parts) == 3:
        dd = parts[0]
        MM = parts[1]
        yyyy = parts[2]
        if len(dd) == 1: dd = "0" + dd
        if len(MM) == 1: MM = "0" + MM
        if len(dd) == 2 and len(MM) == 2 and len(yyyy) == 4 and yyyy >= "1000":
            ans = is_valid_date(dd + "/" + MM + "/" + yyyy, '%d/%m/%Y')
            if ans:
                other_result = []
                for day_ in read_number(ans.day):
                    for month_ in read_number(ans.month):
                        for year_ in read_number(ans.year):
                            other_result.append("{} tháng {} năm {}".format(day_, month_, year_))
                            if month_ == "bốn":
                                other_result.append("{} tháng {} năm {}".format(day_, "tư", year_))
                return other_result
    return False


def is_short_datetime_type_1_update(n):
    parts = re.compile("[/\-.]").split(n)
    if len(parts) == 2:
        dd = parts[0]
        MM = parts[1]
        if len(dd) == 1: dd = "0" + dd
        if len(MM) == 1: MM = "0" + MM
        if len(dd) == 2 and len(MM) == 2:
            ans = is_valid_date(dd + "/" + MM, '%d/%m')
            if ans:
                other_result = []
                for day_ in read_number(ans.day):
                    for month_ in read_number(ans.month):
                        other_result.append("{} tháng {}".format(day_, month_))
                        if month_ == "bốn":
                            other_result.append("{} tháng {}".format(day_, "tư"))
                return other_result
    return False


def is_short_datetime_type_2_update(n):
    parts = re.compile("[/\-.]").split(n)
    if len(parts) == 2:
        MM = parts[0]
        yyyy = parts[1]
        if len(MM) == 1: MM = "0" + MM
        if len(MM) == 2 and len(yyyy) == 4 and yyyy > "1000":
            ans = is_valid_date(MM + "/" + yyyy, '%m/%Y')
            if ans:
                other_result = []
                for month_ in read_number(ans.month):
                    for year_ in read_number(ans.month):
                        other_result.append("{} năm {}".format(month_, year_))
                        if month_ == "bốn":
                            other_result.append("{} năm {}".format("tư", year_))
                return other_result
    return False


def read_string(word, prev_word=""):
    word = normalize(word)
    prev_word = normalize(prev_word)
    if prev_word in ["ngày", "hôm", "mùng", "chiều", "sáng", "lúc", "đêm", "qua", "trưa", "tối", "nay", "đến", "sau",
                     "khuya"]:
        result = is_short_datetime_type_1_update(word)
        if not result:
            result = is_long_datetime_update(word)
        if result:
            shuffle(result)
            return result, "DATE"

    if prev_word in ["tháng", "lúc"]:
        result = is_short_datetime_type_2_update(word)
        if result:
            shuffle(result)
            return result, "DATE"

    if prev_word in ["ngày"]:
        result = is_positive_integer_number(word)
        if result and 1 <= len(word) <= 2:
            shuffle(result)
            return result, "DATE"
    if prev_word in ["tháng"]:
        result = is_positive_integer_number(word)
        if result and 1 <= len(word) <= 2:
            if word == "4": result.append("tư")
            shuffle(result)
            return result, "DATE"
    if prev_word in ["năm"]:
        result = is_positive_integer_number(word)
        if result and 3 <= len(word) <= 4:
            other_way_to_read = read_character(word)
            result.append(other_way_to_read)
            if other_way_to_read.endswith(" một") and not other_way_to_read.endswith(
                    "không một") and not other_way_to_read.endswith("mười một"):
                result.append(other_way_to_read.replace(" một", " mốt"))
            if " một " in other_way_to_read:
                if other_way_to_read.endswith(" không"):
                    result.append(other_way_to_read.replace("một không", "mười"))
                else:
                    result.append(other_way_to_read.replace("một ", "mười "))

            if other_way_to_read.endswith(" không") and not other_way_to_read.endswith(" không không") \
                    and not other_way_to_read.endswith(" một không"):
                result.append(other_way_to_read.replace(" không", " mươi"))
            shuffle(result)
            return result, "DATE"

    if prev_word == "viên":
        result = is_short_datetime_type_1_update(word)
        if not result:
            result = is_long_datetime_update(word)
        if result:
            shuffle(result)
            return result, "MISC"

    if prev_word in ["lộ", "đường"]:
        if word.endswith("a") or word.endswith("b"):
            number_road = word[:-1]
            result = is_positive_integer_number(number_road)
            if result:
                return result, "MISC"

    for func in list_function:
        result = func(word)
        # print(func.__name__)
        if result:
            shuffle(result)
            return result, list_function[func]
    return False, "ERROR"


def convert(n):
    return str(n) if n else "_"


class SYLLABLE:
    def __init__(self, origin="", syllable="", postagging_label="", word_label="", entity_label="", separator_label="",
                 index_sentence=""):
        self.origin = origin
        self.syllable = syllable
        self.postagging_label = postagging_label
        self.word_label = word_label
        self.entity_label = entity_label
        self.separator_label = separator_label
        self.index_sentence = index_sentence

    def __str__(self):
        return self.syllable + "\t" \
               + self.postagging_label + "\t" \
               + self.word_label + "\t" \
               + self.entity_label + "\t" \
               + self.separator_label + "\t" + str(self.index_sentence)

    def copy(self):
        return SYLLABLE(origin=self.origin,
                        syllable=self.syllable,
                        postagging_label=self.postagging_label,
                        word_label=self.word_label,
                        entity_label=self.entity_label,
                        separator_label=self.separator_label,
                        index_sentence=self.index_sentence)


def get_list_dict_syllable():
    conll_path_list = [
        "C:\\Users\\vietbt\\Documents\\VLSP Data\\VLSP\\2016\\test_vlsp2016.conll",
        "C:\\Users\\vietbt\\Documents\\VLSP Data\\VLSP\\2016\\train_vlsp2016.conll",
        "C:\\Users\\vietbt\\Documents\\VLSP Data\\VLSP\\2018\\test_vlsp2018.conll",
        "C:\\Users\\vietbt\\Documents\\VLSP Data\\VLSP\\2018\\train_vlsp2018.conll",
        # "C:\\Users\\vietbt\\Desktop\\FinalVitalk.txt.genNER"

    ]
    list_syllable = []
    sentence_number = 0
    for conll_path in conll_path_list:
        sentence_number = get_list_syllable(conll_path, list_syllable, sentence_number)

    list_dict_syllable = {}
    for syllable in list_syllable:
        if syllable.index_sentence not in list_dict_syllable:
            list_dict_syllable[syllable.index_sentence] = []
        list_dict_syllable[syllable.index_sentence].append(syllable)

    new_list_syllable = []
    # p = Pool(None)
    # with ProcessPoolExecutor(None) as p:
    #     for x in p.map(multi_way_to_read_syllable, list_dict_syllable.values()):
    #         new_list_syllable += x

    # for x in p.map(multi_way_to_read_syllable, list_dict_syllable.values()):
    #     new_list_syllable += x
    # for sentence in list_dict_syllable.values():
    #     new_list_syllable += multi_way_to_read_syllable(sentence)
    return new_list_syllable


def multi_way_to_read_syllable(sentence):
    _, total_ways_to_read_sentence = fix_content_syllable_sentence(sentence)
    max_number_random = 10
    list_sentence = []
    while total_ways_to_read_sentence > 0 and max_number_random > 0:
        new_sentence, _ = fix_content_syllable_sentence(sentence)
        if len(list_sentence) == 0 or not any(is_equal_sentences(x, new_sentence) for x in list_sentence):
            list_sentence.append(new_sentence)
        total_ways_to_read_sentence -= 1
        max_number_random -= 1
    return list_sentence


def is_equal_sentences(sentence_1, sentence_2):
    if len(sentence_1) != len(sentence_2):
        return False
    for i in range(len(sentence_1)):
        if sentence_1[i].syllable != sentence_2[i].syllable:
            return False
    return True


def copy_sentence(sentence):
    new_sentence = []
    for syllable in sentence:
        new_sentence.append(syllable.copy())
    return new_sentence


def fix_content_syllable_sentence(sentence):
    sentence = copy_sentence(sentence)
    inserted = 0
    i = 0
    total_ways_to_read_sentence = 1
    while i < len(sentence):
        syllable = sentence[i]
        prev_word = sentence[i - 1] if i > 0 else False
        next_word = sentence[i + 1] if i + 1 < len(sentence) else False
        next_next_word = sentence[i + 2] if i + 2 < len(sentence) else False

        # custom
        if syllable.postagging_label == "M" and syllable.entity_label == "O":
            syllable.entity_label = "B_NUMB"
            for k in [1, 2, 3]:
                next_k_word = sentence[i + k] if i + k < len(sentence) else False
                if next_k_word and next_k_word.postagging_label == "M" and next_k_word.entity_label == "O":
                    next_k_word.entity_label = "I_NUMB"
        # done

        if inserted > 0:
            inserted -= 1
            continue
        if any(x.isdigit() for x in sentence[i].syllable):
            # print(syllable.syllable)

            str_val, type = read_string(sentence[i].syllable, prev_word.syllable if prev_word else "")

            if str_val:
                total_ways_to_read_sentence *= len(str_val)
                words = str_val[0].split(" ")
                syllable.syllable = words[0]
                last_separator_label = syllable.separator_label
                syllable.separator_label = "O"

                # if next_word == "m":
                #     sentence[i + 1].syllable = "mét"
                # sentence[i + 1].entity_label = "I_MISC"
                # elif next_word == "km":
                #     sentence[i + 1].syllable = "ki lô mét"
                # sentence[i + 1].entity_label = "I_MISC"
                # elif next_word == "giờ" or next_word == "phút" or next_word == "giây":
                #     sentence[i + 1].entity_label = "I_DATE"

                if next_word and next_next_word and next_word.syllable + " " + next_next_word.syllable == "phần trăm" and type == "NUMB":
                    type = "PERC"
                    next_word.word_label = "I_W"
                    next_next_word.word_label = "I_W"
                    next_word.entity_label = "I_" + type
                    next_next_word.entity_label = "I_" + type
                if next_word and next_word.syllable in ["triệu", "tỷ", "tỉ"] and type == "NUMB":
                    next_word.word_label = "I_W"
                    next_word.entity_label = "I_" + type

                if next_word and next_word.syllable in ["mét", "gam"] and type == "NUMB":
                    type = "MISC"
                    next_word.word_label = "I_W"
                    next_word.entity_label = "I_" + type

                if prev_word and prev_word.syllable in ["ngày", "hôm", "mùng", "chiều", "sáng", "lúc", "đêm", "trưa",
                                                        "tối", "khuya", "kia", "qua", "tháng",
                                                        "năm"] and type == "DATE":
                    if i - 2 >= 0 and sentence[i - 2].syllable + sentence[i - 1].syllable \
                            in ["buổi sáng", "buổi chiều", "buổi tối", "rạng sáng", "đêm khuya", "đêm tối", "hôm nay",
                                "hôm qua", "hôm kia"]:
                        sentence[i - 2].word_label = "B_W"
                        sentence[i - 2].entity_label = "B_" + type
                        sentence[i - 1].word_label = "I_W"
                        sentence[i - 1].entity_label = "I_" + type
                    else:
                        sentence[i - 1].word_label = "B_W"
                        sentence[i - 1].entity_label = "B_" + type
                    syllable.word_label = "I_W"
                    syllable.entity_label = "I_" + type
                else:
                    syllable.entity_label = syllable.word_label[:-1] + type

                if len(words) > 1:
                    all_copy_syllable = []
                    words.reverse()
                    for word in words[:-1]:
                        copy_syllable = syllable.copy()
                        copy_syllable.syllable = word
                        copy_syllable.word_label = "I_W"
                        copy_syllable.separator_label = "O"
                        copy_syllable.entity_label = "I_" + type
                        all_copy_syllable.append(copy_syllable)
                    all_copy_syllable[0].separator_label = last_separator_label
                    for copy_syllable in all_copy_syllable:
                        sentence.insert(i + 1, copy_syllable)
                        inserted += 1
            else:
                with open("log_unrealizable_number.txt", "a+", encoding="utf-8") as f:
                    str = sentence[i].syllable + "\t" + " ".join(x.syllable for x in sentence)
                    f.write(str + "\n")
                    print(str)
                total_ways_to_read_sentence = 0
                break
        i += 1
    return sentence, total_ways_to_read_sentence


def fix_content_line(line):
    line = line.strip()
    line = line.replace("–", "-")
    line = line.replace("—", "-")
    line = line.replace("“", "\"")
    line = line.replace("”", "\"")
    line = line.replace("‘", "'")
    line = line.replace("’", "'")
    line = line.replace("™", "TM")
    line = line.replace("×", "x")
    return line


def get_list_syllable(conll_path, list_syllable, sentence_number):
    with open(conll_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
        for index in range(len(all_lines)):
            line = all_lines[index]
            if "\t" in line:
                parts = line.strip().split("\t")
                syllable_origin = parts[0]
                if len(syllable_origin) == 1 and not syllable_origin.isalnum():
                    list_syllable[-1].separator_label = "B_" + syllable_origin
                elif len(syllable_origin) > 0:
                    # syllable_origin = syllable_origin.lower()
                    postagging_label = parts[1]
                    entity_label = parts[-1]
                    if "+" in entity_label: entity_label = entity_label[:entity_label.index("+")]
                    # VLSP 2016
                    if "\t" in entity_label:
                        entity_label = entity_label[entity_label.index("\t") + 1]
                    # Done VLSP 2016

                    # Chị Oanh bảo bộ GRAM-CNN đặt label viết hoa thành MISC
                    if "ORG" in entity_label: entity_label = "ORG"  # entity_label = "ORG"
                    if "PER" in entity_label: entity_label = "PER"  # entity_label = "PER"
                    if "LOC" in entity_label: entity_label = "LOC"  # entity_label = "LOC"
                    if "MISC" in entity_label: entity_label = "MIS"  # entity_label = "MISC"
                    # Done

                    is_first = True
                    is_in_list = False
                    if syllable_origin.endswith("G"):
                        ans = read_number(syllable_origin[:-1])
                        if ans:
                            syllable_origin = ans[0] + "_gờ"
                            entity_label = "MISC"
                            is_in_list = True
                    if not is_in_list:
                        for name, metric in list_currency_symbols.items():
                            if syllable_origin.lower() == name:
                                syllable_origin = metric.replace(" ", "_")
                                entity_label = "MISC"
                                is_in_list = True
                                break
                    if not is_in_list:
                        for name, metric in list_special_string.items():
                            if syllable_origin.lower() == name:
                                syllable_origin = metric[randrange(0, len(metric))].replace(" ", "_")
                                entity_label = "MISC"
                                is_in_list = True
                                break
                    if not is_in_list:
                        for name, metric in list_metric.items():
                            if syllable_origin.lower() == name:
                                syllable_origin = metric[randrange(0, len(metric))].replace(" ", "_")
                                entity_label = "MISC"
                                is_in_list = True
                                break
                    if not is_in_list:
                        for name, metric in list_static_string.items():
                            if syllable_origin.lower() == name:
                                syllable_origin = metric[randrange(0, len(metric))].replace(" ", "_")
                                entity_label = "MISC"
                                is_in_list = True
                                break
                    for word in syllable_origin.split("_"):
                        if len(word) > 0:
                            if entity_label in ["ORG", "PER", "LOC", "MIS"]:
                                if word[0] == word[0].upper():
                                    entity_label = "CAP"
                                else:
                                    entity_label = "O"
                                    is_first = True

                            word_entity_label = "B_" + entity_label if is_first else "I_" + entity_label
                            list_syllable.append(SYLLABLE(
                                origin=syllable_origin,
                                syllable=word.lower(),
                                word_label="B_W" if is_first else "I_W",
                                postagging_label=postagging_label,
                                entity_label="O" if entity_label == "O" else word_entity_label,
                                separator_label="O",
                                index_sentence=sentence_number
                            ))
                            is_first = False
            else:
                if list_syllable[-1].separator_label == "O":
                    list_syllable[-1].separator_label = "B_."
                sentence_number += 1
    return sentence_number


list_function = {is_metric               : "MISC",
                 is_time                 : "DATE",
                 is_short_form_number    : "NUMB",
                 is_phone_number         : "NUMB",
                 is_license_plate        : "MISC",
                 is_percentage           : "PERC",
                 is_currency             : "MISC",
                 is_short_datetime_type_1: "DATE",
                 is_short_datetime_type_2: "DATE",
                 is_long_datetime        : "DATE",
                 is_number               : "NUMB",
                 is_special_string       : "MISC"}


def save_syllable_to_file(path, list_dict_syllable):
    index = 0
    with open(path, "w", encoding="utf-8") as f:
        for value in list_dict_syllable:
            for syllable in value:
                # if "NUMB" in syllable.entity_label: syllable.entity_label = "O"
                # if "DATE" in syllable.entity_label: syllable.entity_label = "O"
                # if "PERC" in syllable.entity_label: syllable.entity_label = "O"
                # if "MISC" in syllable.entity_label: syllable.entity_label = "O"

                output = syllable.syllable + " " + syllable.postagging_label + " " + syllable.entity_label.replace("_",
                                                                                                                   "-")
                # if syllable.syllable != "...":
                #     if syllable.separator_label not in ["B_.", "B_,", "B_?", "B_!"]:
                #         syllable.separator_label = "O"
                #     output = syllable.syllable + " " + syllable.postagging_label + " " + syllable.separator_label.replace(
                #         "_", "-")
                #     # if index % 100 == 0 and index > 0: output += "\n"
                #     index += 1
                f.write(output + "\n")
            f.write("\n")


def get_list_sentence_at_index(list_dict_syllable, indexs):
    list_sentence = []
    for sentence in list_dict_syllable:
        if sentence[0].index_sentence in indexs:
            list_sentence.append(sentence)
    return list_sentence


def run_vlsp():
    list_dict_syllable = get_list_dict_syllable()
    shuffle(list_dict_syllable)
    total_length = len(list_dict_syllable)
    train_size = 0.8 * total_length
    list_dict_train_syllable = []
    list_dict_dev_syllable = []
    k = 0
    error_index = 0
    for x in list_dict_syllable:
        if len(x) > 0:
            if k < train_size:
                list_dict_train_syllable.append(x)
                error_index = x[0].index_sentence
            elif k == train_size:
                while list_dict_train_syllable[-1][0].index_sentence == error_index:
                    list_dict_train_syllable.pop()
            elif x[0].index_sentence != error_index:
                list_dict_dev_syllable.append(x)
        k += 1
    save_syllable_to_file("C:\\Users\\vietbt\\Documents\\VLSP Data\\train_output_python.txt", list_dict_train_syllable)
    save_syllable_to_file("C:\\Users\\vietbt\\Documents\\VLSP Data\\dev_output_python.txt", list_dict_dev_syllable)
    # save_syllable_to_file("C:\\Users\\vietbt\\Documents\\VLSP Data\\test_output_python.txt", list_dict_test_syllable)


dict_unit = {
    "không": 0,
    "một"  : 1,
    "mốt"  : 1,
    "hai"  : 2,
    "ba"   : 3,
    "bốn"  : 4,
    "tư"   : 4,
    "năm"  : 5,
    "lăm"  : 5,
    "nhăm" : 5,
    "sáu"  : 6,
    "bảy"  : 7,
    "bẩy"  : 7,
    "tám"  : 8,
    "chín" : 9,
    "mười" : 10,
}

numb_x1 = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]
numb_x2 = ["hai", "ba", "bốn", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]
numb_x3 = ["không", "mốt", "hai", "ba", "bốn", "tư", "lăm", "nhăm", "sáu", "bảy", "bẩy", "tám", "chín"]
numb_x4 = ["không", "một", "hai", "ba", "bốn", "tư", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]
numb_x5 = ["không", "một", "hai", "ba", "bốn", "tư", "lăm", "nhăm", "sáu", "bảy", "bẩy", "tám", "chín"]
numb_y = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "bẩy", "tám", "chín"]


def get_number_from_hundred_str(str):
    if len(str) == 0:
        return 0, False
    value = 0
    if "trăm" in str:
        part = str.split("trăm", 1)
        unit = part[0].strip()
        str = part[1].strip()
        if unit not in numb_y: return value, False
        unit_value = dict_unit[unit]
        value += unit_value * 100
    if str.startswith("mười"):
        part = str.split("mười", 1)
        unit = part[1].strip()
        if len(unit) == 0:
            value += 10
        else:
            if unit not in numb_x5: return value, False
            unit_value = dict_unit[unit]
            value += 10 + unit_value
    elif "mươi" in str:
        part = str.split("mươi", 1)
        ten_str = part[0].strip()
        unit = part[1].strip()
        if ten_str not in numb_x2 or dict_unit[ten_str] <= 1:
            return value, False
        ten_value = dict_unit[ten_str]
        if len(unit) == 0:
            value += 10 * ten_value
        else:
            if unit not in numb_x3: return value, False
            unit_value = dict_unit[unit]
            value += 10 * ten_value + unit_value
    elif "chục" in str:
        part = str.split("chục", 1)
        unit = part[0].strip()
        if len(part[1]) != 0 or unit not in numb_x2: return value, False
        unit_value = dict_unit[unit]
        value += 10 * unit_value
    elif str.startswith("linh") or str.startswith("lẻ"):
        part = str.split("linh" if str.startswith("linh") else "lẻ", 1)
        unit = part[1].strip()
        if unit not in numb_x4: return value, False
        unit_value = dict_unit[unit]
        value += unit_value
    elif " " in str:
        part = str.split(" ", 1)
        if part[0] not in numb_x2 or part[1] not in numb_x3:
            return value, False
        value += dict_unit[part[0]] * 10 + dict_unit[part[1]]
    elif str in numb_x1 and "trăm" not in str:
        value += dict_unit[str]
    elif len(str) != 0:
        return value, False
    return value, True


def sentence_to_numb(sentence, word_by_word=False, format_numb=True):
    numb = _sentence_to_numb(sentence, word_by_word=word_by_word, format_numb=format_numb)
    if numb:
        if numb.endswith(".000.000.000"):
            numb = numb[:-12]
            return numb + " " + "tỷ"
        elif numb.endswith(".000.000"):
            numb = numb[:-8]
            if len(numb) < 4:
                return numb + " " + "triệu"
            else:
                return numb[:-4] + " tỷ " + numb[-3:] + " triệu"
        return numb
    elif sentence.endswith(" triệu"):
        numb = _sentence_to_numb(sentence[:-6], word_by_word=word_by_word, format_numb=format_numb)
        if numb:
            return numb + " triệu"
    elif sentence.endswith(" tỷ"):
        numb = _sentence_to_numb(sentence[:-3], word_by_word=word_by_word, format_numb=format_numb)
        if numb:
            return numb + " tỷ"
    return False


def _sentence_to_numb(sentence, word_by_word=False, format_numb=True):
    if len(sentence) == 0:
        return False
    if word_by_word:
        sentence_2 = sentence
        for x in ["linh", "lẻ"]:
            sentence_2 = sentence_2.replace(x + " mười", "mười")
            sentence_2 = sentence_2.replace(x, "không")
        for x in dict_unit:
            sentence_2 = sentence_2.replace("mười " + x, "một " + x)
        words = sentence_2.split(" ")
        ans = []
        for x in words:
            if x in dict_unit:
                ans.append(str(dict_unit[x]))
            else:
                ans = []
                break
        if len(ans) > 0:
            return "".join(ans)
    value = 0
    is_positive = True
    if sentence.startswith("âm "):
        sentence = sentence[3:]
        is_positive = False
    if "tỷ" in sentence:
        part = sentence.split("tỷ", 1)
        hundred_part = part[0].strip()
        sentence = part[1].strip()
        hundred_value, is_correct = get_number_from_hundred_str(hundred_part)
        if not is_correct: return False
        value += hundred_value * 1e9
    if "triệu" in sentence:
        part = sentence.split("triệu", 1)
        hundred_part = part[0].strip()
        sentence = part[1].strip()
        hundred_value, is_correct = get_number_from_hundred_str(hundred_part)
        if not is_correct: return False
        value += hundred_value * 1e6
    if "nghìn" in sentence or "ngàn" in sentence:
        part = sentence.split("nghìn" if "nghìn" in sentence else "ngàn", 1)
        hundred_part = part[0].strip()
        sentence = part[1].strip()
        hundred_value, is_correct = get_number_from_hundred_str(hundred_part)
        if not is_correct: return False
        value += hundred_value * 1e3

    if "phẩy" in sentence:
        part = sentence.split("phẩy")
        real_str = part[0].strip()
        unreal_str = part[1].strip()
        if len(real_str) == 0 or len(unreal_str) == 0: return False
        hundred_value, is_correct = get_number_from_hundred_str(real_str)
        if not is_correct: return False
        value += hundred_value
        result = format_number(value, is_positive, format_numb=format_numb)
        result += ","
        read_unreal = sentence_to_numb(unreal_str, format_numb=format_numb)
        # print("read_unreal = " + read_unreal)
        if read_unreal:
            result += read_unreal
        else:
            for word in unreal_str.split(" "):
                if word not in dict_unit: return False
                result += str(dict_unit[word])
        return result
    else:
        if len(sentence) > 0:
            hundred_value, is_correct = get_number_from_hundred_str(sentence)
            if not is_correct:
                return False
            value += hundred_value
        return format_number(value, is_positive, format_numb=format_numb)


def format_number(value, is_positive, format_numb):
    if format_numb and int(value) >= 10000:
        ans = '{:,d}'.format(int(value)) if is_positive else '-{:,d}'.format(int(value))
        return ans.replace(',', '.')
    else:
        return str(int(value)) if is_positive else "-" + str(int(value))


def get_index(sentence=[], list_word=[], min=0, get_last=True):
    index_ans = -1
    for word in list_word:
        for i in range(len(sentence)):
            if sentence[i] == word:
                if i >= min and i > index_ans:
                    index_ans = i
                    if not get_last:
                        return index_ans
    return index_ans if index_ans != -1 else len(sentence)


def read_last(number, format_numb=False):
    words = number.split(" ")
    list_read_last = []
    for i in range(len(words)):
        list_read_last.append((" ".join(words[:i]), " ".join(words[i:])))
    # list_read_last.reverse()
    for word, next_word in list_read_last:
        read_numb = sentence_to_numb(next_word, format_numb=format_numb)
        if read_numb:
            return (word + " " + read_numb).strip()
    return False


def read_first(number, format_numb=False):
    words = number.split(" ")
    list_read_first = []
    for i in range(len(words)):
        list_read_first.append((" ".join(words[:i + 1]), " ".join(words[i + 1:])))
    list_read_first.reverse()
    for word, next_word in list_read_first:
        read_numb = sentence_to_numb(word, format_numb=format_numb)
        if read_numb:
            return (read_numb + " " + next_word).strip()
    return False


def get_ans(list_syllabels):
    # print(list_syllabels)
    list_words = []
    for word, label in list_syllabels:
        if label == "O":
            list_words.append((word, "O"))
        elif label.startswith("B-"):
            list_words.append((word, label[2:]))
        elif label.startswith("I-"):
            sentence, sen_label = list_words[-1]
            if label[2:] == list_words[-1][1]:
                list_words[-1] = (sentence + " " + word, sen_label)
            else:
                list_words.append((word, label[2:]))
    return _get_ans(list_words)


def _get_ans(list_words):
    sentence_split = " ".join([x.replace(" ", "_") for x, y in list_words])
    print(sentence_split)
    print("\n".join([str(x) for x in list_words]))
    result = []
    for index in range(len(list_words)):
        sentence, label = list_words[index]
        if label == "NUMB":
            read_numb = sentence_to_numb(sentence)
            if read_numb:
                result.append((str(read_numb), label))
            else:
                result.append((sentence, label))
        elif label == "DATE":
            part = sentence.split(" ")
            is_correct_date = True
            is_correct_hour = True
            if "giờ" in sentence:
                part = sentence.split("giờ", 1)
                hour = part[0].strip()
                minute = part[1].strip()
                if minute.endswith("phút"):
                    minute = minute[:-len("phút") - 1]
                # print(hour, minute)
                ans_hour = read_last(hour)
                ans_minute = read_first(minute)
                # print(ans_hour)
                # print(ans_minute)
                # ans_all_hour = sentence_to_numb(hour)
                ans_all_minute = sentence_to_numb(minute, format_numb=False)
                # print(ans_all_minute)
                if ans_hour and ans_all_minute:
                    sentence = ans_hour + ":" + ans_all_minute
                elif ans_hour or ans_minute:
                    if part[1].endswith("phút") and ans_minute:
                        ans_minute += " phút"
                    if not ans_minute:
                        ans_minute = part[1]
                    sentence = ans_hour + " giờ " + ans_minute
                else:
                    is_correct_hour = False
            elif "phút" in sentence:
                is_correct_hour = False
                for i in range(len(part)):
                    read_numb = sentence_to_numb(" ".join(part[:-i]), format_numb=False)
                    if read_numb:
                        sentence = read_numb + " " + " ".join(part[-i:])
                        is_correct_hour = True
                        break
            else:
                is_correct_hour = False

            index_day = get_index(part, ["ngày", "mùng", "hôm", "sáng", "trưa", "chiều", "tối", "đêm", "khuya", "lúc"],
                                  0, get_last=True)
            index_month = get_index(part, ["tháng"], index_day + 1 if index_day != len(part) else 0, get_last=False)
            index_year = get_index(part, ["năm"], index_month + 2 if index_month != len(part) else 0, get_last=False)

            if index_day < len(part) and index_month == len(part):
                index_year = get_index(part, ["năm"], index_day + 2)
                index_month = index_year

            # print(sentence)
            day_str = " ".join(part[index_day + 1:index_month])
            month_str = " ".join(part[index_month + 1:index_year])
            year_str = " ".join(part[index_year + 1:])

            day = sentence_to_numb(day_str, word_by_word=True, format_numb=False)
            month = sentence_to_numb(month_str, word_by_word=True, format_numb=False)
            year = sentence_to_numb(year_str, word_by_word=True, format_numb=False)
            if day and len(day) == 1: day = "0" + day
            if month and len(month) == 1: month = "0" + month

            if not day and len(day_str) > 0: day_str = " ngày " + day_str + " "
            if not month and len(month_str) > 0: month_str = " tháng " + month_str + " "
            if not year and len(year_str) > 0: year_str = " năm " + year_str + " "
            print(day_str, day)
            print(month_str, month)
            print(year_str, year)
            if day and month and year:
                sentence = " ".join(part[:index_day + 1]) + " %s/%s/%s" % (day, month, year)
            elif day and 1 <= int(day) <= 31 and month and 1 <= int(month) <= 9999:
                if int(month) > 12:
                    words_month = month_str.split(" ", 1)
                    month = sentence_to_numb(words_month[0])
                    if len(month) == 1: month = "0" + month
                    next_words_month = read_last(words_month[1])
                    if next_words_month:
                        month += " " + next_words_month
                    else:
                        month += " " + words_month[1]
                sentence = " ".join(part[:index_day + 1]) + " %s/%s" % (day, month) + year_str
            elif month and 1 <= len(month) <= 12 and year and 1 <= int(year) <= 9999:
                sentence = day_str + " ".join(part[:index_month + 1]) + " %s/%s" % (month, year)
            elif day and 1 <= int(day) <= 31 and year and 1 <= int(year) <= 9999:
                sentence = " ".join(part[:index_day + 1]) + " %s%s năm %s" % (day, month_str, year)
            elif day and 1 <= int(day) <= 9999:
                if day.startswith("0"):
                    day = day[1:]
                sentence = " ".join(part[:index_day + 1]) + " " + day + month_str + year_str
            elif month and 1 <= int(month) <= 9999:
                if month.startswith("0"):
                    month = month[1:]
                sentence = day_str + " ".join(part[:index_month + 1]) + " " + month + year_str
            elif year and 1 <= int(year) <= 9999:
                sentence = day_str + month_str + " ".join(part[:index_year + 1]) + " " + year
                if not sentence.startswith("năm "):
                    is_correct_date = False
            else:
                is_correct_date = False
            while "  " in sentence: sentence = sentence.replace("  ", " ")
            if not is_correct_date and not is_correct_hour:
                for word in part:
                    if word == "năm": word = "năm_date"
                    result.append((word, "O"))
            else:
                result.append((sentence.strip(), label))
        elif label == "PERC":
            if sentence.endswith(" phần trăm"):
                number = sentence.split(" phần trăm")[0]
                ans = read_last(number)
                if ans: sentence = ans + "%"
            result.append((sentence, label))
        elif label == "MISC":
            is_correct_sentence = False
            for name, _metric in list_metric.items():
                for metric in _metric:
                    if sentence.endswith(metric):
                        number = sentence.split(" " + metric)[0]
                        ans = read_last(number)
                        if ans:
                            # fix MISC for hour and minute
                            if metric == "giờ" or metric == "phút":
                                if metric == "phút" and index > 0 and list_words[index - 1][1] == "DATE" \
                                        and list_words[index - 1][0].endswith(" giờ"):
                                    list_words[index - 1] = (
                                        list_words[index - 1][0] + " " + list_words[index][0], "DATE")
                                    list_words[index] = ("", "")
                                else:
                                    list_words[index] = (sentence, "DATE")
                                return _get_ans(list_words)
                            sentence = ans + name
                            is_correct_sentence = True
                            break
                if is_correct_sentence: break
            if not is_correct_sentence:
                for name, _metric in list_special_string.items():
                    for metric in _metric:
                        if sentence.startswith(metric + " "):
                            number = sentence.split(metric + " ")[1]
                            ans = read_last(number)
                            if ans:
                                sentence = name + ans
                                is_correct_sentence = True
                                break
                    if is_correct_sentence: break
            if not is_correct_sentence:
                for name, _metric in list_static_string.items():
                    for metric in _metric:
                        if sentence == metric:
                            sentence = name
            if not is_correct_sentence:
                label = "O"
                for word in sentence.strip().split(" "):
                    result.append((word, label))
            else:
                result.append((sentence.strip(), label))
        elif label == "CAP":
            words = sentence.split(" ")
            sentence = " ".join(x[0].upper() + x[1:].lower() if len(x) > 1 else x.upper() for x in words)
            result.append((sentence, label))
        elif label == "O":
            if sentence == "giờ" and index > 0 and index < len(list_words) - 1:
                sentence_prev, label_prev = list_words[index - 1]
                sentence_next, label_next = list_words[index + 1]
                if label_next == "DATE" and sentence_next.endswith("phút") and label_prev == "NUMB":
                    sentence = sentence_prev + " " + sentence + " " + sentence_next
                    list_words[index] = (sentence, "DATE")
                    list_words[index - 1] = (sentence_prev, "")
                    list_words[index + 1] = (sentence_next, "")
                    return _get_ans(list_words)
            result.append((sentence, label))
        else:
            result.append((sentence + label, "O"))
        index += 1
    print("result", result)
    return post_of_post_processing(result)


list_vietnamese_rimes = ['a', 'e', 'i', 'o', 'u', 'y', 'oa', 'oe', 'ue', 'uy',
                         'ia', 'ua', 'uya',
                         'ai', 'oi', 'ui', 'oai', 'uoi',
                         'ao', 'eo', 'oao', 'oeo',
                         'au', 'eu', 'iu', 'uu', 'ieu', 'uou', 'uyu', 'yeu',
                         'ay', 'oay', 'uay',
                         'am', 'em', 'im', 'om', 'um', 'iem', 'oam', 'oem', 'uom', 'yem',
                         'an', 'en', 'in', 'on', 'un', 'ien', 'oan', 'oen', 'uan', 'uon', 'uyen', 'yen',
                         'ang', 'eng', 'ong', 'ung', 'ieng', 'oang', 'oong', 'uang', 'uong', 'yeng',
                         'anh', 'enh', 'inh', 'oanh', 'uenh', 'uynh',
                         'ach', 'ech', 'ich', 'oach', 'uech', 'uych',
                         'ac', 'ec', 'ic', 'oc', 'uc', 'iec', 'oac', 'ooc', 'uoc',
                         'at', 'et', 'it', 'ot', 'ut', 'iet', 'oat', 'oet', 'uat', 'uot', 'uyt', 'uyet', 'yet',
                         'ap', 'ep', 'ip', 'op', 'up', 'iep', 'oap', 'uop', 'uyp']

list_vietnamese_onset = ['b', 'd', 'h', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'x',
                         'tr', 'th', 'ch', 'ph', 'nh', 'kh', 'gi', 'gu',
                         'ngh', 'ng', 'gh', 'g', 'k', 'c', '']


def is_vietnamese_syllable(str):
    list_tab = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"
    for character in list_tab:
        if character in str:
            return True
    for onset in list_vietnamese_onset:
        if str.startswith(onset) and str[len(onset):] in list_vietnamese_rimes:
            return True
    return False


list_post_of_post_processing_misc = {
    "vtv" : "VTV",
    "h5n" : "H5N",
    "vov" : "VOV",
    "vtc" : "VTC",
    "sctv": "SCTV",
    "pc"  : "PC",
    "u-"  : "U",
    "u."  : "U",
    "u"   : "U",
    "s"   : "S"
}


def post_of_post_processing(list_sentence):
    all_words = []
    for index in range(len(list_sentence)):
        sentence, label = list_sentence[index]
        if label == "CAP":
            words = sentence.split(" ")
            for i in range(len(words)):
                if not is_vietnamese_syllable(words[i].lower()):
                    if len(words) == 1 and len(words[i]) <= 5:
                        # if (index == 0 and list_sentence[index + 1][1] != "CAP") or (
                        #         index == len(list_sentence) - 1 and list_sentence[index - 1][1] != "CAP") or (
                        #         list_sentence[index - 1][1] != "CAP" and list_sentence[index + 1][1] != "CAP"):
                        words[i] = words[i].upper()
            sentence = " ".join(words)
        elif label == "MISC":
            if sentence.endswith("hz") and index < len(list_sentence) - 1 and list_sentence[index + 1] == ("ta", "O"):
                sentence = sentence[:-2] + "ha"
                list_sentence[index + 1] = ("", "")
            else:
                for data, value in list_post_of_post_processing_misc.items():
                    if sentence.startswith(data):
                        sentence = value + sentence[len(data):]
                        break
        list_sentence[index] = (sentence, label)
        all_words.append(sentence)

    # print("\n".join(str(x) for x in list_sentence))
    list_words = []
    index = 0
    n = 0
    while index < len(all_words):
        sentence, label = list_sentence[index]
        is_checked = False
        if label == "NUMB":
            value = ""
            for word in sentence.split(" "):
                ans = get_word_from_list_read_series(word)
                if ans:
                    value += ans
                else:
                    value += " " + word + " "
            value = value.replace("  ", " ").strip()
            if n == 0:
                list_words.append([(sentence, value)])
            else:
                list_words[-1].append((sentence, value))
            n += 1
            is_checked = True
        elif label == "O" and sentence != "năm":
            if sentence == "năm_date": all_words[index] = "năm"
            for k in range(2):
                word = " ".join(all_words[index: index + 2 - k])
                value = get_word_from_list_read_series(word)
                if value:
                    if n == 0:
                        list_words.append([(word, value)])
                    else:
                        list_words[-1].append((word, value))
                    n += 1
                    index += 1 - k
                    is_checked = True
                    break
        elif label == "MISC" or label == "CAP":
            is_checked = True
            words = sentence.lower().split(" ")
            for word in words:
                value = get_word_from_list_read_series(word)
                if value:
                    if n == 0:
                        list_words.append([(sentence, value)])
                    else:
                        list_words[-1].append((sentence, value))
                    n += 1
                else:
                    is_checked = False
                    break

        if not is_checked and len(all_words[index]) > 0:
            n = 0
            list_words.append([(all_words[index], False)])
        index += 1
    ans = []
    for index in range(len(list_words)):
        words = list_words[index]
        if len(words) > 2:
            value = ""
            for i in range(len(words)):
                if words[i][1] == "x":
                    if i < len(words) - 1 and words[i + 1][1] not in dict_digit:
                        value += "10"
                    else:
                        value += "1"
                else:
                    value += words[i][1]
            ans.append(value)
        elif len(words) == 2:
            is_fixed = False
            # fix : "một nghìn năm trăm"
            # before : "1000500"
            # after : "1500"
            read_numb_1, can_read_1 = string_to_numb(words[0][1])
            read_numb_2, can_read_2 = string_to_numb(words[1][1])

            if can_read_1 and can_read_2 and (read_numb_1 >= 1000 or read_numb_2 >= 1000):
                ans.append(str(read_numb_1 + read_numb_2))
                is_fixed = True
            if not is_fixed:
                ans.append("".join([x[1] for x in words]))
        else:
            if all(x.isdigit() or x == "x" or x.isupper() for x in words[0][0]):
                s = ""
                k = 0
                while k < len(words[0][0]):
                    c = words[0][0][k]
                    next_c = words[0][0][k + 1] if k + 1 < len(words[0][0]) else False
                    if c == "x":
                        if next_c and next_c == "x":
                            s += "10"
                        elif not next_c:
                            s += "10"
                        else:
                            s += "1"
                    else:
                        s += c
                    k += 1
                ans += [s]
            else:
                ans += [x[0] for x in words]
    print(ans)

    # custom for marriott presentation
    # print("custom marriott: ")
    new_ans = []
    for index in range(len(ans)):
        word = ans[index]
        new_ans += word.split(" ")

    new_ans_2 = []
    index = 0
    while index < len(new_ans):
        is_checked = False
        for k in range(3, 1, -1):
            if index + k <= len(new_ans):
                word = " ".join(new_ans[index:index + k]).lower()
                if word in list_vietnamese_local:
                    new_ans_2.append(list_vietnamese_local[word])
                    index += k - 1
                    is_checked = True
                    break
        if not is_checked:
            new_ans_2.append(new_ans[index])
        index += 1

    new_ans_3 = []
    index = 0
    while index < len(new_ans_2):
        word = new_ans_2[index]
        if word == "số" and index < len(new_ans_2) - 2:
            next_word = new_ans_2[index + 1]
            next_next_word = new_ans_2[index + 2].decode('utf-8')
            if next_word.isdigit() and next_next_word[0].isalpha() and next_next_word[0].isupper():
                index += 1
                continue
        new_ans_3.append(word)
        index += 1
    ans = new_ans_3
    # done

    result = " ".join(ans).replace("mồng mùng", "mồng")
    return result

# with open('list_vietnamese_local.json', 'r') as f:
with open('list_vietnamese_local.json', 'r') as f:
    list_vietnamese_local = json.load(f)
    list_vietnamese_local = {x.encode('utf-8'): y.encode('utf-8') for x, y in list_vietnamese_local.items()}


def string_to_numb(s):
    try:
        return int(s), True
    except ValueError:
        return -1, False


# it will be removed if STT model is good enough
list_abbreviations = {
    "FPT"      : ["ép pi ti", "ép pê tê"],
    "Galaxy"   : ["ga la xi"],
    "Samsung"  : ["xam xung"],
    "Xiaomi"   : ['xi ao mi'],
    "GB"       : ['ghi ga bai', 'gi ga bai'],
    "Gb"       : ['ghi ga bít', 'gi ga bít'],
    # "Viettel" : ["việt theo", "việt ten"],
    "Vinaphone": ["vi na phôn"],
    # "gi": ["ghi"],
    "dota"     : ["đô ta"],
    "dota2"    : ["đô ta hai"],
    "Mobifone" : ["mô bi phôn"],
    "THCS"     : ["trung học cơ sở"],
    "THPT"     : ["trung học phổ thông"],
    # "Vietnamobile" : ["việt nam mô bai"],
    # "Iphone" : ["ai phôn"],
    # "Ipad" : ["ai pát"],

}


def pre_of_post_processing(sentence):
    for word, x in list_abbreviations.items():
        for _x in x:
            sentence = sentence.replace(_x, word)
    words = sentence.split(" ")
    for index in range(len(words)):
        if index > 0 and words[index] == "nhăm" and words[index - 1] in numb_x2:
            words[index] = "lăm"
        if 0 < index < len(words) - 1 and words[index] == "lẻ" and (
                words[index + 1] in numb_x1 or words[index + 1] == "mười"):
            words[index] = "linh"
        if index < len(words) - 1 and words[index] == "mồng" and (
                words[index + 1] in numb_x1 or words[index + 1] == "mười"):
            words[index] = "mồng mùng"
    list_words = []
    n = 0
    index = 0
    while index < len(words):
        sentence = words[index]
        value = get_word_from_list_read_series(sentence)
        if value:
            if n == 0:
                list_words.append([(sentence, value)])
            else:
                list_words[-1].append((sentence, value))
            n += 1
        else:
            list_words.append([(sentence, value)])
            n = 0
        index += 1
    output = []
    for sentence in list_words:
        if len(sentence) >= 6:
            output.append("".join([x[1] for x in sentence]))
        else:
            output.append(" ".join([x[0] for x in sentence]))
    # print("\n".join([str(x) for x in output]))
    return " ".join(output)


list_read_series = {
    "A": ["a"],
    "B": ["bê", "bờ"],
    "C": ["xê", "cờ"],
    "D": ["đê", "đê"],
    "E": ["e"],
    "F": ["ép"],
    "G": ["gờ"],
    "H": ["hắt"],
    "I": ["i"],
    "J": ["di"],
    "K": ["ca"],
    "L": ["lờ"],
    "M": ["mờ", "em mờ"],
    "N": ["nờ", "en nờ"],
    "O": ["o", "ô"],
    "P": ["pê"],
    "Q": ["qui"],
    "R": ["rờ"],
    "S": ["ét", "ét xì", "ét xi", "sờ"],
    "T": ["tê"],
    "U": ["u"],
    "V": ["vê"],
    "X": ["ích", "ích xì", "ích xi"],
    "W": ["vê kép"],
    "Y": ["y"],
    "Z": ["dét"],
    "1": ["một"],
    "2": ["hai"],
    "3": ["ba"],
    "4": ["bốn", "tư"],
    "5": ["năm"],
    "6": ["sáu"],
    "7": ["bảy", "bẩy"],
    "8": ["tám"],
    "9": ["chín"],
    "0": ["không"],
    ".": ["chấm"],
    "-": ["gạch ngang"],
    ",": ["phẩy"],
    # ":": ["hai chấm"],
    # "...": ["ba chấm"],
    "x": ["mười"]  # special case 1

}


def get_word_from_list_read_series(str):
    for name in list_read_series:
        for value in list_read_series[name]:
            if value == str:
                return name
    return False


if __name__ == "__main__":
    # run_vlsp()
    print(pre_of_post_processing("hôm nay là mồng tám tháng ba năm chín bảy"))
    list_syllabels = [
        ("tôi", "O"),
        # ("hai năm ba không", "B-DATE"),
        ("ở", "O"),
        ("sốvxcvxcv", "B-,"),
        ("mười bảy", "B-NUMB"),
        ("duy tân", "B-CAP"),
        ("hà nội", "B-CAP"),
        # ("x năm tám không tám bảy không năm", "B-DATE"),
        # ("tê", "O"),
        # ("vê tê xê", "B-MISC"),
        # ("xêx", "O"),
        # ("ba mươi héc", "B-MISC"),
        # ("ta", "O"),
        # ("ba", "O"),
        # ("u hai ba", "B-MISC"),
        # ("nghìn", "B-NUMB"),
        # ("trần thị kim oanh", "B-CAP"),
        # ("fpt", "B-CAP"),
        ("o số", "O"),
        ("tám", "B-NUMB"),
        ("điện biên phủ cùng với mẹ", "O"),
        # ("năm trăm", "B-NUMB"),
        # ("fpt", "B-CAP"),
        # ("vê tê bê vê", "O"),
        # ("ba", "B-NUMB")
    ]
    print(get_ans(list_syllabels))
    # print(is_vietnamese_syllable("nam"))
    # print(get_number_from_hundred_str("hai lăm"))
    # print(read_last("hai ba bốn năm a bê xê"))
    # print(read_first("hai ba bốn năm a bê xê"))
