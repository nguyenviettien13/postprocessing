'''
author: nguyenviettien2102@gmail.com
github: nguyenviettien13@github.com
'''

'''
This module use to convert number form  in string type to string describe what we read
INPUT:  "123"
OUTPUT: "một trăm hai mươi ba"
'''
import string2numer


PRONOUN_DIGIT_DICT = {
    "0": "không",
    "1": "một",
    "2": "hai",
    "3": "ba",
    "4": "bốn",
    "5": "năm",
    "6": "sáu",
    "7": "bảy",
    "8": "tám",
    "9": "chín",
}

#Hàm dùng để đảm bảo chuỗi đầu vào chỉ chứa toàn số
def ensure_number(s):
    s = s.strip()
    for c in s:
        if c not in PRONOUN_DIGIT_DICT.keys():
            return False
        else:
            return True

#---------------------------------------------------------------------------------------------------------------------
#-------------------------------------------- ĐỌC SỐ TỰ NHIÊN --------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

# Đọc số tự nhiên có một chữ số theo dạng chuẩn
def read_1d_number(s):
    if not ensure_number(s):
        print("Err: string \""+ s + "\" is not valid, it is not number string!!! Oopps")
        return False

    if len(s) != 1:
        print("ERR: " + s + " do not have one digit! Oopps")
        return False
    else:
        return PRONOUN_DIGIT_DICT[s]



# Đọc số tự nhiên có it hon hoac bang 2 chu so.
# Chú ý:
# Vấn đề 1: Nếu 01 đọc là một hay đọc là linh một
# Vấn đề 2: 15 đọc là mười lăm
# Vấn đề 3: 05 đọc là linh lăm
# Vấn đề 4: 24 đọc là hai mươi tư
# Vấn đề 5: 14 đọc là mười bốn

def read_2d_number(input):
    s = ""
    #Đảm bảo chuối chỉ chứa toàn số
    if not ensure_number(input):
        print("Err: string \""+ input + "\" is not valid, it is not number string!!! Oopps")
        return False
    #Đảm bảo chuỗi chỉ chứa 2 chữ số
    if len(input) > 2:
        print("Error: read_2d_number cannot convert " + input + "to number")
        return False
    elif len(input) < 2:
        return read_1d_number(input)
    else:
        tens_string = input[0]
        ones_string = input[1]
        if tens_string == "0":
            s += "linh"
        elif tens_string == "1":
            s += "mười"
        else:
            s += PRONOUN_DIGIT_DICT[tens_string] + " mươi"


        if ones_string == "0":
            if s == "linh":
                s = ""
        elif ones_string == "1":
            if tens_string != "1" and tens_string != "0" :
                s += " mốt"
            else:
                s += " một"
        elif ones_string == "4":
            if tens_string == "1":
                s += " bốn"
            else:
                s += " tư"
        elif ones_string == "5":
            if tens_string == "0":
                s += " năm"
            else:
                s += " lăm"
        else:
            s += " " + PRONOUN_DIGIT_DICT[ones_string]
    return s.strip()


# Đọc số có ít hơn hoặc bằng 3 chữ số
def read_3d_number(input):
    s = ""
    # Đảm bảo chuối chỉ chứa toàn số
    if not ensure_number(input):
        print("Err: string \"" + input + "\" is not valid, it is not number string!!! Oopps")
        return False
    if len(input) >3:
        print("Error: read_3d_number cannot convert " + input + "to number")
        return False
    elif len(input) < 3:
        return read_2d_number(input)
    else:
        hundreds_string = input[0]
        two_last_digit = input[1:]
        s += PRONOUN_DIGIT_DICT[hundreds_string] + " trăm" + " " + read_2d_number(two_last_digit)
    return s.strip()

# Đọc số có ít hơn hoặc bằng 6 chữ số
def read_6d_number(input):
    s = ""
    # Đảm bảo chuối chỉ chứa toàn số
    if not ensure_number(input):
        print("Err: string \"" + input + "\" is not valid, it is not number string!!! Oopps")
        return False
    if len(input) > 6:
        print("Error: read_6d_number cannot convert " + input + "to number")
        return False
    elif len(input) <= 3:
        return read_3d_number(input)
    else:
        thousands_part = input[:-3]
        hundreds_part = input[-3:]
        s = read_3d_number(thousands_part) + " nghìn " + read_3d_number(hundreds_part)
        return s.strip()


# Đọc số có ít hơn hoặc bằng 9 chữ số
def read_9d_number(input):
    s = ""
    # Đảm bảo chuối chỉ chứa toàn số
    if not ensure_number(input):
        print("Err: string \"" + input + "\" is not valid, it is not number string!!! Oopps")
        return False

    if len(input) > 9:
        print("Error: read_9d_number cannot convert " + input + "to number")
        return False
    elif len(input) <= 6:
        return read_6d_number(input)
    else:
        millions_part = input[:-6]
        thousands_part = input[-6:]
        s = read_3d_number(millions_part) + " triệu " + read_6d_number(thousands_part)
        return s.strip()

#Đọc số tự nhiên bất kỳ
def read_number(input):
    s = ""
    # Đảm bảo chuối chỉ chứa toàn số
    if not ensure_number(input):
        print("Err: string \"" + input + "\" is not valid, it is not number string!!! Oopps")
        return False
    list_list = []
    input_list = list(input)
    while len(input_list) != 0:
        list_list.append(input_list[-9:])
        del input_list[-9:]
    string_list = []
    for e in list_list:
        string_list.append(''.join(e).strip())
    if len(string_list) == 1:
        return read_9d_number(string_list[0])
    else:
        temporary_list = string_list[1:]
        temporary_list.reverse()
        for e in temporary_list:
            s += read_9d_number(e)+ " tỷ "
        s += read_9d_number(string_list[0])
        return s

# Đọc số nguyên bất kỳ có cả âm và dương
def read_number_with_sign(input):
    sign = ""
    if input.startswith("+"):
        sign = ""
        input = input.replace("+", "")
        input = input.strip()

    if input.startswith("-"):
        sign = "âm"
        input = input.replace("-", "")
        input = input.strip()
    number = read_number(input)
    return sign + " " + number
#---------------------------------------------------------------------------------------------------------------------
#--------------------------------------------ĐỌC SỐ THẬP PHÂN--------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
'''
Đọc số thập phân theo chuẩn quốc tế 
float pointer is "." not ","
'''

# Kiểm tra xem chuỗi đầu vào có đúng định dạng số thập phân không
# Nếu thỏa mãn return True ngược lại, sai return False
def ensure_decimal_number(input):
    if input.count(".")>1:
        print("Err: " + input + " is not a decimal number.")
        return False
    for c in input:
        if c not in PRONOUN_DIGIT_DICT.keys() and c not in ["."]:
            return False
    return True

'''
Đọc số thập phân 
'''
def read_decimal_number(input):
    if not ensure_decimal_number(input.strip()):
        print("Err:" + input + " is not inform of decimal number ")
        return False
    if input.count(".") == 0:
        return read_number(input)
    else:
        whole_number, decimal_number = input.split(".")
        s = read_number(whole_number) + " phảy " + read_number(decimal_number)
        return s.strip()
#Chuyển số thập phân âm hoặc dương sang chuối
def read_decimal_number_with_sign(input):
    sign = 1
    if input.startswith("+"):
        sign = 1
        input = input.replace("+", "")
        input = input.strip()

    if input.startswith("-"):
        sign = -1
        input = input.replace("-", "")
        input = input.strip()
    number = read_decimal_number(input)
    return number * sign


if __name__ == "__main__":
    #print (read_1d_number("12"))
    #print(read_2d_number("75"))
    #print(read_3d_number("4"))
    print("\"01                         :" + read_number("01") + "\"")
    print("\"11                         :" + read_number("11") + "\"")
    print("\"15                         :" + read_number("15") + "\"")
    print("\"25                         :" + read_number("25") + "\"")
    print("\"44                         :" + read_number("44") + "\"")
    print("\"54                         :" + read_number("54") + "\"")
    print("\"51                         :" + read_number("51") + "\"")
    print("\"151                        :" + read_number("151") + "\"")
    print("\"051                        :" + read_number("051") + "\"")
    print("\"1001                       :" + read_number("1001") + "\"")
    print("\"5611                       :" + read_number("5611") + "\"")
    print("\"1115611                    :" + read_number("1115611") + "\"")
    print("\"24241115611                :" + read_number("24241115611") + "\"")
    print("\"242234124124241115611      :" + read_number("242234124124241115611") + "\"")
    print("\"1234123412345              :" + read_number("1234123412345") + "\"")
    print(read_decimal_number_with_sign("- 13.21"))