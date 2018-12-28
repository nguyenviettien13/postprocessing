# encoding: utf-8
# Read numb
import datetime
import json
import re
from random import random
from re import split

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
    'c': ["xê", "cờ"],
    'd': ["đê", "dờ"],
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
    'o': ["ô", "o"],
    'p': ["pê", "pờ"],
    'q': ["quy", "qờ"],
    'r': ["rờ"],
    's': ["ét", "sờ"],
    't': ["tê", "tờ"],
    'u': ["u"],
    'v': ["vê", "vờ"],
    'w': ["vê kép", "đáp bờ liu"],
    'x': ["ích", "xờ"],
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
                other_result.append((a_ + " tỉ " + b_).strip())
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
        else:
            return False
    if len(list_read) > 0:
        return ' '.join(list_read)
    else:
        return False



english_vietnam_list_read_series = {
    "A": ["a", "êi"],
    "B": ["bê", "bờ", "bi"],
    "C": ["xê", "cờ", "xi"],
    "D": ["đê", "dờ", "đi"],
    "E": ["e", "i"],
    "F": ["ép"],
    "G": ["gờ", "ri", "di"],
    "H": ["hắt", "hát", "ết"],
    "I": ["i", "ai"],
    "J": ["di"],
    "K": ["ca", "cây"],
    "L": ["lờ", "eo"],
    "M": ["mờ", "em mờ", "em"],
    "N": ["nờ", "en nờ", "en"],
    "O": ["o", "ô", "âu"],
    "P": ["pê", "pi"],
    "Q": ["qui", "ciu"],
    "R": ["rờ", "a"],
    "S": ["ét", "ét xì", "ét xi", "sờ"],
    "T": ["tê", "ti"],
    "U": ["u", "iu"],
    "V": ["vê", "vi"],
    "X": ["ích", "ích xì", "ích xi"],
    "W": ["vê kép", "vê đúp"],
    "Y": ["y", "goai"],
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
#Convert spelling of character to symbol
#Example: ép - > F
def convert_word_character(word):
    for symbol, spelling in english_vietnam_list_read_series.items():
        if word in spelling:
            return symbol
    return False


#Convert "ép pi ti" to "FPT"
def cap_to_abbreviation(string_abrreviation):
    #Buoc 1: Chia các từ thành các cụp "vê kép hát ô" -> ["vê kép", "hát", "ô"]
    word_set = []
    word_set_after_combine = []
    word_set = string_abrreviation.split()
    idx = 0;
    while(idx < len(word_set)):
        curr_word = word_set[idx]
        next_word = ""
        couple_word =""
        try:
            next_word = word_set[idx+1]
            couple_word = curr_word + " " + next_word
        except:
            word_set_after_combine.append(curr_word)
            break

        flag  = False
        for symbol, spelling in english_vietnam_list_read_series.items():
            if couple_word in spelling:
                flag = True
                break
        if flag:
            word_set_after_combine.append(couple_word)
            idx += 1
        else:
            word_set_after_combine.append(curr_word)
        idx += 1


    cap_character_set = []
    for word in word_set_after_combine:
        cap_character = convert_word_character(word)
        if  cap_character == False:
            return False
        else:
            cap_character_set.append(cap_character)
    return "".join(cap_character_set)


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
    ans = is_integer_number(n) or is_positive_float_number(n) or is_negative_float_number(n)
    if ans:
        return [[(x, "NUMB")] for x in ans]
    else:
        return False


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
                            other_result.append([("ngày {} tháng {} năm {}".format(day_, month_, year_), "DATE")])
                            other_result.append([("mùng {} tháng {} năm {}".format(day_, month_, year_), "DATE")])
                            other_result.append([("mồng {} tháng {} năm {}".format(day_, month_, year_), "DATE")])
                            other_result.append([("hôm {} tháng {} năm {}".format(day_, month_, year_), "DATE")])
                            if month_ == "bốn":
                                other_result.append([("ngày {} tháng {} năm {}".format(day_, "tư", year_), "DATE")])
                                other_result.append([("mùng {} tháng {} năm {}".format(day_, "tư", year_), "DATE")])
                                other_result.append([("mồng {} tháng {} năm {}".format(day_, "tư", year_), "DATE")])
                                other_result.append([("hôm {} tháng {} năm {}".format(day_, "tư", year_), "DATE")])
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
                        other_result.append([("ngày {} tháng {}".format(day_, month_), "DATE")])
                        other_result.append([("mùng {} tháng {}".format(day_, month_), "DATE")])
                        other_result.append([("mồng {} tháng {}".format(day_, month_), "DATE")])
                        other_result.append([("hôm {} tháng {}".format(day_, month_), "DATE")])
                        if month_ == "bốn":
                            other_result.append([("ngày {} tháng {}".format(day_, "tư"), "DATE")])
                            other_result.append([("mùng {} tháng {}".format(day_, "tư"), "DATE")])
                            other_result.append([("mồng {} tháng {}".format(day_, "tư"), "DATE")])
                            other_result.append([("hôm {} tháng {}".format(day_, "tư"), "DATE")])
                return other_result
    return False


def is_short_datetime_type_2(n):
    parts = n.split("/" if "/" in n else "-")
    if len(parts) == 2:
        MM = parts[0]
        yyyy = parts[1]
        if len(MM) == 1: MM = "0" + MM
        if len(MM) == 2 and len(yyyy) == 4 and yyyy >= "1000":
            ans = is_valid_date(MM + "/" + yyyy, '%m/%Y')
            if ans:
                other_result = []
                for month_ in read_number(ans.month):
                    for year_ in read_number(ans.year):
                        other_result.append([("tháng {} năm {}".format(month_, year_), "DATE")])
                        if month_ == "bốn":
                            other_result.append([("tháng {} năm {}".format("tư", year_), "DATE")])
                return other_result
    return False


def is_currency(n):
    str = n.lower()
    for symbols, reading in list_currency_symbols.items():
        if str.endswith(symbols):
            str = str[:-len(symbols)]
            ans = is_number(str)
            if ans:
                other_result = []
                for x in ans:
                    other_result.append([x[0], (reading, "O")])
                return other_result
    return False


def is_percentage(n):
    ans = is_number(n[:-1])
    if len(n) > 1 and n[-1] == '%' and ans:
        other_result = []
        for x in ans:
            other_result.append([x[0], ("phần trăm", "O")])
        return other_result
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
        return all(re.fullmatch(r"[0-9]", x) for x in y) and [[(x, "NUMB")] for x in read_character(n)]


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


# def is_short_form_number(n):
#     parts = n.split('k')
#     if len(parts) == 2 and is_positive_integer_number(n.replace('k', '')):
#         other_result = []
#         for part0_ in read_number(parts[0]):
#             for part1_ in read_number(parts[1]):
#                 other_result.append([' '.join([part0_, "nghìn", part1_]).strip(), "NUMB"])
#         return other_result


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
                    other_result.append([(hour_ + " giờ " + minute_ + " phút", "DATE")])
                    # other_result.append([(hour_ + " tiếng " + minute_ + " phút", "DATE")])
                    other_result.append([(hour_ + " giờ " + minute_, "DATE")])
            return other_result
    except Exception:
        pass
    return False


def is_metric(n):
    if n.count("m") == 1:
        part = n.split("m", 1)
        if len(part) == 2:
            read_1 = read_number(part[0])
            read_2 = read_number(part[1])
            other_result = []
            if read_1 and read_2:
                for part0_ in read_1:
                    for part1_ in read_2:
                        other_result.append([(part0_, "NUMB"), ("mét", "O"), (part1_, "NUMB")])
                        # other_result.append(' '.join([part0_, "mét", part1_]).strip())
                return other_result
    for metric, name in list_metric.items():
        number = is_number(n[:-len(metric)])
        if n.endswith(metric) and number:
            other_result = []
            for x in number:
                for y in name:
                    other_result.append([x[0], (y, "O")])
            return other_result
    if any(x.isdigit() for x in n) and n in list_metric:
        return [[(x, "O")] for x in list_metric[n]]
    return False


list_currency_symbols = {'₽'   : 'rúp',
                         '$'   : 'đô la',
                         '£'   : 'pao',
                         '¥'   : 'yên',
                         '₭'   : 'kíp',
                         '₩'   : 'won',
                         '฿'   : 'bát',
                         '€'   : 'euro',
                         '₫'   : 'đồng',
                         '₿'   : 'bitcoin',
                         "vnd" : 'việt nam đồng',
                         "vnđ" : 'việt nam đồng',
                         "đ"   : 'đồng',
                         "dola": 'đô la',
                         "euro": 'euro'
                         }


list_metric = {"kg"         : ["ki lô gam", "ki lô gờ gam"],
               "g"          : ["gam"],
               # "g": ["gờ"],  # Custom: 3G, 4G, 5G, ...
               "%"          : ["phần trăm"],
               "m"          : ["mét"],
               "m2"         : ["mét vuông"],
               "m3"         : ["mét khối"],
               "km"         : ["ki lô mét"],
               "km2"        : ["ki lô mét vuông"],
               "ml"         : ["mi ni lít", "mi li lít"],
               "km/s"       : ["ki lô mét trên giây"],
               "gb"         : ["gi ga bai", "ghi ga bai"],
               "ft"         : ["phít"],
               # "h"          : ["giờ"],
               # "ts": ["tê ét"],
               "m/s"        : ["mét trên giây"],
               # "đ/sms": ["đồng trên ét em ét", "đồng trên một ét em ét"],
               # "đ/phút": ["đồng trên phút", "đồng trên một phút"],
               "mb"         : ["mê ga bai", "mờ bê", "mê ga bít"],
               "kbps"       : ["ki lô bít trên giây", "ki lô bai trên giây"],
               "mb/phút"    : ["mê ga bai trên phút", "mê ga bít trên phút"],
               "ms"         : ["mi li giây", "mi ni giây"],
               "gb/ngày"    : ["gi ga bai trên ngày", "ghi ga bai trên ngày"],
               "mm"         : ["mi li mét", "mi ni mét"],
               "h/tuần"     : ["giờ trên tuần"],
               "cm"         : ["xen ti mét", "sen ti mét"],
               # "usd/tuần": ["u ét đê trên tuần", "đô la trên tuần", "iu ét đê trên tuần", "iu ét đi trên tuần"],
               "m2sàn/người": ["mét vuông sàn trên người"],
               # "/nq-cp": ["nghị quyết chính phủ"],
               # "/qđ-syt": ["quyết định sở y tế"],
               "km/h"       : ["ki lô mét trên giờ"],
               "kb/s"       : ["ki lô bai trên giây", "ki lô bít trên giây"],
               # "/qđ-ubnd": ["quyết định ủy ban nhân dân"],
               "%/cổ"       : ["phần trăm trên một cổ", "phần trăm trên cổ"],
               # "ph"         : ["phút"],
               "ha"         : ["héc ta", "hét ta"],
               # "đồng/m3": ["đồng trên mét vuông", "đồng trên 1 mét vuông"],
               # "m3/ngày": ["mét vuông trên ngày", "mét vuông trên một ngày"],
               "gr"         : ["gờ ram"],
               # "đ/học": ["đồng trên một lần học"],
               # "usd/1kg": ["u ét đê trên một ki lô gam"],
               # "/qđ-bhxh": ["quy định bảo hiểm xã hội"],
               "mp"         : ["mê ga pixel"],
               "oc"         : ["độ xê", "độ sê"],
               "mbps"       : ["mê ga bít trên giây", "mê ga bai trên giây"],
               "px"         : ["pixel"],
               # "usd": ["u ét đê", "đô la"],
               # "/cp": ["trên 1 cổ phiếu"],
               # "%/năm": ["phần trăm trên năm", "phần trăm trên 1 năm"],
               "hz"         : ["héc"],
               "inch"       : ["inh"]
               }

# normalize không dùng đến cái này
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


# list_static_string = {
#     "3.0": ["ba chấm không"],
#     "4.0": ["bốn chấm không"],
#     "3d": ["ba đê"],
#     "24/24": ["hai tư trên hai tư", "hai bốn trên hai bốn"],
#     "24/7": ["hai tư trên bảy", "hai tư trên bẩy"],
#     "m/s2": ["mét trên giây bình phương"],
#     "802.11": ["tám không hai chấm mười một", "tám không hai chấm một một"],
#     "6/55": ["sáu trên năm lăm"],
#     "6/45": ["sáu trên bốn lăm"],
#     "4.7": ["bốn phẩy bẩy", "bốn phẩy bảy", "bốn chấm bẩy", "bốn chấm bảy"],
#     "t.ư": ["trung ương"],
#     "ubnd": ["ủy ban nhân dân"],
#     "pccc": ["phòng cháy chữa cháy"],
#     "tq": ["trung quốc"],
#     "lđbđ": ["liên đoàn bóng đá"],
#     "sn": ["sinh năm"],
# }


# def is_special_string(n):
#     for x in list_special_string:
#         if n.startswith(x):
#             number = is_positive_integer_number(n[len(x):])
#             if number:
#                 return [z + " " + y for y in number for z in list_special_string[x]]
#     if n in list_special_string:
#         return [x for x in list_special_string[n]]
#     elif n in list_static_string:
#         return [x for x in list_static_string[n]]
#     else:
#         return False


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
    if n.startswith(":") or n.startswith("+"):
        n = n[1:]
    if n.endswith(",") or n.endswith("."):
        n = n[:-1]
    return n


# list_function = [is_metric, is_time, is_short_form_number, is_email, is_url, is_phone_number, is_license_plate,
#                  is_percentage, is_currency, is_short_datetime_type_1, is_short_datetime_type_2, is_long_datetime,
#                  is_number, is_special_string]

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
                    for year_ in read_number(ans.year):
                        other_result.append("{} năm {}".format(month_, year_))
                        if month_ == "bốn":
                            other_result.append("{} năm {}".format("tư", year_))
                return other_result
    return False


def convert(n):
    return str(n) if n else "_"


try:
    with open('/test/NLP_postprocessing.tmp/list_abbreviation_words.json', 'r') as f:
        list_abbreviation_words = json.load(f)
    with open('/test/NLP_postprocessing.tmp/list_correct_words.json', 'r') as f:
        list_correct_words = json.load(f)
except:
    pass

list_numb_label = [
    "không", "một", "mốt", "hai", "ba", "bốn", "tư", "năm", "nhăm", "lăm", "sáu", "bảy", "bẩy", "tám", "chín", "mười",
    "mươi", "linh", "lẻ", "chục", "nghìn", "ngàn", "triệu", "tỷ", "phẩy", "phảy"
]

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


def format_number(value, is_positive, format_numb, focus = False):
    if format_numb and (focus or int(value) >= 10000):
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
    # ghép begin và inner -> một

    #tien: Combine components into one
    list_words = []
    for word, label in list_syllabels:
        # word = word.encode('utf-8') #turn it on if error
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

    #return _get_ans(list_words)
    return my_get_answer(list_words)

#list_words: set of words, each word still has content and relative label
def _get_ans(list_words):
    #sentence_split = " ".join([x.replace(" ", "_") for x, y in list_words])
    #print(sentence_split)
    #print("\n".join([str(x) for x in list_words]))
    result = []
    index = 0
    while index < len(list_words):
        # for index in range(len(list_words)):
        sentence, label = list_words[index]
        if label == "NUMB":
            # đổi chữ thành số
            read_numb = sentence_to_numb(sentence)
            if read_numb:
                result.append((str(read_numb), label))
            else:
                words = sentence.split(" ")
                is_correct = True
                all_word = []
                for word in words:
                    ans = read_first(word)
                    if ans:
                        all_word.append(ans)
                    else:
                        is_correct = False
                        break
                if is_correct:
                    result.append(("".join(all_word), label))
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
                    if len(ans_hour) == 1: ans_hour = "0" + ans_hour
                    if len(ans_all_minute) == 1: ans_all_minute = "0" + ans_all_minute
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

            if not day: day_str = " ngày " + day_str + " "
            if not month: month_str = " tháng " + month_str + " "
            if not year: year_str = " năm " + year_str + " "
            # print(day_str, day)
            # print(month_str, month)
            # print(year_str, year)
            if day and month and year:
                sentence = " ".join(part[:index_day + 1]) + " %s/%s/%s" % (day, month, year)
            elif day and 1 <= int(day) <= 31 and month and 1 <= int(month) <= 9999:
                if int(month) > 12:
                    words_month = month_str.split(" ", 1)
                    month = sentence_to_numb(words_month[0])
                    if len(month) == 1: month = "0" + month
                    # next_words_month = read_last(words_month[1])
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
            result.append((sentence, "O"))
            result.append((str(label), "O"))
        index += 1
    phrase_set = []
    for phrase in result:
        phrase_set.append(phrase[0])
    print("Debug: "+ " ".join(phrase_set))
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
normal_word_2_correct_form_dictionary = {
    "pháp luật"         : "Pháp luật",
    "tòa án nhân dân"   : "Tóa án Nhân dân"
}

#ham my_get_answer thay thế cho hàm _get_ans
def my_get_answer(list_sentence):
    #Buoc 1: Xu ly cac tu viet hoa
    all_words_after_process_cap = []
    for index in range(len(list_sentence)):
        sentence, label = list_sentence[index]
        # xử lý tên viết hoa
        if label == "CAP":
            #Trường hợp viết hoa theo mẫu có sẵn
            if sentence.lower() in normal_word_2_correct_form_dictionary.keys():#check cac tu viet hoa co trong tu dien
                # pháp luật -> Pháp luật
                sentence = normal_word_2_correct_form_dictionary[sentence.lower()]
                all_words_after_process_cap.append((sentence, label))
            #trường hợp viết hoa các từ
            elif cap_to_abbreviation(sentence):
                # vê en nờ lai xê đê e: VNCDE
                all_words_after_process_cap.append((cap_to_abbreviation(sentence), label))
            else:
                #Tu viet hoa duoc cau tao boi nhieu tu khac nhau
                words = sentence.split(" ")
                sentence = " ".join(x[0].upper() + x[1:].lower() if len(x) > 1 else x.upper() for x in words)
                all_words_after_process_cap.append((sentence, label))
        else:
            all_words_after_process_cap.append((sentence, label))

    # Chu thuong -> Chu hoa su dung tu dien trong file lo-up_EngDictionary.txt
    #loading dictionary
    lo_up_English_dictionary = {}
    with open("lo-up_EngDictionary.txt", 'r') as f:
        line = f.readline()
        while (line):
            lowcase, uppercase = line.split("\t", 1)
            uppercase = uppercase.strip()
            lo_up_English_dictionary.update({lowcase : uppercase})
            line = f.readline()


    all_words_after_use_lo_up_EngDictionary =[]
    for word, label in all_words_after_process_cap:
        if word in lo_up_English_dictionary.keys():
            uppercaseWord = lo_up_English_dictionary.get(word)
            all_words_after_use_lo_up_EngDictionary.append((uppercaseWord, label))
        else:
            all_words_after_use_lo_up_EngDictionary.append((word, label))


    #Xu ly ngay thang
    all_words_after_process_date = [];
    for phrase, label in all_words_after_use_lo_up_EngDictionary:
        if label == "DATE":
            #nếu date là mười giờ hai mượi phút mười chín giây
            time = ""
            if "giờ" in phrase:
                hour, rest = phrase.split("giờ", 1)
                hour = sentence_to_numb(hour.strip())
                if len(hour) == 1: hour = "0"+hour
                time+= hour
                if "phút" in rest:
                    minute, rest = rest.split("phút", 1)
                    minute = sentence_to_numb(minute.strip())
                    if len(minute) ==1: minute= "0"+minute
                    time+=":"+minute
                    if "giây" in rest:
                        second = rest.split("giây")[0]
                        second = sentence_to_numb(second)
                        time+= ":"+ second
                all_words_after_process_date.append((time, label))
            #Xu ly voi date
            #Truong hop date: long date "ngày hai mươi tư tháng tám năm hai ngàn không trăm mười bốn"
            date = ""
            start_date_candidate = [""]
            rest = ""
            if "năm" in phrase:
                rest, year = phrase.split("năm", 1);
                year = sentence_to_numb(year.strip())
                date += year
                start_date_candidate.append("năm")
            else:
                pass
            if "tháng" in phrase:
                rest, month = rest.split("tháng",1)
                month = sentence_to_numb(month.strip())
                if len(month) == 1: month= "0"+ month
                if len(date) ==0:
                    date = month
                else:
                    date = month +"/" + date
                start_date_candidate.append("tháng")

            if len(rest.strip()) > 0:
                pre_noon_days = ["sáng sớm", "rạng sáng", "tờ mờ",
                         "chiều muộn", "chiều tối",
                         "tối muộn", "tối muộn", "nửa đêm", "nửa đêm",
                         "sớm", "sáng", "trưa", "chiều", "tối", "đêm"
                         ]
                pre_days = [ "ngày", "mùng", "mồng", "hôm"]
                start_day = ""
                start_days = []
                for pre_noon_day in pre_noon_days:
                    for pre_day in pre_days:
                        start_day_element = pre_noon_day + " " + pre_day
                        start_days.append(start_day_element)

                for pre_noon_day in pre_noon_days:
                    start_days.append(pre_noon_day)
                for pre_day in pre_days:
                    start_days.append(pre_day)
                start_days.append("")
                #Debug
                # for a in start_days:
                #     print(a)
                for start_day_element in start_days:
                    if rest.startswith(start_day_element):
                        start_day = start_day_element
                        start_date_candidate.append(start_day_element)
                        break

                day = ""
                if start_day == "":
                    day = rest
                else:
                    day = rest.split(start_day,1)[1]
                day = sentence_to_numb(day.strip())
                if len(day) == 1: day = "0" + day
                if len(date) == 0:
                    date = day
                else:
                    date = day +"/" + date
            date = start_date_candidate[-1] + " " + date
            all_words_after_process_date.append((date, label))
        else:
            all_words_after_process_date.append((phrase, label))


    #Xử lý số
    all_words_after_process_number = [];
    for phrase, label in all_words_after_process_date:
        if label == "NUMB":
            phrase = sentence_to_numb(phrase)
            all_words_after_process_number.append((phrase, label))
        else:
            all_words_after_process_number.append((phrase, label))

    # gop cac tu cung loại liên tiếp vào với nhau
    all_words_after_process_combine = []
    previous_label = "Initial"
    idx = 0;
    while(idx < len(all_words_after_process_date)):
        curr_word, curr_label = all_words_after_process_number[idx]
        if curr_label == previous_label:
            corpus = all_words_after_process_combine[-1][0] + " " + curr_word
            all_words_after_process_combine = all_words_after_process_combine[:-1]
            all_words_after_process_combine.append((corpus, curr_label))
        else:
            all_words_after_process_combine.append((curr_word, curr_label))
        previous_label = curr_label
        idx += 1


    #Xử lý các trường hợp đặc biệt
    #xử lý metric: number + metric = number+ abbreviation of metric
    sufficient_to_symbol_list_currency_symbols = [
            ('rúp'           , '₽'),
            ('đô la sing'    ,'$Singapore'),
            ('đô la'         , '$'),
            ('pao'           , '£'),
            ('yên'           , '¥'),
            ('kíp'           , '₭'),
            ('won'           , '₩'),
            ('bát'           , '฿'),
            ('euro'          , '€'),
            ('đồng'          , '₫'),
            ('bitcoin'       , '₿'),
            ('việt nam đồng' , "vnd"),
            ('việt nam đồng' , "vnđ"),
            ('euro'          , "euro")
    ]
    sufficient_to_symbols_list_metric = [
            ("ki lô gam"                         , "kg"        ),
            ("ki lô gờ gam"                      , "kg"        ),
            ("gam"                               , "g"         ),
            ("gờ"                                , "g"         ),
            ("phần trăm"                         , "%"         ),
            ("mét vuông"                         , "m2"        ),
            ("mét khối"                          , "m3"        ),
            ("mét"                               , "m"         ),
            ("ki lô mét"                         , "km"        ),
            ("ki lô mét vuông"                   , "km2"       ),
            ("mi ni lít"                         , "ml"        ),
            ("mi li lít"                         , "ml"        ),
            ("ki lô mét trên giây"               , "km/s"      ),
            ("gi ga bai"                         , "gb"        ),
            ("ghi ga bai"                        , "gb"        ),
            ("phít"                              , "ft"        ),
            ("giờ"                               , "h"         ),
            ("tê ét"                             , "ts"        ),
            ("mét trên giây"                     , "m/s"       ),
            ("đồng trên ét em ét"                , "đ/sms"     ),
            ("đồng trên một ét em ét"            , "đ/sms"     ),
            ("đồng trên phút"                    , "đ/phút"    ),
            ("đồng trên một phút"                , "đ/phút"    ),
            ("mê ga bai"                         , "mb"        ),
            ("mờ bê"                             , "mb"        ),
            ("mê ga bít"                         , "mb"        ),
            ("ki lô bít trên giây"               , "kbps"      ),
            ("ki lô bai trên giây"               , "kbps"      ),
            ("mê ga bai trên phút"               , "mb/phút"   ),
            ("mê ga bít trên phút"               , "mb/phút"   ),
            ("mi li giây"                        , "ms"        ),
            ("mi ni giây"                        , "ms"        ),
            ("gi ga bai trên ngày"               , "gb/ngày"   ),
            ("ghi ga bai trên ngày"              , "gb/ngày"   ),
            ("mi li mét"                         , "mm"        ),
            ("mi ni mét"                         , "mm"        ),
            ("giờ trên tuần"                     , "h/tuần"    ),
            ("xen ti mét"                        , "cm"        ),
            ("sen ti mét"                        , "cm"        ),
            ("u ét đê trên tuần"                 , "usd/tuần"  ),
            ("đô la trên tuần"                   , "usd/tuần"  ),
            ("iu ét đê trên tuần"                , "usd/tuần"  ),
            ("iu ét đi trên tuần"                , "usd/tuần"  ),
            ("mét vuông sàn trên người"          ,"m2sàn/người"),
            ("nghị quyết chính phủ"              , "/nq-cp"    ),
            ("ki lô mét trên giờ"                , "km/h"      ),
            ("ki lô bai trên giây"               , "kb/s"      ),
            ("ki lô bít trên giây"               , "kb/s"      ),
            ("phần trăm trên một cổ"             , "%/cổ"      ),
            ("phần trăm trên cổ"                 , "%/cổ"      ),
            ("phút"                              , "ph"        ),
            ("héc ta"                            , "ha"        ),
            ("hét ta"                            , "ha"        ),
            ("đồng trên mét vuông"               , "đồng/m3"   ),
            ("đồng trên 1 mét vuông"             , "đồng/m3"   ),
            ("mét vuông trên ngày"               , "m3/ngày"   ),
            ("mét vuông trên một ngày"           , "m3/ngày"   ),
            ("gờ ram"                            , "gr"        ),
            ("u ét đê trên một ki lô gam"        , "usd/kg"    ),
            ("mê ga pixel"                       , "mp"        ),
            ("độ xê"                             , "oc"        ),
            ("độ sê"                             , "oc"        ),
            ("mê ga bít trên giây"               , "mbps"      ),
            ("mê ga bai trên giây"               , "mbps"      ),
            ("pixel"                             , "px"        ),
            ("u ét đê"                           , "usd"       ),
            ("đô la"                             , "usd"       ),
            ("héc"                               , "hz"        ),
            ("inh"                               , "inch"      ),
            ]

    idx = 0;
    all_words_after_process_combine_len = len(all_words_after_process_combine) - 1
    while(idx < all_words_after_process_combine_len):
        curr_content, curr_label = all_words_after_process_combine[idx]
        next_content, next_label = all_words_after_process_combine[idx+1]
        if curr_label == "NUMB" and next_label == "O":
            #Xu ly ve don vi tien te
            for sufficient_currency, symbol_currency in sufficient_to_symbol_list_currency_symbols:
                if next_content.startswith(sufficient_currency):
                    curr_content += symbol_currency
                    curr_label = "NUMB-CURR"
                    next_content = next_content.replace(sufficient_currency, symbol_currency,1)
                    next_label = next_label
                    del all_words_after_process_combine[idx]
                    del all_words_after_process_combine[idx+1]
                    all_words_after_process_combine.index(idx,(curr_content, curr_label))
                    all_words_after_process_combine.index(idx+1,(next_content, next_label))
                    break
                else:
                    pass

            #Xu ly don vi metric
            for sufficient_metric, symbol_metric in sufficient_to_symbols_list_metric:
                if next_content.startswith(sufficient_metric):
                    curr_content += symbol_metric
                    curr_label = "NUMB-METRIC"
                    next_content = next_content.replace(sufficient_metric, "",1)
                    next_label = next_label  #= 'O'
                    del all_words_after_process_combine[idx]
                    all_words_after_process_combine.insert(idx,(curr_content, curr_label))
                    del all_words_after_process_combine[idx+1]
                    all_words_after_process_combine.insert(idx+1,(next_content, next_label))
                    break
                else:
                    pass
        idx+=1



    #Thay the cac cụm từ bằng từ viết tắt thích hợp
    idx = 0
    len1 = len(all_words_after_process_combine)
    danhsachcactuviettat = [
        ("vê vê tê vê"          ,   "VVTV"      ),
        ("vê tê vê"             ,   "VTV"       ),
        ("ép pi ti"             ,   "FPT"       ),
        ("sam sung"             ,   "Samsung"   ),
        ("trung học cơ sở"      ,   "THCS"      ),
        ("trung học phổ thông"  ,   "THPT"      ),
        ("đại học"              ,   "ĐH"        ),
        ("xi ao mi"             ,   "Xiaomi"    ),
        ("ghi ga bai"           ,   "GB"        ),
        ("gi ga bai"            ,   "GB"        ),
        ("vi na phôn"           ,   "Vinaphone" ),
        ("đô ta"                ,   "Dota"      ),
        ("đô ta hai"            ,   "Dota2"     ),
        ("mô bi phôn"           ,   "Mobiphone" ),
        ("ai phôn mười"         ,   "IphoneX"    ),
        ("ai phôn"              ,   "Iphone"    ),
        ("ai pát"               ,   "Ipad"      ),
        ("việt theo"            ,   "Viettel"   ),
        ("việt ten"             ,   "Viettel"   ),
    ];

    while(idx < len1):
        current_context, current_label = all_words_after_process_combine[idx]
        if current_label == 'O':
            phrase =""
            abbreviation=""
            for phrase, abbreviation in danhsachcactuviettat:
                current_context = current_context.replace(phrase, abbreviation)
            del all_words_after_process_combine[idx]
            all_words_after_process_combine.insert(idx, (current_context, current_label))
        idx += 1

    #Xử lý "chín A" -> 9A
    idx = 0
    len1 = len(all_words_after_process_combine) - 1
    while(idx < len1):
        current_content, current_label = all_words_after_process_combine[idx]
        next_content, next_label = all_words_after_process_combine[idx+1]
        if current_label == "NUMB" and next_label == "O":
            for symbol_character, spelling_character_set in english_vietnam_list_read_series.items():
                for spelling_character in spelling_character_set:
                    if next_content.startswith(spelling_character):
                        next_content = next_content.replace(spelling_character,"",1)
                        next_label = next_label
                        current_content += symbol_character
                        current_label = "NUMB-CHAR"
                        del all_words_after_process_combine[idx]
                        all_words_after_process_combine.insert(idx, (current_content, current_label))
                        del all_words_after_process_combine[idx+1]
                        all_words_after_process_combine.insert(idx+1, (next_content, next_label))
        idx += 1




    a = []
    for e in all_words_after_process_combine:
        a.append(e[0])

    result = " ".join(a)


    # Replace cho chuẩn form:
    # Iphone ích-> Iphone X
    post_dictionary = {
        "Iphone ích"    : "Iphone X",
    }
    for vietnamspelling, englishspelling in post_dictionary.items():
        result = result.replace(vietnamspelling, englishspelling)



    return result

def post_of_post_processing(list_sentence):
    all_words = []
    for index in range(len(list_sentence)):
        sentence, label = list_sentence[index]
        if label == "CAP":
            # phần này cần sửa lại
            words = sentence.split(" ")
            for i in range(len(words)):
                if not is_vietnamese_syllable(words[i].lower()):
                    if len(words) == 1 and len(words[i]) <= 5:
                        words[i] = words[i].upper()
            sentence = " ".join(words)
            # end
        elif label == "NUMB":
            if any([x not in list_numb_label for x in sentence.split(" ")]):
                label = "O"
        list_sentence[index] = (sentence, label)
        all_words.append(sentence)
    # print(list_sentence)
    # print(all_words)
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
        elif label == "CAP":
            is_checked = True
            words = sentence.split(" ")
            i = 0
            while i < len(words):
                ans = False
                for k in range(2):
                    k = 2 - k
                    word = " ".join(words[i:i + k])
                    ans = get_word_from_list_read_series(word.lower())
                    if ans:
                        if n == 0:
                            list_words.append([(word, ans)])
                        else:
                            list_words[-1].append((word, ans))
                        n += 1
                        if k > 1:
                            i += 1
                        break
                if not ans:
                    list_words.append([(words[i], False)])
                    n = 0
                i += 1

        if not is_checked and len(all_words[index]) > 0:
            n = 0
            list_words.append([(all_words[index], False)])
        index += 1


    ans = []
    for index in range(len(list_words)):
        words = list_words[index]
        if len(words) >= 2:
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
        else:
            ans += [x[0] for x in words]

    max_length_metric = max([len(x) for x in list_metric.values()])



    # concat digit + metric -> abbreviation
    # e.g: "50 ki lô mét" -> "50km"
    new_ans = []
    index = 0
    while index < len(ans):
        metric = False
        for k in range(max_length_metric):  # 3, 2, 1
            k = max_length_metric - k
            word = " ".join(ans[index: index + k])
            metric = get_metric_value(word)
            if metric:
                if index > 0 and all([x in [",", "-"] or x.isdigit() for x in ans[index - 1]]):
                    new_ans.append("_" + metric)
                else:
                    new_ans.append(word)
                index += k
        if not metric and index < len(ans):
            new_ans.append(ans[index])
            index += 1

    # number format consistency
    index = 0
    is_formated_number = any(re.search(r"\d.\d\d\d", word) for word in new_ans)
    while index < len(new_ans):
        word = new_ans[index]
        print(word)
        print(is_formated_number)
        if is_formated_number:
            read = string_to_numb(word)
            if read[1]:
                new_ans[index] = format_number(word, is_positive=True, format_numb=True, focus=True)
        index += 1

    result = " ".join(new_ans).replace("mồng mùng", "mồng").replace(" _", "")

    result = last_post_proccessing(result)
    return result


def last_post_proccessing(sentence):

    #xu ly viec 9 ích thành 9x
    words = sentence.split()
    i = 0
    while i < len(words):
        word = words[i]
        if word == "ích" and i > 0:
            prev_word = words[i - 1]
            if string_to_numb(prev_word)[1]:
                words[i - 1] = prev_word + "x"
                del(words[i])
        i += 1
    result = " ".join(words)

    #xử lý các từ viết hoa


    return result


def get_metric_value(metric_name):
    for key, value in list_metric.items():
        for _value in value:
            if _value == metric_name:
                return key
    return False


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
        if len(sentence) >= 7:
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
    "N": ["nờ", "en nờ", "en"],
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
    # print(read_string("209"))
    # print(is_percentage("20%"))
    # print(is_currency("%3"))
    # run_vlsp()
    # print(pre_of_post_processing("số điện thoại của tôi là không chín sáu năm bảy ba bốn tám chín ba"))
    # predict('tôi xem phim hello cô ba cùng ba mẹ tôi')
    list_syllabels = [
        ("cii", "O"),
        ("vê", "O"),
        ("vê", "O"),
        ("tê", "O"),
        ("vê", "O"),
        ("năm", "B-NUMB"),
        ("mươi", "I-NUMB"),
        ("hai", "I-NUMB"),
        ("nghìn", "I-NUMB"),
        ("ép pi ti", "B-CAP"),
        ("sáu nghìn", "B-NUMB"),
        ("mét", "O"),
        ("việt nam", "B-CAP"),
        ("hai phẩy ba", "B-NUMB"),
        ("ki lô mét", "O"),
        ("và", "O"),
        ("park", "B-CAP"),
        ("chín", "B-NUMB"),
        ("ích", "O"),
        ("chiều tối hai mươi tư tháng mười hai năm hai ngàn", "B-DATE"),
        ("hai mươi", "B-NUMB"),
        ("mét vuông", "O"),
        ("đầu", "O"),
        ("tư", "O"),
        ("không", "O"),
        ("hoàn", "O"),
        ("lại", "O"),
        ("vê tê vê", "O"),
        ("ai phôn", "O"),
        ("ích", "O"),
        ("học", "O"),
        ("lớp", "O"),
        ("mười", "B-NUMB"),
        ("xê", "O"),
        ("tôi", "O"),
        ("mới", "O"),
        ("mua", "O"),
        ("con", "O"),
        ("ai phôn", "O"),
        ("mười", "O"),
        ("ét ô ét", "B-CAP"),
        ("wimbledon", "O")
    ]
    # predict('số điện thoại của tôi là không chín sáu năm bảy ba bốn tám chín ba')
    #print(read_number("123")[0])   `                           một trăm hai ba
    # print(read_character("da", type="standard"))              đê a
    # print(read_character("vcl", type="standard"))             vê xê lờ

    #print(is_whole_number("112", type="Formal")[0])           #một trăm mười hai
    #print(is_whole_number("112", type="Standard")[0])          một trăm mười hai
    #print(is_whole_number("112a", type="Standard")[0])         một nghìn một trăm hai mươi

    #print(is_long_datetime("1.2.2019")[0][0][0])               ngày một tháng hai năm hai nghìn không trăm mười chín

    #print(is_short_datetime_type_1("02/09")[0][0][0])          ngày hai tháng chín

    #print(get_number_from_hundred_str("bốn trăm bảy mươi lăm"))(475, True)

    # print(is_short_datetime_type_2("02-2288")[0][0][0])         #tháng hai năm hai nghìn hai trăm tám tám

    #print(is_phone_number("0974793321"))                          error when run with python2 matchfull()

    print(get_ans(list_syllabels))
    print(sentence_to_numb("hai trăm bốn mươi ba nghìn tỷ bảy trăm hai mươi mốt triệu"))
    print(sentence_to_numb("bốn mươi hai phẩy hai tư"))
    print(read_character("F"))
    print(convert_word_character("ép"))
    print(cap_to_abbreviation("vê kép hắt ô"))
    # # print(is_vietnamese_syllable("nam"))
    # # print(get_number_from_hundred_str("hai lăm"))
    # # print(read_last("hai ba bốn năm a bê xê"))
    # # print(read_first("hai ba bốn năm a bê xê"))post_proccessing_production.py:1609
    print(read_number("145"))