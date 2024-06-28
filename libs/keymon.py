from pynput.keyboard import Key, Listener

class KeyMon():
    DEFAULT_EXIT_KEY = Key.pause
    DEFAULT_RUN_KEY = Key.f9
    DEFAULT_STOP_KEY = Key.f10

    def __init__(self, start_callback=None, stop_callback=None, exit_key=DEFAULT_EXIT_KEY, run_key=DEFAULT_RUN_KEY, stop_key=DEFAULT_STOP_KEY):
        # Allow for custom callbacks to handle start/stop key events
        if start_callback is None:
            print("No start callback provided... Good luck starting capture? 🤷")
        
        if stop_callback is None:
            print("No stop callback provided... Good luck stopping capture? 🤷")
        
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.run_key = run_key
        self.stop_key = stop_key
        self.exit_key = exit_key
        self.do_exit = False
        self.listener = None
        
        self.run_listener()
        print(f"Watching for keyboard hotkeys now...")
        print(f"👉    Press {self.run_key} to start capture")
        print(f"👉    Press {self.stop_key} to stop capture")
        print(f"👉    Press {self.exit_key} to exit")
    
    #def run_listener(self, press_watcher, release_watcher):
    def run_listener(self):
        # Collect events until released
        self.listener = Listener(on_release=self.on_release)
        self.listener.start()

    # Handle key press events
    def on_release(self, key):
        #print('{0} release'.format(key)) #DEBUG
        if key == self.run_key and self.start_callback != None:
            self.start_callback()
        elif key == self.stop_key and self.stop_callback != None:
            self.stop_callback()
        elif key == self.exit_key:
            self.do_exit = True
            return False

    # Stop listener, cleanup thread
    def stop(self):
        if hasattr(self, 'listener') and self.listener:  # Check if the listener exists
            self.listener.stop()  # Stop the listener
