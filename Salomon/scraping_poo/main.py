from utils.file_handler import FileHandler

data = [
    {"title": "News 1", "category": "tech", "author": "John"},
    {"title": "News 2", "category": "business", "author": "Anna"},
]

handler = FileHandler("data/processed")

handler.save_json(data, "news.json")
handler.save_csv(data, "news.csv")
handler.export_excel(data, "news.xlsx")