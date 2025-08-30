from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    "1. 以下問題與你的膝蓋疼痛有關, 您多久會感到膝蓋疼痛？<br>1. How often do you experience knee pain?",
    "2. 過去一週您在平坦路面上行走時感到膝蓋疼痛的程度如何？<br>2. Knee pain while walking on flat surface?",
    "3. 過去一週您上落樓梯時感到膝蓋疼痛的程度如何？<br>3. Knee pain while going up/down stairs?",
    "4. 過去一週您坐著或躺著時感到膝蓋疼痛的程度如何？<br>4. Knee pain while sitting/lying down?",
    "5. 從坐姿站起來時的困難程度<br>5. Difficulty rising from seated position?",
    "6. 站立時的困難程度<br>6. Difficulty standing?",
    "7. 上車或落車時的困難程度<br>7. Difficulty getting in/out of car?",
    "8. 扭動或旋轉膝蓋時的困難程度<br>8. Difficulty twisting/pivoting knee?",
    "9. 你多久感覺到膝蓋問題？<br>9. How often do you notice knee problems?",
    "10. 是否改變生活方式以避免傷害膝蓋？<br>10. Changed lifestyle to protect knee?",
    "11. 缺乏信心造成的困擾程度<br>11. How much does lack of confidence in knee bother you?",
    "12. 整體膝蓋困難程度<br>12. Overall difficulty caused by knee condition?"
]

choices = [
    ["從不 Never", "每月 Monthly", "每週 Weekly", "每天 Daily", "總是 Always"],
    ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    ["無疼痛 None", "輕度疼痛 Mild", "中度疼痛 Moderate", "重度疼痛 Severe", "極度疼痛 Extreme"],
    ["無困難 None", "輕度困難 Mild", "中度困難 Moderate", "重度困難 Severe", "極度困難 Extreme"],
    ["無困難 None", "輕度困難 Mild", "中度困難 Moderate", "重度困難 Severe", "極度困難 Extreme"],
    ["無困難 None", "輕度困難 Mild", "中度困難 Moderate", "重度困難 Severe", "極度困難 Extreme"],
    ["無困難 None", "輕度困難 Mild", "中度困難 Moderate", "重度困難 Severe", "極度困難 Extreme"],
    ["從不 Never", "每月 Monthly", "每週 Weekly", "每天 Daily", "不斷地 Constantly"],
    ["完全沒有改變 Not at all", "輕微改變 Mildly", "有些改變 Moderately", "嚴重改變 Severely", "完全改變 Totally"],
    ["完全沒有困擾 Not at all", "輕微困擾 Mildly", "有些困擾 Moderately", "嚴重困擾 Severely", "極度困擾 Extremely"],
    ["完全沒有困難 None", "輕微困難 Mild", "有些困難 Moderate", "非常困難 Severe", "極度困難 Extreme"]
]

consent_text = """
<h2>膝關節損傷與骨關節炎結果問卷研究參與知情同意書</h2>
<p>感謝您選擇香港港怡醫院作為您的醫療照護機構。我們衷心感謝您一直以來對我們的信任與支持。現誠摯邀請您參與一項關於膝關節健康的研究問卷調查。透過這份簡短的問卷，我們希望能更全面了解您的膝關節症狀與日常活動狀況。您所提供的資料將僅用於醫學研究及服務品質提升，幫助我們持續改進醫療服務。</p>
<p><strong>問卷目的:</strong> 本問卷旨在更深入了解您的膝關節狀況，協助臨床團隊更好地掌握您的康復進展，並為您制定更合適的個人化治療計劃。</p>
<p><strong>自願參與:</strong> 參與本問卷完全出於自願。您可以隨時選擇退出，這不會影響您在本院接受的任何醫療服務。</p>
<p><strong>資料保密:</strong> 您的所有資料都將被嚴格保密，僅供研究及臨床品質改善使用。任何公開報告中均不會披露您的個人身份資訊。</p>
<p><strong>填寫指引:</strong> 請根據您目前的實際情況，選擇最符合的選項。若有不確定之處，請選擇最接近您實際感受的答案。每題請僅選擇一個答案。</p>
<p>繼續填寫本問卷即表示您已閱讀、理解並同意上述內容，自願參與本研究。</p>
<p>誠摯感謝您的參與及支持，您的意見對我們非常重要。</p>
<hr>
<h2>Informed Consent for Participation in the Knee Injury and Osteoarthritis Outcome Questionnaire</h2>
<p>Thank you for choosing Gleneagles Hospital Hong Kong for your healthcare needs. We truly value your trust and are committed to supporting your well-being.</p>
<p>You are warmly invited to take part in a research study that involves completing a questionnaire about your knee health. This will include questions related to your current symptoms and daily activities. All information gathered will be used solely for medical research and to further improve the quality of care we provide.</p>
<p><strong>Purpose of the Questionnaire:</strong> This questionnaire aims to better understand your knee condition. Your input will help our clinical team monitor your recovery and develop treatment plans that are tailored to your individual needs.</p>
<p><strong>Voluntary Participation:</strong> Participation is entirely voluntary. You are free to decline or withdraw at any time without affecting your current or future medical care at our hospital.</p>
<p><strong>Confidentiality:</strong> Your responses will be kept strictly confidential and will be used only for research and clinical quality improvement. No personally identifiable information will be published or shared in any study reports.</p>
<p><strong>Instructions:</strong> For each question, please select the answer that best reflects your current experience. If you are uncertain, choose the option that most closely matches your situation. Only one response should be selected per question.</p>
<p>By continuing with the questionnaire, you confirm that you have read and understood this information, and you voluntarily agree to participate in this study.</p>
<p>We sincerely thank you for your time and support. Your contribution is greatly appreciated.</p>
<form method='post'><button type='submit'>我同意並繼續 I Agree and Continue</button></form>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hn = request.form.get('hospital_number')
        session['hospital_number'] = hn
        session['responses'] = {}
        return redirect(url_for('consent'))

    html = """
    <h2>問卷開始前</h2>
    <form method="post">
        <label for="hospital_number">Hospital Number (HN250000XXXX):</label><br>
        <input type="text" id="hospital_number" name="hospital_number" required><br><br>
        <button type="submit">開始問卷</button>
    </form>
    """
    return render_template_string(html)

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        return redirect(url_for('question', qnum=0))
    return render_template_string(consent_text)

@app.route('/question/<int:qnum>', methods=['GET', 'POST'])
def question(qnum):
    if 'responses' not in session:
        session['responses'] = {}

    responses = session['responses']

    if request.method == 'POST':
        responses[str(qnum)] = request.form.get('answer')
        session['responses'] = responses

        if 'next' in request.form and qnum < len(questions) - 1:
            return redirect(url_for('question', qnum=qnum + 1))
        elif 'back' in request.form and qnum > 0:
            return redirect(url_for('question', qnum=qnum - 1))
        elif 'submit' in request.form:
            return redirect(url_for('submit'))

    question_text = questions[qnum]
    options = choices[qnum]
    selected = responses.get(str(qnum), '')

    html = f"""
    <h2>問題 {qnum + 1}</h2>
    <p>{question_text}</p>
    <form method='post'>
    {''.join([f"<input type='radio' name='answer' value='{opt}' {'checked' if opt == selected else ''}> {opt}<br>" for opt in options])}
    <br>
    {'<button type="submit" name="back">上一題</button>' if qnum > 0 else ''}
    {'<button type="submit" name="next">下一題</button>' if qnum < len(questions) - 1 else ''}
    {'<button type="submit" name="submit">提交</button>' if qnum == len(questions) - 1 else ''}
    </form>
    """
    return render_template_string(html)

@app.route('/submit')
def submit():
    responses = session.get('responses', {})
    hn = session.get('hospital_number', '未提供')
    result_html = f"<h2>感謝您完成問卷！</h2><p>Hospital Number: {hn}</p><ul>"
    for i in range(len(questions)):
        answer = responses.get(str(i), '未回答')
        result_html += f"<li>問題 {i+1}: {answer}</li>"
    result_html += "</ul>"
    return render_template_string(result_html)

if __name__ == '__main__':
    app.run(debug=True)



