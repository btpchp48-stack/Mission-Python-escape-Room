# MISSION PYTHON: The Cute Escape Room
# เกม Escape Room ฝึกทักษะ Python สำหรับ Google Colab
# รันเซลล์นี้ แล้วกดปุ่ม "เริ่มภารกิจ"

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import threading
import time

ROOMS = [
    {"name":"🚪 ห้องที่ 1: The Gate of Conditions","topic":"if / elif / else",
     "hint":"if ใช้ตรวจสอบเงื่อนไข ส่วน else ทำงานเมื่อเงื่อนไขก่อนหน้าไม่เป็นจริง",
     "questions":[
      {"q":"คำสั่งใดใช้ตรวจสอบเงื่อนไขในภาษา Python?","choices":["for","if","def","print"],"answer":1,"explain":"if ใช้ตรวจสอบว่าเงื่อนไขเป็นจริงหรือไม่"},
      {"q":"ถ้าเงื่อนไข if เป็น False ควรใช้คำสั่งใดเพื่อให้มีคำสั่งทำงานแทน?","choices":["else","break","return","range"],"answer":0,"explain":"else จะทำงานเมื่อเงื่อนไขใน if ไม่เป็นจริง"}]},
    {"name":"🔁 ห้องที่ 2: The Loop Chamber","topic":"for / while / range",
     "hint":"for ใช้วนซ้ำตามลำดับ ส่วน range(5) ให้ค่า 0 ถึง 4 รวม 5 ค่า",
     "questions":[
      {"q":"ต้องการวนซ้ำคำสั่ง 5 รอบ คำสั่งใดเหมาะสม?","choices":["for i in range(5):","if i == 5:","def range(5):","print(5)"],"answer":0,"explain":"range(5) ให้ค่า 0, 1, 2, 3, 4 รวม 5 รอบ"},
      {"q":"while จะวนซ้ำตราบใดที่เงื่อนไขเป็นอย่างไร?","choices":["False","ไม่มีเงื่อนไข","True","เป็นข้อความ"],"answer":2,"explain":"while ทำงานซ้ำตราบใดที่เงื่อนไขเป็น True"}]},
    {"name":"🧪 ห้องที่ 3: The Function Lab","topic":"def / parameters / return",
     "hint":"ใช้ def เพื่อสร้างฟังก์ชัน และ return เพื่อส่งค่ากลับจากฟังก์ชัน",
     "questions":[
      {"q":"คำสั่งใดใช้ประกาศฟังก์ชันใน Python?","choices":["function","define","def","fun"],"answer":2,"explain":"Python ใช้ def ในการประกาศฟังก์ชัน"},
      {"q":"คำสั่งใดใช้ส่งค่ากลับจากฟังก์ชัน?","choices":["print","return","input","break"],"answer":1,"explain":"return ใช้ส่งค่ากลับไปยังจุดที่เรียกใช้ฟังก์ชัน"}]},
    {"name":"🐞 ห้องที่ 4: The Debugging Room","topic":"ข้อผิดพลาด / break",
     "hint":"break ใช้หยุด loop ทันที ส่วน SyntaxError เกิดจากการเขียนไวยากรณ์ไม่ถูกต้อง",
     "questions":[
      {"q":"คำสั่งใดใช้หยุด loop ทันที?","choices":["stop","exit","break","continue"],"answer":2,"explain":"break ใช้ยุติการวนซ้ำทันที"},
      {"q":"ข้อผิดพลาดจากการเขียนไวยากรณ์ Python ไม่ถูกต้องเรียกว่าอะไร?","choices":["SyntaxError","ValueCorrect","LoopError","PrintError"],"answer":0,"explain":"SyntaxError เกิดเมื่อรูปแบบคำสั่งไม่ถูกต้อง"}]},
    {"name":"🏆 ห้องที่ 5: The Final Challenge","topic":"ทบทวนความรู้ Python",
     "hint":"ทบทวนเรื่องตัวแปร ชนิดข้อมูล และคำสั่งแสดงผล",
     "questions":[
      {"q":"ชนิดข้อมูลของค่า 25 ใน Python คืออะไร?","choices":["str","float","int","list"],"answer":2,"explain":"25 เป็นจำนวนเต็ม จึงมีชนิดข้อมูลเป็น int"},
      {"q":"ฟังก์ชันใดใช้แสดงผลข้อความบนหน้าจอ?","choices":["input()","print()","range()","type()"],"answer":1,"explain":"print() ใช้แสดงผลข้อมูลออกทางหน้าจอ"}]}
]

score = 0
room_index = 0
question_index = 0
room_correct = 0
hint_used = False
game_active = False
time_left = 180
game_version = 0
timer_stop = threading.Event()

header = widgets.HTML()
status = widgets.HTML()
timer_label = widgets.HTML()
story = widgets.HTML()
question_box = widgets.HTML()
feedback = widgets.HTML()
hint_button = widgets.Button(description="💡 ขอคำใบ้ (-2 คะแนน)", button_style="warning")
start_button = widgets.Button(description="เริ่มภารกิจ", button_style="success")
next_button = widgets.Button(description="คำถามถัดไป ➜", button_style="info")
restart_button = widgets.Button(description="เล่นอีกครั้ง", button_style="info")
answer_buttons = [widgets.Button(layout=widgets.Layout(width="100%", height="42px")) for _ in range(4)]
answer_grid = widgets.GridBox(answer_buttons, layout=widgets.Layout(
    grid_template_columns="repeat(2, minmax(0, 1fr))", grid_gap="8px", width="100%"))
main_output = widgets.Output()

def stop_timer():
    timer_stop.set()

def timer_worker(version):
    global time_left, game_active
    while not timer_stop.is_set() and version == game_version and game_active:
        time.sleep(1)
        if timer_stop.is_set() or version != game_version or not game_active:
            break
        time_left -= 1
        timer_label.value = f"<b>⏳ เวลาคงเหลือ: {time_left//60:02d}:{time_left%60:02d}</b>"
        if time_left <= 0:
            game_active = False
            timer_label.value = "<b style='color:#d62828'>⏰ หมดเวลา!</b>"
            with main_output:
                clear_output(wait=True)
                display(HTML("<div style='background:#fff0f6;padding:20px;border-radius:16px'><h2>⏰ TIME OUT!</h2>หมดเวลาในห้องนี้แล้ว ลองเริ่มภารกิจใหม่เพื่อฝึกอีกครั้งนะ</div>"))
                display(restart_button)
            break

def start_room_timer():
    global time_left, game_version
    stop_timer()
    game_version += 1
    version = game_version
    timer_stop.clear()
    time_left = 180
    timer_label.value = "<b>⏳ เวลาคงเหลือ: 03:00</b>"
    threading.Thread(target=timer_worker, args=(version,), daemon=True).start()

def update_status():
    status.value = (f"<p>🏅 คะแนน: <b>{score}</b>　|　🔐 ห้อง: <b>{room_index+1}/5</b>"
                    f"　|　✅ ตอบถูกในห้องนี้: <b>{room_correct}/2</b></p>")

def show_question():
    room = ROOMS[room_index]
    q = room["questions"][question_index]
    header.value = "<h1 style='color:#c04483;margin-bottom:0'>MISSION PYTHON</h1><b>THE CUTE ESCAPE ROOM</b>"
    story.value = f"<div style='background:#fff0f6;padding:14px;border-radius:14px'><h3>{room['name']}</h3><b>ภารกิจ:</b> {room['topic']}<br>ตอบให้ถูก 2 ข้อเพื่อรับ Digital Key</div>"
    question_box.value = f"<div style='background:#eef7ff;padding:14px;border-radius:14px;margin-top:8px'><b>คำถามที่ {question_index+1}/2</b><h3>{q['q']}</h3></div>"
    feedback.value = ""
    update_status()
    for i, b in enumerate(answer_buttons):
        b.description = f"{'ABCD'[i]}. {q['choices'][i]}"
        b.disabled = False
        b.button_style = ""
    hint_button.disabled = hint_used
    next_button.layout.display = "none"

def show_next_question_button():
    next_button.description = "คำถามถัดไป ➜"
    next_button.layout.display = "block"
    for b in answer_buttons:
        b.disabled = True

def on_answer(index):
    global score, question_index, room_correct, game_active
    if not game_active:
        return
    q = ROOMS[room_index]["questions"][question_index]
    if index == q["answer"]:
        score += 10
        room_correct += 1
        feedback.value = f"<p style='color:#16834a'><b>🎉 ถูกต้อง! +10 คะแนน</b><br>{q['explain']}</p>"
        for b in answer_buttons:
            b.disabled = True
        update_status()
        if room_correct == 2:
            stop_timer()
            game_active = False
            feedback.value += "<b style='color:#b04483'>🔑 ได้รับ Digital Key แล้ว!</b>"
            next_button.description = "ไปห้องถัดไป ➜"
            next_button.layout.display = "block"
        else:
            question_index += 1
            show_next_question_button()
    else:
        feedback.value = "<p style='color:#d62828'><b>❌ ยังไม่ถูกต้อง ลองเลือกอีกครั้งนะ</b></p>"

def go_next_room():
    global room_index, question_index, room_correct, hint_used, game_active
    room_index += 1
    if room_index >= len(ROOMS):
        show_victory()
        return
    question_index = 0
    room_correct = 0
    hint_used = False
    game_active = True
    start_room_timer()
    show_question()

def on_next(_):
    if room_correct < 2:
        show_question()
    else:
        go_next_room()

def on_hint(_):
    global score, hint_used
    if not game_active or hint_used:
        return
    hint_used = True
    score = max(0, score - 2)
    feedback.value = f"<p style='color:#9a6700'>💡 คำใบ้: {ROOMS[room_index]['hint']}<br>หัก 2 คะแนนแล้ว</p>"
    hint_button.disabled = True
    update_status()

def show_victory():
    global game_active
    game_active = False
    stop_timer()
    with main_output:
        clear_output(wait=True)
        display(HTML(f"""<div style='background:#fff0f6;padding:24px;border-radius:18px;text-align:center'>
        <h1 style='color:#c04483'>🎉 YOU ESCAPED! 🎉</h1>
        <h2>คุณหนีออกจากห้องทดลอง Python สำเร็จแล้ว</h2>
        <h1>🏆 คะแนนรวม {score} คะแนน</h1>
        <p>ผ่านครบทั้ง 5 ห้องและได้รับ Digital Keys ครบแล้ว!</p></div>"""))
        display(restart_button)

def start_game(_=None):
    global score, room_index, question_index, room_correct, hint_used, game_active
    stop_timer()
    score, room_index, question_index, room_correct = 0, 0, 0, 0
    hint_used = False
    game_active = True
    with main_output:
        clear_output(wait=True)
        display(widgets.VBox([header, status, timer_label, story, question_box,
                              answer_grid, feedback,
                              widgets.HBox([hint_button, next_button])]))
    start_room_timer()
    show_question()

for i, b in enumerate(answer_buttons):
    b.on_click(lambda _, idx=i: on_answer(idx))
hint_button.on_click(on_hint)
next_button.on_click(on_next)
start_button.on_click(start_game)
restart_button.on_click(start_game)

display(HTML("""
<div style='background:linear-gradient(135deg,#fff0f6,#eef7ff);padding:22px;border:2px solid #f3b6d2;border-radius:18px;text-align:center'>
<h1 style='color:#c04483'>🔐 MISSION PYTHON</h1>
<h3>THE CUTE ESCAPE ROOM</h3>
<p>คุณติดอยู่ในห้องทดลอง AI ที่ระบบรักษาความปลอดภัยขัดข้อง!</p>
<p>ตอบปริศนา Python ทั้ง 5 ห้อง เพื่อรวบรวม Digital Keys และหนีออกไป</p>
<p>✨ ตอบถูก +10 คะแนน　|　💡 คำใบ้ -2 คะแนน　|　⏳ 3 นาทีต่อห้อง</p>
</div>
"""))
display(start_button)
display(main_output)
