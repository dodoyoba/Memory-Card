from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(900,600)

notes = {
    'Добро пожаловать':{
        'текст':'Моё второе приложение',
        'теги':['Заметка','Привет']
    }
}
field_text = QTextEdit()

list_notes_label = QLabel('Список заметок')
list_notes = QListWidget()
button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')

list_tags_label = QLabel('Список тегов')
list_tags = QListWidget()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')

col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)

rov1 = QHBoxLayout()
rov2 = QHBoxLayout()
rov1.addWidget(button_note_create)
rov1.addWidget(button_note_del)
rov2.addWidget(button_note_save)

col2.addLayout(rov1)
col2.addLayout(rov2)

col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
rov3 = QHBoxLayout()
rov4 = QHBoxLayout()
rov3.addWidget(button_tag_add)
rov3.addWidget(button_tag_del)
rov4.addWidget(button_tag_search)

col2.addLayout(rov3)
col2.addLayout(rov4)

main_h = QHBoxLayout()
main_h.addLayout(col1)
main_h.addLayout(col2)

main_win.setLayout(main_h)

def show_notes():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

def add_note():
    note_name,ok=QInputDialog.getText(main_win,'Добавить заметку','Название заметки')
    if ok and note_name != '':
        notes[note_name] = {
            'текст':'',
            'теги':[]
        }
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])

def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json','w',encoding = 'utf-8') as file:
            json.dump(notes,file)
    else:
        print('Заметка для удаления не выбрана')

def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = field_text.toPlainText()
        with open('notes_data.json','w',encoding = 'utf-8') as file:
            json.dump(notes,file)
    else:
        print('Заметка для сохранения не выбрана')

def add_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[name]['теги']:
            notes[name]['теги'].append(tag)
            field_tag.clear()
            with open('notes_data.json','w',encoding = 'utf-8') as file:
                json.dump(notes,file)
    else:
        print('Заметка для добавления тега не выбрана')

def del_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[name]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])
        with open('notes_data.json','w',encoding = 'utf-8') as file:
                json.dump(notes,file)
    else:
        print('Заметка для удаления тега не выбрана')

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        notes_filter = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filter[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filter)
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')

list_notes.itemClicked.connect(show_notes)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
main_win.show()
with open('notes_data.json','r', encoding = 'utf-8') as file:
    notes = json.load(file)
list_notes.addItems(notes)
app.exec_()
