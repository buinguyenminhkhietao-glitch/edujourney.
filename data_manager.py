import os

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
    {'id': 'cong-nghe', 'name': 'Công nghệ', 'icon': '🛠️'},
]

def get_lessons_by_subject(subject_id):
    file_name_1 = subject_id.replace('-', '_') + '.txt'
    file_name_2 = subject_id.replace('-', '') + '.txt'
    
    file_path = os.path.join('data', file_name_1)
    if not os.path.exists(file_path):
        file_path = os.path.join('data', file_name_2)
        
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Lỗi đọc file {file_path}: {e}")
        return []
        
    lessons = []
    current_title, current_content = "", []
    
    for line in lines:
        text = line.strip()
        if not text: continue
        
        # Nhận diện tiêu đề bài học mới (linh hoạt hơn)
        if text.startswith("Bài") or text.startswith("Chương") or text.startswith("Lớp") or text.startswith("Phần"):
            if current_title: 
                lessons.append({'title': current_title, 'content': "<br>".join(current_content)})
            current_title = text.strip()
            current_content = []
        else:
            if current_title:
                clean_text = text.replace("•", "").replace("o ", "").strip()
                if clean_text: current_content.append(clean_text)
                    
    if current_title: 
        lessons.append({'title': current_title, 'content': "<br>".join(current_content)})
        
    return lessons

def get_hsg_exercises():
    return [
        {'title': 'Câu 1: Vật lý (HSG)', 'question': 'Một túi đường 2,5kg. Tính trọng lượng?', 'solution': 'P = 10 * m = 10 * 2,5 = 25 (N).'},
        {'title': 'Câu 2: Toán (HSG)', 'question': 'Tìm x: 2x + 15 = 31.', 'solution': '2x = 16 => x = 8.'}
    ]