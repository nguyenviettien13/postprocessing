import re
DICTIONARY_FOR_ABBREVIATE_NAME = "dictionary.text"

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

class Abbreviation:
    def __init__(self, var):
        #do nothing
        print("Create an Abbreaviation" + var)
    ####################################################################################################################
    ###############################     Xử lý viết tắt (có thể là hoa hoặc thường ) dựa trên ký tự  ####################
    ###############################     Ví dụ :a xê bê -> ACB                                       ####################
    ####################################################################################################################

    # Hàm sẽ kiểm tra xem đầu vào có phải phát âm của một chữ cái hay không
    # Return Value: True /False
    def check_character_spelling(self, input):
        input = input.strip()
        character_spelling_list = []
        for char, spelling_list in english_vietnam_list_read_series.items():
            character_spelling_list.extend(spelling_list)
        if input in character_spelling_list:
            return True
        else:
            return False

    def spelling_2_character(self, input):
        for k, v in english_vietnam_list_read_series.items():
            if input in v:
                return k
    #chuyển đầu vào là danh sách các ký tự thành đầu ra là các ký tự viết tắt
    def string2abbre(self, input): #input sẽ có dạng [("vê kép", "character"), ("hát", "character"), ("ô", "character")]
        output = ""
        list = input[0]
        for w in list:
            output += self.spelling_2_character(w)
        return output

    # Hàm sẽ nhiệm vụ lọc các từ có thể viết tắt trong câu có nhãn là O
    #đầu vào            chuỗi nối các string có nhãn là O với nhau.
    # cê cê tê vê       ---------------------->               CCTV
    def refine_character_spelling_list(self, input):
        input = input.strip()
        #danh sach các chữ cái có 2 âm tiết
        two_syllabel_character = [("ét xì","ét_xì"), ("ích xì","ích_xì"),("vê kép" ,"vê_kép"), ("vê đúp","vê_đúp")]
        for word, word_with_dash in two_syllabel_character:
            if word in input:
                input = input.replace(word, word_with_dash)
        # tách các từ
        input_list = input.split()
        input_list1 = []
        for word in input_list:
            if word in ["ét_xì","ích_xì","vê_kép", "vê_đúp"]:
                word = word.replace("_", " ")
            input_list1.append(word)
        #input_list1 = ["tổ", "chức", "vê kép", "hắt" , "ô", "đã", "chuyển", "trụ", "sở", "về", "việt", "nam" ]
        # gán nhãn character, noncharacter label
        input_list_with_label = []
        for word in input_list1:
            if self.check_character_spelling(word):
                input_list_with_label.append(tuple((word, "character")))
            else:
                input_list_with_label.append(tuple((word, "noncharacter")))
        # kết thúc ta sẽ thu được
        #       "tổ",     "chức",     "vê kép",   "hắt" ,     "ô",    "đã",   "chuyển",   "trụ",  "sở",   "về",   "việt",     "nam"
        #       non         non         char       char       char     non       non         non     non     non     non         non
        # cê cê tê vê
        input_list_after_combine = []
        character_list = []
        for k, v in input_list_with_label:
            if v == "noncharacter":
                if len(character_list) > 0:
                    input_list_after_combine.append(tuple((character_list,"character")))
                    character_list = []
                input_list_after_combine.append(tuple((k,v)))
            else:
                character_list.append(k)
        if len(character_list) > 0:
            input_list_after_combine.append((character_list,"character"))

        output = ""
        for k, v in input_list_after_combine:
            if v == "noncharacter":
                output += " " + k
            else:
                output += " " + self.string2abbre((k,v))
        return output.strip()

    ####################################################################################################################
    ##############################      Xử lý các từ viết tắt dựa trên từ  #############################################
    ##############################      Trung học cơ sở -> THCS            #############################################
    ##############################      Đại học         -> ĐH              #############################################
    ####################################################################################################################

    dict_word_base_abbreviation = "dict_word_base_abbreviation.txt"
    word_base_abbreviation_dictionary = {}
    #Ta có hai hướng xử lý:
    # Hướng 1: Đối với mỗi một câu ta sẽ phải iterate qua toàn bộ các từ của từ điển
    # Hướng 2: Xử lý từng phần của câu. # Hướng này không khả thi tạm thời code theo hướng 1.
    # Sử dụng để filter qua các từ viết tắt trong từ điển
    # Trả lại câu đúng luôn
    def load_word_base_abbreviation_dictionary(self):
        with open("dict_word_base_abbreviation.txt") as file:
            line = file.readline()
            while line:
                k, v = tuple(line.split("\t", 1))
                self.word_base_abbreviation_dictionary[k] = v
        return self.word_base_abbreviation_dictionary

    def filter_use_dict_word_base_abbreviation(self, sentence):
        word_base_abbreviation_dictionary = self.load_word_base_abbreviation_dictionary()
        for k, v in word_base_abbreviation_dictionary.items():
            sentence = sentence.replace(k, v)
        return sentence



if __name__ == "__main__":
    a  = Abbreviation("Tien")
    print(a.refine_character_spelling_list("xin chào tất cả vê kép hát ô"))

    

