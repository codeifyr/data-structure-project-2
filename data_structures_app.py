import tkinter as tk
from tkinter import ttk, messagebox
import random
from tkinter.scrolledtext import ScrolledText
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Dequeue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.count = 0
        self.operations_history = []

    def create(self):
        self.front = None
        self.rear = None
        self.count = 0
        self.operations_history = []
        self._add_to_history("Dequeue created")

    def _add_to_history(self, operation):
        timestamp = time.strftime("%H:%M:%S")
        self.operations_history.append(f"[{timestamp}] {operation}")

    def insertFront(self, value):
        new_node = Node(value)
        if not self.front:
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front = new_node
        self.count += 1
        self._add_to_history(f"Inserted {value} at front")

    def insertRear(self, value):
        new_node = Node(value)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.count += 1
        self._add_to_history(f"Inserted {value} at rear")

    def removeFront(self):
        if not self.front:
            raise ValueError("Dequeue is empty")
        value = self.front.value
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.count -= 1
        self._add_to_history(f"Removed {value} from front")
        return value

    def removeRear(self):
        if not self.front:
            raise ValueError("Dequeue is empty")
        if self.front == self.rear:
            value = self.front.value
            self.front = self.rear = None
            self.count -= 1
            self._add_to_history(f"Removed {value} from rear")
            return value
        current = self.front
        while current.next != self.rear:
            current = current.next
        value = self.rear.value
        self.rear = current
        self.rear.next = None
        self.count -= 1
        self._add_to_history(f"Removed {value} from rear")
        return value

    def size(self):
        return self.count

    def get_values(self):
        values = []
        current = self.front
        while current:
            values.append(str(current.value))
            current = current.next
        return values

    def get_history(self):
        return self.operations_history

class SortingAlgorithms:
    @staticmethod
    def bubble_sort(arr, callback=None):
        n = len(arr)
        comparisons = 0
        swaps = 0
        for i in range(n):
            for j in range(0, n-i-1):
                comparisons += 1
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swaps += 1
            if callback:
                callback(arr.copy(), i+1, comparisons, swaps)
        return arr, comparisons, swaps

    @staticmethod
    def selection_sort(arr, callback=None):
        n = len(arr)
        comparisons = 0
        swaps = 0
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1
            if callback:
                callback(arr.copy(), i+1, comparisons, swaps)
        return arr, comparisons, swaps

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Data Structures & Algorithms")
        self.geometry("1000x800")
        self.configure(bg="#f0f0f0")

        # Set theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('Custom.TButton', padding=10, font=('Helvetica', 10))
        self.style.configure('Custom.TLabel', font=('Helvetica', 10))
        self.style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))

        # Initialize data structures
        self.dequeue = Dequeue()

        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(expand=True, fill="both")

        # Create tabs
        self.dequeue_frame = ttk.Frame(self.notebook)
        self.sorting_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.dequeue_frame, text="Dequeue Operations")
        self.notebook.add(self.sorting_frame, text="Sorting Algorithms")

        self.setup_dequeue_interface()
        self.setup_sorting_interface()

    def setup_dequeue_interface(self):
        left_panel = ttk.Frame(self.dequeue_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        right_panel = ttk.Frame(self.dequeue_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        operations_frame = ttk.LabelFrame(left_panel, text="Operations", padding=10)
        operations_frame.pack(fill="x", pady=5)

        input_frame = ttk.Frame(operations_frame)
        input_frame.pack(fill="x", pady=5)

        ttk.Label(input_frame, text="Value:").pack(side="left", padx=5)
        self.value_entry = ttk.Entry(input_frame, width=10)
        self.value_entry.pack(side="left", padx=5)

        buttons_frame = ttk.Frame(operations_frame)
        buttons_frame.pack(fill="x", pady=5)

        ttk.Button(buttons_frame, text="Insert Front", style='Custom.TButton', command=self.insert_front).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Insert Rear", style='Custom.TButton', command=self.insert_rear).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Remove Front", style='Custom.TButton', command=self.remove_front).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Remove Rear", style='Custom.TButton', command=self.remove_rear).pack(side="left", padx=5)

        visual_frame = ttk.LabelFrame(left_panel, text="Dequeue Visualization", padding=10)
        visual_frame.pack(fill="both", expand=True, pady=5)

        self.dequeue_content = ScrolledText(visual_frame, height=10, width=50)
        self.dequeue_content.pack(fill="both", expand=True)

        history_frame = ttk.LabelFrame(right_panel, text="Operations History", padding=10)
        history_frame.pack(fill="both", expand=True)

        self.history_content = ScrolledText(history_frame, height=30, width=40)
        self.history_content.pack(fill="both", expand=True)

    def setup_sorting_interface(self):
        control_frame = ttk.LabelFrame(self.sorting_frame, text="Controls", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill="x", pady=5)

        ttk.Label(input_frame, text="Number of elements:").pack(side="left", padx=5)
        self.elements_entry = ttk.Entry(input_frame, width=10)
        self.elements_entry.pack(side="left", padx=5)

        ttk.Button(input_frame, text="Generate Random Numbers", style='Custom.TButton', command=self.generate_numbers).pack(side="left", padx=5)

        algo_frame = ttk.Frame(control_frame)
        algo_frame.pack(fill="x", pady=5)

        self.sort_algorithm = tk.StringVar(value="bubble")
        ttk.Radiobutton(algo_frame, text="Bubble Sort", variable=self.sort_algorithm, value="bubble").pack(side="left", padx=5)
        ttk.Radiobutton(algo_frame, text="Selection Sort", variable=self.sort_algorithm, value="selection").pack(side="left", padx=5)
        ttk.Button(algo_frame, text="Sort", style='Custom.TButton', command=self.sort_array).pack(side="left", padx=5)

        stats_frame = ttk.LabelFrame(self.sorting_frame, text="Statistics", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=5)

        self.stats_label = ttk.Label(stats_frame, text="")
        self.stats_label.pack(fill="x")

        progress_frame = ttk.LabelFrame(self.sorting_frame, text="Sorting Progress", padding=10)
        progress_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.sorting_content = ScrolledText(progress_frame, height=20, width=50)
        self.sorting_content.pack(fill="both", expand=True)

        self.current_array = []

    def insert_front(self):
        try:
            value = int(self.value_entry.get())
            self.dequeue.insertFront(value)
            self.update_dequeue_display()
            self.update_history_display()
            self.value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def insert_rear(self):
        try:
            value = int(self.value_entry.get())
            self.dequeue.insertRear(value)
            self.update_dequeue_display()
            self.update_history_display()
            self.value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def remove_front(self):
        try:
            value = self.dequeue.removeFront()
            self.update_dequeue_display()
            self.update_history_display()
            messagebox.showinfo("Removed", f"Removed value: {value}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_rear(self):
        try:
            value = self.dequeue.removeRear()
            self.update_dequeue_display()
            self.update_history_display()
            messagebox.showinfo("Removed", f"Removed value: {value}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_dequeue_display(self):
        values = self.dequeue.get_values()
        self.dequeue_content.delete(1.0, tk.END)
        self.dequeue_content.insert(tk.END, f"Size: {self.dequeue.size()}\n\n")
        self.dequeue_content.insert(tk.END, f"Content: {' -> '.join(values) if values else 'Empty'}\n\n")
        self.dequeue_content.insert(tk.END, "Structure:\n")
        if values:
            for i, value in enumerate(values):
                self.dequeue_content.insert(tk.END, f"Node {i+1}: {value}\n")

    def update_history_display(self):
        self.history_content.delete(1.0, tk.END)
        for operation in self.dequeue.get_history():
            self.history_content.insert(tk.END, f"{operation}\n")
        self.history_content.see(tk.END)

    def generate_numbers(self):
        try:
            n = int(self.elements_entry.get())
            if n <= 0:
                raise ValueError("Number must be positive")
            if n > 100:
                raise ValueError("Please use 100 or fewer elements")
            self.current_array = [random.randint(1, 100) for _ in range(n)]
            self.sorting_content.delete(1.0, tk.END)
            self.sorting_content.insert(tk.END, f"Generated array: {self.current_array}\n")
            self.stats_label.config(text="")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def sort_array(self):
        if not self.current_array:
            messagebox.showerror("Error", "Please generate numbers first")
            return

        array = self.current_array.copy()
        self.sorting_content.delete(1.0, tk.END)

        def update_progress(arr, pass_num, comparisons, swaps):
            self.sorting_content.insert(tk.END, f"Pass {pass_num}: {arr}\n")
            self.stats_label.config(text=f"Comparisons: {comparisons}, Swaps: {swaps}")
            self.update()
            time.sleep(0.5)

        start_time = time.time()
        if self.sort_algorithm.get() == "bubble":
            sorted_arr, comparisons, swaps = SortingAlgorithms.bubble_sort(array, update_progress)
        else:
            sorted_arr, comparisons, swaps = SortingAlgorithms.selection_sort(array, update_progress)
        end_time = time.time()

        self.sorting_content.insert(tk.END, f"\nFinal sorted array: {sorted_arr}\n")
        self.sorting_content.insert(tk.END, f"\nTime taken: {(end_time - start_time):.3f} seconds\n")
        self.stats_label.config(text=f"Final Stats - Comparisons: {comparisons}, Swaps: {swaps}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
