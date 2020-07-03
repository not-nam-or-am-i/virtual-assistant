import datetime
import os
from numpy.random import seed
from numpy.random import randint


game_list = { "Sở thú bị cháy ,đố bạn con gì chạy ra đầu tiên?" : "người",
             "Mỗi năm có 7 tháng 31 ngày. Đố bạn có bao nhiêu tháng có ngày 28 ? ": "12",
             "Tại sao 30 người đàn ông và 2 người đàn bà đánh nhau toán loạn ?": "cờ",
             "Bệnh gì bác sỹ bó tay" : "gãy tay",
             "Con gì ăn lửa với nước than": "con tàu",
             "Nắng ba năm tôi ko bỏ bạn, mưa 1 ngày sao bạn lại bỏ tôi là cái gì?" : "bóng",
             "Trên nhấp dưới giật là đang làm gì?": "câu cá",
             "Con gì mang được miếng gỗ lớn nhưng ko mang được hòn sỏi?" : "sông",
             "Rất thích hôn gọi là gì?" : "kết hôn",
             "Vua hôn gọi là gì?" : "hoàng hôn",
             "Cái gì đánh cha, đánh má, đánh anh, đánh chị, đánh em?" : "bàn chải",
             "Tại sao có những người đi taxi nhưng sao họ lại không trả tiền?": "tài xế",
             "gười da đen tắm biển đen. Vậy hỏi họ bị gì?" : "bị ướt",
             "Cái gì chứa nhiều nước nhất mà không ướt?" : "bản đồ",
             "Con gì bỏ cái đuôi thành con ngựa?" : "mèo",
             "Bố mẹ có sáu người con trai, mỗi người con trai có một em gái. Hỏi gia đình đó có bao nhiêu người?" : "9",
             "Miệng rộng nhưng không nói một từ, là gì?" : "sông",
             "Hoa gì biết ăn, biết nói, biết hát ...?" : "hoa hậu",
             "5 chia 3 bằng 2 khi nào?" : "sai", # ta làm sai 
             "Ở Việt Nam, con rồng bay ở đâu ?" : "thăng long",
             "Ở Việt Nam, con rồng đáp ở đâu?" : "hạ long",
             "Đố em cái gì khi xài thì quăng đi, không xài thì lấy lại?" : "neo",
             "Cái gì mà đi thì nằm, đứng cũng nằm, nhưng nằm lại đứng?" : "bàn chân",
             "Cái gì tay trái cầm được còn tay phải cầm không được?" : "tay phải",
             "Bánh chưng, bánh giầy bánh nào tượng trưng cho đất?" : "bánh chưng",
             "Ăn gì mà bán buôn tấp nập?" : "ăn khách",
             "Từ điển có bao nhiêu từ?" : "2",
             "Tay nào chẳng làm nên chuyện gì ra hồn?" : "tay mơ",
             "Cái gì lặn mà không lặn?" : "mặt trời",
             "Ăn gì mà càng ngày càng nhỏ lại?": "ăn mòn",
             "Xã đông nhất là xã nào?" : "xã hội",
             "Quần rộng nhất là quần gì?" : "quần đảo",
             "Hôn trong mơ gọi là" : "hôn ước",
             "Núi nào mà bị chặt ra từng khúc?" : "thái sơn",
             "Sở thú bị cháy, con gì chạy ra đầu tiên?" : "người",
             "Có 1 người không may bị té xuống hồ sâu, quần áo đều ướt đẫm hết nhưng không thấy tóc ướt tí nào. Hỏi vì sao?" : "không có tóc",          
 }
 
key_list = list(game_list)

def play_hangman(ques: str):
    list_ques = ["câu đố", "game", "trò chơi"] 
    flag = 0
    for i in list_ques:
        if i in ques:
            flag = 1

    if os.stat("game_history.txt").st_size != 0 :
        print("file game có dữ liệu ")
        flag = 1

    if flag == 1 :     
        #open and read the file after the appending:
        if os.stat("game_history.txt").st_size == 0 :
            # print("nothing")
            f = open("game_history.txt", "w", encoding="utf-8")
            seed_num = datetime.datetime.now().time().microsecond % 100
            print("seed number: ", seed_num)

            seed(seed_num) 
            number_ = randint(0, len(game_list), 1)[0]
            cau_hoi = key_list[number_]
            f.write(""+cau_hoi)
            f.close()    
            ans = cau_hoi
            return "true", ans   
        else:      
            if "thoát trò chơi" in ques.strip().lower() or "đầu hàng" in ques.strip().lower() or "thoát game" in ques.strip().lower():
                f = open("game_history.txt", "r+", encoding="utf-8")
                f.truncate(0)
                f.close()
                return "true", "Bạn gà lắm hi hi "                

            f = open("game_history.txt", "r", encoding="utf-8")            
            data = f.read()
            print(data)
            real_ans = game_list[data]
            if real_ans.lower() in ques.strip().lower():

                f = open("game_history.txt", "r+", encoding="utf-8")
                f.truncate(0)
                f.close()
                return "true", "Chính xác ! Chúc mừng bạn !"

            else:
                return "true", "Chưa đúng ! Cố lên bạn ơi !"

    return "false", "none"
