import os, sys, subprocess, tempfile
from flask import Flask, render_template, request, abort, send_file
from data import SUBJECTS, PY_EXERCISES, CPP_EXERCISES, get_lessons_by_subject, get_hsg_exercises

app = Flask(__name__)
SUBJECT_MAP = {s['id']: s for s in SUBJECTS}

# --- MẬT KHẨU ADMIN ---
ADMIN_PASSWORD = "nemchuathanhhoa36"
CODE_ADMIN_PASSWORD = "cpp_hardcore_hon_python"

# --- HÀM CHẠY CODE (HỖ TRỢ CẢ PYTHON VÀ C++) ---
def run_code(code, stdin_data, lang='python', timeout=5):
    if lang == 'cpp':
        fd, path = tempfile.mkstemp(suffix='.cpp', text=True)
        out_path = path.replace('.cpp', '.exe')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write(code)
            compile_res = subprocess.run(['g++', path, '-o', out_path], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return '', f"Lỗi biên dịch:\n{compile_res.stderr}", -1
            res = subprocess.run([out_path], input=stdin_data, capture_output=True, text=True, timeout=timeout)
            return res.stdout.strip(), res.stderr.strip(), res.returncode
        except subprocess.TimeoutExpired: return '', 'Lỗi: Timeout', -1
        finally:
            try: os.unlink(path)
            except: pass
            try: os.unlink(out_path)
            except: pass
    else:
        fd, path = tempfile.mkstemp(suffix='.py', text=True)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write(code)
            res = subprocess.run([sys.executable, path], input=stdin_data, capture_output=True, text=True, timeout=timeout)
            return res.stdout.strip(), res.stderr.strip(), res.returncode
        except subprocess.TimeoutExpired: return '', 'Lỗi: Timeout', -1
        finally:
            try: os.unlink(path)
            except: pass

# --- ROUTES ---
@app.route('/')
def index(): return render_template('index.html', subjects=SUBJECTS)

@app.route('/study')
def all_study():
    lessons = get_lessons_by_subject('all')
    return render_template('study.html', subject={'name': 'Tất cả môn học'}, lessons=lessons)

@app.route('/study/<subject_id>')
def study(subject_id):
    subj = SUBJECT_MAP.get(subject_id)
    if not subj: abort(404)
    lessons = get_lessons_by_subject(subject_id)
    return render_template('study.html', subject=subj, lessons=lessons)

@app.route('/hsg', methods=['GET', 'POST'])
def hsg():
    exercises = get_hsg_exercises() 
    ex_id = request.args.get('id', 0)
    try: ex = exercises[int(ex_id)]
    except: ex = exercises[0] if exercises else None
    
    show_sol, user_ans = False, ""
    if request.method == 'POST':
        user_ans, show_sol = request.form.get('answer', ''), True
    return render_template('hsg.html', exercises=exercises, current=int(ex_id), exercise=ex, show_solution=show_sol, user_answer=user_ans)

@app.route('/tin', methods=['GET', 'POST'])
def tin():
    lang = request.args.get('lang') or request.form.get('lang') or 'python'
    
    if lang == 'cpp':
        auth = request.args.get('pass') or request.form.get('pass')
        if auth != CODE_ADMIN_PASSWORD: 
            return "<h2 style='text-align:center; margin-top:50px; color:red;'>Lỗi 403: Chức năng C++ chỉ dành cho Admin!</h2>", 403

    exercises = PY_EXERCISES if lang == 'python' else CPP_EXERCISES
    ex_id = request.args.get('ex') or request.form.get('exercise_id') or next(iter(exercises))
    if ex_id not in exercises: ex_id = next(iter(exercises))
        
    ex = exercises[ex_id]
    code = ex['starter']
    results, summary = None, None
    
    if request.method == 'POST':
        code = request.form.get('code', '')
        results, passed = [], 0
        for idx, tc in enumerate(ex['test_cases'], 1):
            out, err, rc = run_code(code, tc['input'], lang)
            ok = (rc == 0 and out.strip() == tc['expected'].strip())
            if ok: passed += 1
            results.append({'index': idx, 'input': tc['input'], 'expected': tc['expected'], 'got': out if rc == 0 else err, 'passed': ok})
        summary = {'passed': passed, 'total': len(ex['test_cases'])}
    
    template_name = 'tin_cpp.html' if lang == 'cpp' else 'tin_py.html'
    return render_template(template_name, exercises=exercises, current=ex_id, code=code, results=results, summary=summary, lang=lang)

# --- TRANG ADMIN ---
@app.route('/admin')
def admin_dashboard():
    if request.args.get('pass') != ADMIN_PASSWORD: 
        return "<h2 style='text-align:center; margin-top:50px; color:red;'>Lỗi 403: Mật khẩu Admin sai!</h2>", 403
    
    thuong = get_lessons_by_subject('all')
    hsg = get_hsg_exercises()
    
    # Thống kê số bài theo môn
    subject_stats = {}
    for les in thuong:
        parts = les['title'].split()
        if len(parts) > 0:
            mon = parts[0]
            if mon not in subject_stats:
                subject_stats[mon] = 0
            subject_stats[mon] += 1

    return render_template('admin.html', 
                           total_thuong=len(thuong), 
                           total_hsg=len(hsg), 
                           subject_stats=subject_stats,
                           pass_word=ADMIN_PASSWORD, 
                           code_pass=CODE_ADMIN_PASSWORD)

@app.route('/download-docx')
def download_docx():
    if request.args.get('pass') != ADMIN_PASSWORD:
        return "<h2 style='text-align:center; margin-top:50px; color:red;'>Lỗi 403: Bạn không có quyền tải file này!</h2>", 403
    
    try:
        return send_file('CƠ SỞ DỮ LIỆU NỘI DUNG BÀI HỌC THCS.docx', as_attachment=True)
    except Exception as e:
        return f"Lỗi không tìm thấy file: {e}", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True, use_reloader=False)