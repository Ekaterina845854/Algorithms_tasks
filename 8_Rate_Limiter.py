from datetime import datetime, timedelta
import time
import threading

class Stack:
    def __init__(self):
        self.arr = []

    def push(self, val):
        self.arr.append(val)

    def size(self):
        return len(self.arr)

    def pop(self):
        if not self.empty():
            return self.arr.pop()
        return None

    def top(self):
        if not self.empty():
            return self.arr[-1]
        return None

    def empty(self):
        return len(self.arr) == 0

class TokenBucket:
    def __init__(self, token_life = 30, lifespan = 3600 * 24):
        self.token_life = token_life  
        self.tokens = Stack()
        self.running = True
        self.lifespan = lifespan
        self.lock = threading.Lock()

        self.fill_thread = threading.Thread(target=self.fill_bucket, daemon=True)
        self.fill_thread.start()

        self.cleanup_thread = threading.Thread(target=self.cleanup, daemon=True)
        self.cleanup_thread.start()

    def fill_bucket(self):
        while self.running:
            with self.lock:
                self.tokens.push(datetime.now())
            time.sleep(self.token_life)

    def can_allow_request(self):
        with self.lock:
            if self.tokens.size() > 0:
                self.tokens.pop()
                return True
            return False

    def cleanup(self):
        while self.running:
            time.sleep(self.token_life)
            current_time = datetime.now()
            with self.lock:
                while not self.tokens.empty() and (current_time - self.tokens.top()).total_seconds() > self.lifespan:
                    self.tokens.pop()

    def stop(self):
        self.running = False
        self.fill_thread.join()
        self.cleanup_thread.join()

#Пример работы
if __name__ == "__main__":
    bucket = TokenBucket(token_life=30, lifespan=100)

    def request_in_sec(bucket):
        while True:
            time.sleep(1)
            if bucket.can_allow_request():
                print("Запрос обработан")
            else:
                print("Запрос отклонен")

    request_thread = threading.Thread(target=request_in_sec, args=(bucket,), daemon=True)
    request_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Остановка выполнения программы...")
        bucket.stop()
