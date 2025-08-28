from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import sys

Window.clearcolor = (1, 1, 1, 1)  # 白色背景

# 問題列表（繁體中文）
KOOS_QUESTIONS_ZH = [
    "1. 以下問題與你的膝蓋疼痛有關, 您多久會感到膝蓋疼痛？\n"
    "1. The following questions are related to your knee pain, how often do you experience knee pain?",
    "2. 過去一週您在平坦路面上行走時感到膝蓋疼痛的程度如何？\n"
    "2. In the past week, how much knee pain did you experience while walking on a flat surface?",
    "3. 過去一週您上落樓梯時感到膝蓋疼痛的程度如何？\n"
    "3. In the past week, how much knee pain did you experience while going up or down stairs?",
    "4. 過去一週您坐著或躺著時感到膝蓋疼痛的程度如何？\n"
    "4. In the past week, how much knee pain did you experience while sitting or lying down?",
    "5. 以下問題與您的身體功能有關, 請說明您上週從坐姿站起來時因膝關節而經歷的困難程度\n"
    "5. The following questions relate to your physical function. In the past week, how difficult\n"
    "was it to rise from a seated position due to your knee condition?",
    "6. 請說明您上週站立時因膝關節而經歷的困難程度\n"
    "6. In the past week, how difficult was it to stand due to your knee condition?",
    "7. 請說明您上週上車或落車時因膝關節而經歷的困難程度\n"
    "7. In the past week, how difficult was it to get in or out of a car due to your knee condition?",
    "8. 請說明您上週扭動或旋轉受傷的膝蓋時因膝關節而經歷的困難程度\n"
    "8. In the past week, how difficult was it to twist or pivot your injured knee due to your knee condition?",
    "9. 以下問題與你的日常生活有關, 你多久會感覺到自己的膝蓋問題? 例如疼痛和不適\n"
    "9. The following questions relate to your daily life. How often do you notice problems with your knee?\n"
    "such as pain or discomfort",
    "10. 您是否改變了自己的生活方式以避免可能損害膝蓋的活動？\n"
    "10. Have you changed your lifestyle to avoid activities that might harm your knee?",
    "11. 你對自己的膝蓋活動能力缺乏信心，這令你困擾的程度有多大？\n"
    "11. How much does your lack of confidence in your knee’s ability to function bother you?",
    "12. 整體來說，您的膝關節給您帶來了多大的困難？\n"
    "12. Overall, how much difficulty has your knee condition caused you?"
]

# 每題對應的選項
CHOICE_SETS = {
    0: ["從不 Never", "每月 Monthly", "每週 Weekly", "每天 Daily", "總是 Always"],
    1: ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    2: ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    3: ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    4: ["無困難 None", " 輕度困難 Mild", "中度困難   Moderate", "重度困難 Severe", "極度困難 Extreme"],
    5: ["無困難 None", " 輕度困難 Mild", "中度困難   Moderate", "重度困難 Severe", "極度困難 Extreme"],
    6: ["無困難 None", " 輕度困難 Mild", "中度困難   Moderate", "重度困難 Severe", "極度困難 Extreme"],
    7: ["無困難 None", " 輕度困難 Mild", "中度困難   Moderate", "重度困難 Severe", "極度困難 Extreme"],
    8: ["從不 Never", "每月 Monthly", "每週 Weekly", "每天 Daily", "不斷地 Constantly"],
    9: ["完全沒有改變 Not at all", "輕微改變 Mildly", "有些改變 Moderately", "嚴重改變 Severely", "完全改變 Totally"],
    10: ["完全沒有困擾 Not at all", "輕微困擾 Mildly", "有些困擾 Moderately", "嚴重困擾 Severely", "極度困擾 Extremely"],
    11: ["完全沒有困難 None", "輕微困難 Mild", "有些困難 Moderate", "非常困難 Severe", "極度困難 Extreme"]
}

answers = {}
FONT_PATH = "TaipeiSansTCBeta-Regular.ttf"
IMAGE_PATH = "ghk_logo.png"  # 請將此檔名改為您上傳的圖片檔案名稱


class KOOSQuestionScreen(Screen):
    def __init__(self, question_text, question_id, choices, **kwargs):
        super().__init__(name=f"question_{question_id}", **kwargs)
        self.question_id = question_id
        self.question_text = question_text
        self.choices = choices
        self.sound = None
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        top_image = Image(source='ghk_logo.png', size_hint_y=None, height=700)
        layout.add_widget(top_image)

        title = Label(
            text='膝關節損傷和膝骨關節炎預後評分\n'
                 'Knee injury and Osteoarthritis Outcome Score-12 (KOOS-12)',
            font_size=72,
            font_name=FONT_PATH,
            bold=True,
            halign='center',
            valign='top',
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=200
        )
        layout.add_widget(title)

        # 顯示問題文字
        layout.add_widget(Label(
            text=question_text,
            font_size=42,
            font_name=FONT_PATH,
            bold=True,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=120,
            color=(0, 0, 0, 1)
        ))

        # 選項按鈕
        self.button_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.button_layout.bind(minimum_height=self.button_layout.setter('height'))

        for choice in choices:
            btn = ToggleButton(
                text=choice,
                group=question_text,
                font_size=42,
                font_name=FONT_PATH,
                bold=True,
                size_hint=(1, None),
                height=60,
                color=(1, 1, 1, 1),
                background_color=(0.6, 0.6, 0.6, 1)
            )
            btn.bind(on_press=self.on_choice_selected)
            self.button_layout.add_widget(btn)

        layout.add_widget(self.button_layout)

        # 導覽按鈕
        nav_layout = BoxLayout(size_hint_y=None, height=80, spacing=20)

        if question_id > 0:
            back_btn = Button(
                text="返回",
                font_size=42,
                font_name=FONT_PATH,
                bold=True,
                background_color=(0.6, 0.7, 0.9, 1),
                color=(1, 1, 1, 1)
            )
            back_btn.bind(on_press=self.go_back)
            nav_layout.add_widget(back_btn)

        if question_id < len(KOOS_QUESTIONS_ZH) - 1:
            next_btn = Button(
                text="繼續",
                font_size=42,
                font_name=FONT_PATH,
                bold=True,
                background_color=(0.4, 0.8, 0.4, 1),
                color=(1, 1, 1, 1)
            )
            next_btn.bind(on_press=self.go_next)
            nav_layout.add_widget(next_btn)
        else:
            submit_btn = Button(
                text="提交",
                font_size=42,
                font_name=FONT_PATH,
                bold=True,
                background_color=(1, 0.8, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            submit_btn.bind(on_press=self.submit_answers)
            nav_layout.add_widget(submit_btn)

        layout.add_widget(nav_layout)
        self.add_widget(layout)

    def on_pre_enter(self):
        audio_file = f"q{self.question_id + 1}.mp3"
        self.sound = SoundLoader.load(audio_file)
        if self.sound:
            self.sound.play()

    def on_choice_selected(self, instance):
        answers[self.question_id] = instance.text

    def go_back(self, instance):
        self.manager.current = f"question_{self.question_id - 1}"

    def go_next(self, instance):
        self.manager.current = f"question_{self.question_id + 1}"

    def submit_answers(self, instance):
        print("使用者回答：")
        for i, answer in answers.items():
            print(f"第{i + 1}題：{KOOS_QUESTIONS_ZH[i]} -> {answer}")
        self.manager.current = "summary"


class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="summary", **kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        top_image = Image(source='ghk_logo.png', size_hint_y=None, height=500)
        layout.add_widget(top_image)
        layout.add_widget(Label(
            text="感謝您參與本次關於膝關節損傷及膝骨關節炎預後評分的問卷調查。您提供的資料對我們非常重要，將有助於港怡醫院\n"
                 "更準確地了解患者的膝關節狀況，並持續提升診斷與治療的質素。本問卷為術前調查，港怡醫院病人聯絡中心職員將會在\n"
                 "術後三個月及六個月以電話 3525 6336 聯絡你，以持續追蹤您的康復情況，並進一步優化治療成效。\n\n"
                 "如有任何疑問或需要進一步協助，歡迎聯絡港怡醫院：\n"
                 "電話： 3153 9000  \n"
                 "電郵： enquiry@gleneagles.hk\n"
                 "衷心祝願您早日康復，重拾健康生活。\n\n\n"
                 "Thank you for participating in this questionnaire regarding the prognosis assessment of knee\n"
                 "injuries and knee osteoarthritis. The information you provide is extremely valuable and will \n"
                 "help Gleneagles Hospital Hong Kong better understand the condition of patients knee joints, while \n"
                 "continuously improving the quality of diagnosis and treatment. This questionnaire is a pre-surgery \n"
                 "survey. Our staff from the Patient Support Call Centre will contact you by phone at 3525 6336 three \n"
                 "months and six months after your surgery to follow up on your recovery and further improve treatment outcomes.\n\n"
                 "If you have any questions or need further assistance, please feel free to contact Gleneagles Hospital Hong Kong:\n"
                 "Phone: 3153 9000 \n"
                 "Email: enquiry@gleneagles.hk \n\n"
                 "Wishing you a speedy recovery and a joyful life.",
            font_size=42,
            font_name=FONT_PATH,
            bold=True,
            halign='center',
            valign='top',
            size_hint=(1, None),
            height=1100,
            color=(0, 0, 0, 1)
        ))
        self.add_widget(layout)


class KOOSApp(App):
    def build(self):
        self.title = "KOOS-12 問卷"
        sm = ScreenManager()
        for i, q in enumerate(KOOS_QUESTIONS_ZH):
            choices = CHOICE_SETS[i]
            sm.add_widget(KOOSQuestionScreen(q, i, choices))
        sm.add_widget(SummaryScreen())
        return sm

KOOSApp().run()




