
class Word:
    def __init__(self):
        pass

    def get_content_file(self, file):
        content = ""
        with open(file, "r") as f:
            c = f.readlines()
        if c != "":
            content = c
        return content
    
    def get_all_words(self, file, sep=" "):
        content = self.get_content_file(file)
        content = "".join(content)
        content = content.split("\n")
        content = "".join(content)
        content = content.split("\r")
        content = "".join(content).lower()
        self.all_words = content.split(sep)
        return self.all_words
    
