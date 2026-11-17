import os
import docx

SUBJECTS = [
    {'id': 'toan', 'name': 'Toán', 'icon': '📐'},
    {'id': 'ngu-van', 'name': 'Ngữ văn', 'icon': '📖'},
    {'id': 'tieng-anh', 'name': 'Tiếng Anh', 'icon': '🌐'},
    {'id': 'vat-ly', 'name': 'Vật lý', 'icon': '⚛️'},
    {'id': 'hoa-hoc', 'name': 'Hóa học', 'icon': '🧪'},
    {'id': 'sinh-hoc', 'name': 'Sinh học', 'icon': '🧬'},
    {'id': 'lich-su', 'name': 'Lịch sử', 'icon': '🏛️'},
    {'id': 'dia-ly', 'name': 'Địa lý', 'icon': '🗺️'},
    {'id': 'gdcd', 'name': 'GDCD', 'icon': '⚖️'},
    {'id': 'tin-hoc', 'name': 'Tin học', 'icon': '💻'},
]

def get_lessons_by_subject(subject_id):
    lessons = []
    filename = 'CƠ SỞ DỮ LIỆU NỘI DUNG BÀI HỌC THCS.docx'
    if not os.path.exists(filename): return lessons
    doc = docx.Document(filename)
    subject_map = {'toan': 'MÔN TOÁN', 'ngu-van': 'MÔN NGỮ VĂN', 'tieng-anh': 'MÔN TIẾNG ANH', 'vat-ly': 'MÔN VẬT LÝ', 'hoa-hoc': 'MÔN HÓA HỌC', 'sinh-hoc': 'MÔN SINH HỌC', 'lich-su': 'MÔN LỊCH SỬ', 'dia-ly': 'MÔN ĐỊA LÝ', 'gdcd': 'MÔN GDCD', 'tin-hoc': 'MÔN TIN HỌC'}
    target_section = "PHẦN" if subject_id == 'all' else subject_map.get(subject_id, '')
    current_section = ""
    current_title, current_content = "", []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        if text.upper().startswith("PHẦN"): current_section = text.upper()
        if target_section in current_section or subject_id == 'all':
            if text.startswith("Bài") or text.startswith("## Bài"):
                if current_title: lessons.append({'title': current_title, 'content': "<br>".join(current_content)})
                current_title = text.replace("##", "").strip()
                current_content = []
            else:
                if current_title and "PHẦN" not in text.upper():
                    clean_text = text.replace("o ", "").replace("• ", "").replace("<br>", " ").strip()
                    if clean_text: current_content.append(clean_text)
    if current_title: lessons.append({'title': current_title, 'content': "<br>".join(current_content)})
    return lessons

def get_hsg_exercises():
    exercises = []
    filename = 'CƠ SỞ DỮ LIỆU NỘI DUNG BÀI HỌC THCS.docx'
    if not os.path.exists(filename): return exercises
    doc = docx.Document(filename)
    current_title, current_content = "", []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        if text.startswith("Câu") or text.startswith("## Câu"):
            if current_title: exercises.append({'title': current_title, 'question': current_title, 'solution': "<br>".join(current_content)})
            current_title = text.replace("##", "").strip()
            current_content = []
        else:
            if current_title:
                clean_text = text.replace("<br>", " ").strip()
                if clean_text: current_content.append(clean_text)
    if current_title: exercises.append({'title': current_title, 'question': current_title, 'solution': "<br>".join(current_content)})
    return exercises

PY_EXERCISES = {
    'py-tong-2-so': {'title': 'Tính tổng hai số', 'description': 'Nhập hai số a, b. In ra tổng.', 'starter': 'a, b = map(int, input().split())\nprint(a + b)', 'test_cases': [{'input': '3 5\n', 'expected': '8'}, {'input': '-4 7\n', 'expected': '3'}]}
}

CPP_EXERCISES = {
    'cpp-tong-2-so': {'title': 'Tính tổng hai số (C++)', 'description': 'Nhập hai số a, b. In ra tổng.', 'starter': '#include <iostream>\nusing namespace std;\nint main() {\n    int a, b;\n    cin >> a >> b;\n    cout << a + b;\n    return 0;\n}', 'test_cases': [{'input': '3 5\n', 'expected': '8'}, {'input': '-4 7\n', 'expected': '3'}]}
}