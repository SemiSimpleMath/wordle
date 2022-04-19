
"""
This is a wordl solver


"""
from collections import defaultdict

import prune
import utils



 #utility funtions
# we are given a string s that looks like num,num;num,num and we want to convert it to a list
# of tuples [(num, num), (num, num), ...]
def convert_to_tuple_list(s):

    s_list = s.split(";")
    result = []
    for i, val in enumerate(s_list):
        val_list = val.split(",")
        if len(val_list) < 2:
            return result
        pos, let = val_list[0], val_list[1]
        result.append((pos, let))
    return result



def compute_suggestion(s):

    global text_suggestion
    global contains_dicts
    global doesnt_contain_dicts
    contains_dicts = utils.create_contains_dicts(s)

    doesnt_contain_dicts = utils.create_doesnt_contain_dicts(s)

    index_dict = utils.compute_index(s, contains_dicts, doesnt_contain_dicts)

    min_val = 999
    for key, val in index_dict.items():
        if val < min_val:
            min_key = key
            min_val = val
    text_suggestion.delete(1.0,"end")
    text_suggestion.insert(1.0, min_key)

def get_data():
    correct_letters_wrong_place = set()
    correct_letters_exact_place = set()
    incorrect_letters = []

    global button_obj_list
    global button_state_list
    global contains_dicts
    global doesnt_contain_dicts
    global all_words
    global text_widget
    global row_number

    for i in range(5):
        button_letter = button_obj_list[i + row_number*5]['text']
        button_state = button_state_list[i + row_number*5]

        if button_state == 0:
            incorrect_letters.append(button_letter)
        if button_state == 1:
            correct_letters_wrong_place.add((i, button_letter))
        if button_state == 2:
            correct_letters_exact_place.add((i, button_letter))
    all_words = utils.find_next_word(contains_dicts, doesnt_contain_dicts, all_words, correct_letters_wrong_place, correct_letters_exact_place, incorrect_letters)
    word_string = ""
    for item in all_words:
        word_string += item + " "

    text_widget.delete(1.0,"end")
    text_widget.insert(1.0, word_string)

    compute_suggestion(all_words)
    create_next_button_group()


def clicked(id):
    global button_state_list
    global button_obj_list
    button_state = button_state_list[id]
    btn = button_obj_list[id]
    if button_state == 0:
        btn.configure(bg="orange", fg= "black")
        button_state = 1
    elif button_state == 1:
        btn.configure(bg="green", fg= "white")
        button_state = 2
    elif button_state == 2:
        btn.configure(bg="gray", fg= "white")
        button_state = 0

    button_state_list[id] = button_state


from tkinter import *

#globals for tkinter (yuck)
button_state_list = []
button_obj_list = []
global_key_counter = 0


def keyup(e):
    global global_key_counter
    global button_state_list
    global button_obj_list
    global row_number

    if row_number == 6:
        return

    if e.keysym != "BackSpace":
        if global_key_counter == 5:
            return
        button_obj_list[global_key_counter + row_number * 5]['text'] = e.char
        global_key_counter+=1
    else:
        if global_key_counter > 0:
            global_key_counter -= 1
        button_obj_list[global_key_counter + row_number * 5]['text'] = ""


def create_next_button_group():
    global window
    global button_state_list
    global button_obj_list
    global row_number
    global global_key_counter

    if row_number == 6:
        return
    row_number += 1
    for i in range(0, 5):
        id = i + row_number * 5
        button_obj_list.append(Button(window, bg="gray", fg="white", text="", font=('Arial', 30), command=lambda id=id: clicked(id)))
        button_obj_list[id].place(x=100 * i + 100, y = 100 + 100 * row_number, width=50, height=50)
        button_state_list.append(0)

    global_key_counter = 0

def run_gui():



    global window
    global text_widget
    global text_suggestion

    window.title("Welcome to Wordle solver!")

    window.geometry('800x1000')
    window.bind("<KeyRelease>", keyup)

    create_next_button_group()

    grab_info_btn = Button(window, text="Run", command=get_data)

    grab_info_btn.place(x=600, y=900)

    text_widget = Text(window)
    text_widget.place(x = 20, y = 600, height = 150, width = 760)
    text_suggestion = Text(window)
    text_suggestion.place(x = 330, y = 850, height = 50, width = 100)


    window.mainloop()



all_words = utils.load_words()

print("Total words: ", len(all_words))


contains_dicts = utils.create_contains_dicts(all_words)

doesnt_contain_dicts = utils.create_doesnt_contain_dicts(all_words)

window = Tk()
text_widget = None
text_suggestion = None
row_number = -1
run_gui()