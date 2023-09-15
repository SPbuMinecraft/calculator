import csv


class CSVWorker:
    def __init__(self, file_name: str, buffer_size: int = 1, clear_file: bool = True):
        if clear_file:
            with open(file_name, mode="w", encoding="utf-8") as w_file:
                pass
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.lines: list[list[str]] = []

    def add_line(self, line: list[str]):
        self.lines.append(line)
        if len(self.lines) == self.buffer_size:
            self.update_file()
            self.lines = []
    
    def add_first_line(self, line: list[str]):
        self.lines.append(line)
        if len(self.lines) == self.buffer_size:
            self.update_file()
            self.lines = []

    def update_file(self):
        with open(self.file_name, mode="a", encoding="utf-8") as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r\n")
            for line in self.lines:
                file_writer.writerow(line)
    
    def get_lines(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            return [elem.split(",") for elem in lines[1:]]
                