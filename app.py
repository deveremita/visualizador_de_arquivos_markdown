import webbrowser
import tkinter as tk
from tkinter import filedialog

class MarkdownViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Markdown")
        
        self.text_widget = tk.Text(root, wrap="word", font=("Helvetica", 12))
        self.text_widget.pack(expand=True, fill="both")
        
        self.text_widget.tag_configure("header1", font=("Helvetica", 20, "bold"))
        self.text_widget.tag_configure("header2", font=("Helvetica", 18, "bold"))
        self.text_widget.tag_configure("header3", font=("Helvetica",16, "bold"))
        
        
        
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Fechar", command=root.destroy)
    def open_link(self, url):
        webbrowser.open(url)  
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown Files","*.md")]) 
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.display_markdown(content)
            
    def display_markdown(self, markdown_content):
        # Limpar o widget Text
        self.text_widget.delete("1.0", tk.END)
        # Processar o conteúdo Markdown e aplicar estilos diretamente ao Text
        self.apply_styles(markdown_content)
        
    
    def apply_styles(self, markdown_content):
        current_position = "1.0"
        in_list = False #Flag para controlar se estamos dentro de uma lista não ordenada
        in_ordered_list = False #Flag para controlar se estamos dentro de uma lista ordenada
        link_counter = 0

        for line in markdown_content.splitlines():
            if line.startswith('#'):
                header_level = min(line.count('#'), 3)  # Limitar a 2 para evitar tamanhos muito grandes
                tag_name = f"header{header_level}"
                self.text_widget.insert(current_position, line.strip('#'), tag_name)
            elif line.startswith('* '):
                # Tratar como uma lista não ordenada
                if not in_list:
                    tag_name = "list_bullet"
                    in_list = True
                self.text_widget.insert(current_position,"• "+line.lstrip('* ').lstrip(), tag_name)
            elif any(line.lstrip().startswith(f"{i}. ") for i in range(1, 1000)):
                # Tratar como uma lista ordenada
                if not in_ordered_list:
                    tag_name = "list_number"
                    in_ordered_list = True
                self.text_widget.insert(current_position,f"{line.split('.', 1)[0]}. {line.split('.',1)[1].lstrip()}", tag_name)
            elif "[" in line and "]" in line and "(" in line and ")" in line:
                # Tratar como um link
                link_text = line[line.find("[")+1:line.find("]")]
                link_url = line[line.find("(")+1:line.find(")")]
                link_tag = f"link_{link_counter}"
                link_counter += 1
                self.text_widget.insert(current_position, link_text, link_tag)
                self.text_widget.tag_add(link_tag, current_position, f"{current_position}+{len(link_text)}c")
                self.text_widget.tag_config(link_tag, foreground="blue", underline=True)
                self.text_widget.tag_bind(link_tag, "<Button-1>", lambda event, url=link_url: self.open_link(url))
            else:
                self.text_widget.insert(current_position, line)
            
            current_position = self.text_widget.index(tk.END)
            self.text_widget.insert(current_position, "\n")  # Adicionar uma quebra de linha
            current_position = self.text_widget.index(tk.END)
            # Resetar as flags de lista e código
            if not line.lstrip().startswith('* '):
                in_list = False
            if not any(line.lstrip().startswith(f"{i}. ") for i in range(1, 1000)):
                in_ordered_list = False
            
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownViewerApp(root)
    root.geometry("800x600")
    root.mainloop()
    
