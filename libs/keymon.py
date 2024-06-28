from pynput.keyboard import Key, Listener
import threading

class KeyMon():
    def __init__(self):
        self.listener_thread = threading.Thread(target=self.run_listener)
        self.listener_thread.start()
    
    def run_listener(self):
        # Collect events until released
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        print('{0} pressed'.format(key))

    def on_release(self, key):
        print('{0} release'.format(key))

        if key == Key.esc:
            # Stop listener
            return False
        
    def stop(self):
        print("hi")
        self.listener_thread.join()

keymon = KeyMon()