import os
import pygetwindow as gw
import win32gui
import win32process
import win32api
import win32con
import pyautogui
import time
import threading
from pynput import keyboard
import Wordlist



class WordChanger:
    def __init__(self, min_length=3):
        self.current_word = ''
        self.replacement = Wordlist.word_list
        self.is_chat_open = False
        self.min_length = min_length

    def get_active_window_executable_path(self):
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            executable_path = win32process.GetModuleFileNameEx(handle, 0)
            return executable_path
        except Exception as e:
            return None

    def is_specific_program_active(self, program_path):
        active_program_path = self.get_active_window_executable_path()
        return active_program_path and os.path.normpath(active_program_path) == os.path.normpath(program_path)

    def chat_open_check(self, key):
        if key == keyboard.Key.enter:
            self.is_chat_open = not self.is_chat_open
        elif key == keyboard.Key.esc and self.is_chat_open:
            self.is_chat_open = False

    def on_press(self, key):
        if not self.is_specific_program_active('C:\\Riot Games\\League of Legends\\Game\\League of Legends.exe'):
            return

        self.chat_open_check(key)
        if self.is_chat_open:
            try:
                char = key.char
            except AttributeError:
                char = None

            if key == keyboard.Key.backspace and len(self.current_word) > 0:
                self.current_word = self.current_word[:-1]
                return

            if char is None or char.isspace():
                self.current_word = ''
            else:
                self.current_word += char

                for word in self.replacement.keys():
                    if word.startswith(self.current_word):
                        if self.current_word in self.replacement or len(self.current_word) >= self.min_length:
                            replacement = self.replacement.get(word)
                            if replacement:
                                pyautogui.press('backspace', presses=len(self.current_word))
                                pyautogui.typewrite(replacement)
                                self.current_word = ''
                                break



word_changer = WordChanger(min_length=4)

def print_chat_status():
    while True:
        print(f"Chat open: {word_changer.is_chat_open}")
        time.sleep(1)


status_thread = threading.Thread(target=print_chat_status)
status_thread.daemon = True
status_thread.start()

with keyboard.Listener(on_press=word_changer.on_press) as listener:
    listener.join()
