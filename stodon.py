import tkinter as tk
from tkinter import messagebox, Menu
import json
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

def add_task(event=None):
    task = task_entry.get()
    if task:
        tasks.append({"task": task, "completed": False})
        task_entry.delete(0, tk.END)
        update_task_list()
        save_tasks(tasks)

def update_task_list():
    task_list.delete(0, tk.END)
    completed_list.delete(0, tk.END)
    for task in tasks:
        if task['completed']:
            completed_list.insert(tk.END, task['task'])
        else:
            task_list.insert(tk.END, task['task'])

def complete_task(event=None):
    selected_index = task_list.curselection()
    if selected_index:
        tasks[selected_index[0]]['completed'] = True
        update_task_list()
        save_tasks(tasks)

def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        tasks.pop(selected_index)
        update_task_list()
        save_tasks(tasks)
    except IndexError:
        try:
            selected_index = completed_list.curselection()[0]
            tasks.pop(selected_index)
            update_task_list()
            save_tasks(tasks)
        except IndexError:
            messagebox.showwarning("Warning", "Choose task to delete!")

def reactivate_task(event=None):
    selected_index = completed_list.curselection()
    if selected_index:
        tasks[selected_index[0]]['completed'] = False
        update_task_list()
        save_tasks(tasks)

root = tk.Tk()
root.title("Stodon")

menu = Menu(root)
root.config(menu=menu)

new_task_label = tk.Label(root, text="New task name")
new_task_label.pack(pady=2)

task_entry = tk.Entry(root, width=20)
task_entry.pack(pady=2)
task_entry.bind('<Return>', add_task)

add_button = tk.Button(root, text="Add task", command=add_task)
add_button.pack(pady=2)

active_tasks_label = tk.Label(root, text="Active tasks")
active_tasks_label.pack(anchor='w', padx=10)

task_list = tk.Listbox(root, width=50, height=10, selectmode=tk.BROWSE)
task_list.pack(pady=10, anchor='w', padx=10)
task_list.bind('<Double-Button-1>', complete_task)

completed_tasks_label = tk.Label(root, text="Completed Tasks")
completed_tasks_label.pack(anchor='w', padx=10)

completed_list = tk.Listbox(root, width=50, height=5, selectmode=tk.BROWSE)
completed_list.pack(pady=10, anchor='w', padx=10)
completed_list.bind('<Double-Button-1>', reactivate_task)

delete_button = tk.Button(root, text="Delete task", command=delete_task)
delete_button.pack(pady=5)

tasks = load_tasks()
update_task_list()

root.mainloop()