from PIL import Image
import numpy as np

class UndoRedoStack:
    def __init__(self):
        self.stack = []
        self.current_index = -1

    def append(self, obj):
        self.stack = self.stack[:self.current_index + 1]
        self.stack.append(obj)
        self.current_index += 1

    def undo(self):
        if self.current_index > 0:
            self.current_index -= 1
            return self.stack[self.current_index]
        return None

    def redo(self):
        if self.current_index < len(self.stack) - 1:
            self.current_index += 1
            return self.stack[self.current_index]
        return None 

    def active(self):
        if self.current_index >= 0:
            return self.stack[self.current_index]
        return None 

def convert_to_bw(image):
    arr = np.array(image)
    bw_arr = np.mean(arr, axis=2)
    return Image.fromarray(bw_arr)

def mirror_image(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

# Пример использования:
if __name__ == "__main__":
    undo_redo_stack = UndoRedoStack()

    img_path = "D:\Infotecs\i.jpg" 
    original_image = Image.open(img_path)

    undo_redo_stack.append(original_image)

    bw_image = convert_to_bw(original_image)
    undo_redo_stack.append(bw_image)

    mirrored_image = mirror_image(bw_image)
    undo_redo_stack.append(mirrored_image)

    active_image = undo_redo_stack.active()
    active_image.show(title='Изображение')

    previous_image = undo_redo_stack.undo()
    previous_image.show(title='После отмены')

    next_image = undo_redo_stack.redo()
    next_image.show(title='После возврата')