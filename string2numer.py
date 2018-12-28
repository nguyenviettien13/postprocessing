DIGIT_DICT = {
        "không":  0 ,
        "một"  :  1 ,
        "hai"  :  2 ,
        "ba"   :  3 ,
        "bốn"  :  4 ,
        "năm"  :  5 ,
        "sáu"  :  6 ,
        "bảy"  :  7 ,
        "tám"  :  8 ,
        "chín" :  9
}

BASE_DICT = {
    "mươi"  :   10,
    "trăm"  :   100,
    "nghìn" :   1000,
    "triệu" :   1000000,
    "tỷ"    :   1000000000,
}

########################################################################################################################
###################################################  SỐ  TỰ  NHIÊN    ##################################################
########################################################################################################################

'''
chuyen mot xau bieu dien so nho hon 1000 ve dang so (int)
Neu xau do la rong trả về -1
Nếu xâu đó sai thì trả về False
'''

def string2number_lt_10E3(s):
    #basic format chuẩn hóa các cách đọc
    s = s.strip()
    s = s.replace("linh", "")
    s = s.replace("mười", "một mươi")
    s = s.replace("tư", "bốn")
    s = s.replace("lăm", "năm")
    s = s.replace("mốt", "một")
    if s == '':
        return -1;
    s = s.split()

    #Chuyển định dạng: hai ba thành hai mươi ba
    set = []
    pre_word    = "non_digit";
    curr_wrod   = ""
    for word in s:
        if word in DIGIT_DICT.keys():
            curr_word = "digit"
        else:
            if word in BASE_DICT.keys():
                curr_word = "non_digit"
            else:
                return False
        if curr_word == "digit" and pre_word == "digit":
            set.append("mươi")

        set.append(word)
        pre_word = curr_word

    # dinh dang chuan dam bao so tan cung ket thuc bang chu so
    # hai mươi -> hai mươi không
    if set[-1] not in ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]:
        set.append("không")

    #tư tưởng thuật toán:
    # một trăm hai mươi ba
    # return
    number = 0;
    curr_base = 1;
    curr_digit= 1
    for word in reversed(set):
        if word in DIGIT_DICT.keys():
            #word là một số
            curr_digit = DIGIT_DICT.get(word)
            number += curr_digit * curr_base
        else:
            #word là một base
            curr_base = BASE_DICT.get(word)
    return number

'''
Chuyen mot xau bieu dien so nho hon mot trieu ve dang so (int)
Neu xau rong tra ve -1 
Neu xau khong hop le tra ve 0
'''

def string2number_lt_10E6(s):
    s = s.strip()
    s = s.replace("linh", "")
    s = s.replace("mười", "một mươi")
    s = s.replace("tư", "bốn")
    s = s.replace("lăm", "năm")
    s = s.replace("ngàn", "nghìn")
    s = s.replace("mốt", "một")

    if s == '':
        return -1

    number_of_thousand  = 0
    additional_number   = 0
    set = s.split("nghìn")
    if len(set) ==1:
        #không chứa chữ nghìn
        return string2number_lt_10E3(set[0])
    else:
        # 2 thành phần
        number_of_thousand  = string2number_lt_10E3(set[0])
        additional_number   = string2number_lt_10E3(set[1])
        if additional_number == False:
            return False
        if number_of_thousand == False or number_of_thousand ==-1:
            return False
        if additional_number == -1:
            return number_of_thousand * 1000
        else :
            return number_of_thousand * 1000 + additional_number

def string2number_lt_10E9(s):
    s = s.strip()
    s = s.replace("linh", "")
    s = s.replace("mười", "một mươi")
    s = s.replace("tư", "bốn")
    s = s.replace("lăm", "năm")
    s = s.replace("mốt", "một")
    s = s.replace("ngàn", "nghìn")
    set = s.split("triệu")
    number_of_million   = 0
    additional_million  = 0

    if len(set) == 1:
        # nho hon mot trieu
        return string2number_lt_10E6(set[0])
    else:
        #lon hon mot trieu
        number_of_million = string2number_lt_10E3(set[0])
        additional_million = string2number_lt_10E6(set[1])

    if additional_million == False or number_of_million == False:
        return False
    else:
        if number_of_million == -1:
            return False
        else:
            if additional_million == -1:
                return number_of_million * 1000000
            else:
                return number_of_million * 1000000 + additional_million


def string2number_lt_10E18(s):
    s = s.strip()
    s = s.replace("linh", "")
    s = s.replace("mười", "một mươi")
    s = s.replace("tư", "bốn")
    s = s.replace("lăm", "năm")
    s = s.replace("ngàn", "nghìn")
    s = s.replace("mốt", "một")
    s = s.replace("tỉ", "tỷ")
    set = s.split("tỷ",1)
    number_of_billion = 0
    additional_billion = 0
    if len(set) ==1:
        #truong hop nho hon mot ty
        return string2number_lt_10E9(set[0])
    else:
        #truong hop lon hon mot ty
        number_of_billion = string2number_lt_10E9(set[0])
        additional_billion = string2number_lt_10E9(set[1])
    if additional_billion == False or number_of_billion ==False:
        return False
    else:
        if number_of_billion == -1:
            return False
        else:
            if additional_billion == -1:
                return number_of_billion* 1000000000
            else:
                return number_of_billion * 1000000000 + additional_billion

# Xử lý số nguyên có dấu
def string2numberlt10E18withsign(s):
    s = s.strip()
    sign = 1
    if s.startswith("+"):
        sign = 1
        s = s.replace("+", "")
    if s.startswith("-"):
        sign = -1
        s = s.replace("-", "")
    s = s.strip()
    number = string2number_lt_10E18(s)
    return number * sign

########################################################################################################################
###################################################  SỐ  THẬP PHÂN    ##################################################
########################################################################################################################


# Có thể chuyển với cả số thập phân hoặc số tự nhiên thông thường.
def string2decimalnumber(input):
    input= input.strip()
    input = input.replace("phẩy", "phảy")
    if input.split().count("phảy") == 0:
        return string2number_lt_10E18(input)
    else:
        string_whole_partition, string_decimal_partition = input.split("phảy")
        s = str(string2number_lt_10E18(string_whole_partition))+ "." + str(string2number_lt_10E18(string_decimal_partition))
        return float(s)

#Chuyen string đọc số thập phân sang sô thập phân
# Có thể áp dụng cho cả số dương hoặc âm
def string2_decimalnumber_with_sign(s):
    s = s.strip()
    sign = 1
    if s.startswith("dương"):
        sign = 1
        s = s.replace("dương", "")
    if s.startswith("âm"):
        sign = -1
        s = s.replace("âm", "")
    s = s.strip()
    number = string2decimalnumber(s)
    return number * sign




if __name__ == "__main__":
    print(string2number_lt_10E3("hai mươi"))
    print(string2number_lt_10E18("hai trăm ba mươi mốt tỷ bốn trăm mười hai triệu ba trăm mười một ngàn chín trăm hai mươi mốt"))
    print(string2number_lt_10E18("máy pha cà phê"))
    print(string2decimalnumber("bốn ba phảy chín tám") + 3)
    print(string2decimalnumber("một phảy hai") + 3)
    print(string2_decimalnumber_with_sign("âm một phảy hai"))
    print(string2_decimalnumber_with_sign("dương một phảy hai"))
