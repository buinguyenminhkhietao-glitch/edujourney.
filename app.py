from flask import Flask, render_template, abort, request, session
from data_manager import get_lessons_by_subject, SUBJECTS, get_hsg_exercises
import os  # cần cho phần ghi file bài học

app = Flask(__name__)
app.secret_key = 'admin kha noob'  # Cần thiết cho session
ADMIN_PASSWORD = ".--..--..-. -.-.....- -.-------..."  # Mật khẩu admin

@app.route('/')
def index():
    return render_template('index.html', subjects=SUBJECTS)

@app.route('/study/<subject_id>')
def study(subject_id):
    subject_name = next((s['name'] for s in SUBJECTS if s['id'] == subject_id), None)
    if not subject_name:
        abort(404)
    lessons = get_lessons_by_subject(subject_id)
    return render_template('study.html', lessons=lessons, subject_name=subject_name)

@app.route('/hsg')
def hsg():
    return render_template('hsg.html', exercises=get_hsg_exercises())

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    is_logged_in = session.get('admin_logged_in', False)

    if request.method == 'POST':
        if 'password' in request.form:
            # ✅ Sửa: dùng ADMIN_PASSWORD thay vì MORSE_PASSWORD
            if " ".join(request.form.get('password', '').split()) == ADMIN_PASSWORD:
                session['admin_logged_in'] = True
                is_logged_in = True
            else:
                error = "Mã Morse sai rồi!"

        elif 'add_lesson' in request.form and is_logged_in:
            subject_id = request.form.get('subject_id')
            title = request.form.get('title')
            content = request.form.get('content')

            file_name = subject_id.replace('-', '_') + '.txt'
            file_path = os.path.join('data', file_name)

            if os.path.exists(file_path):
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{title}\n{content}\n")
                session['message'] = f"Đã thêm bài '{title}' thành công!"
            else:
                error = f"Không tìm thấy file {file_name} để ghi!"

    msg = session.pop('message', None)
    return render_template('admin.html', error=error, is_logged_in=is_logged_in, msg=msg, subjects=SUBJECTS)

if __name__ == '__main__':
    # Sửa host thành 0.0.0.0 và lấy port từ biến môi trường của Render (nếu có)
    import os
    port = int(os.environ.get("PORT", 9000))
    app.run(host='0.0.0.0', port=port)