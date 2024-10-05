import json

# Hàm chuyển đổi datetime sang Unix timestamp
def date_to_timestamp(date_obj):
    return int(date_obj.timestamp())

# Hàm lưu dữ liệu vào file JSON
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
