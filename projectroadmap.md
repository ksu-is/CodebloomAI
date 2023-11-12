# CodebloomAI Project Roadmap

## Sprint Week 1
### Tasks
- [x] Create project repository
- [x] Create documentation
- [x] Use and Evaluate CustomTkinter example
- [x] Use and Evaluate PaLM2 in python
- [x] Create python file using CustomTkinter example
- [x] Embed PaLM into custom python file
- [x] Create Home Page with 
    - [x] code input
    - [x] command input
    - [x] ai generated code output 

### Findings
- CustomTkinter repository has several pre-made templates that make understanding CustomTkinter modules easy.
    - `image_example.py` proved to be a great outline for `codebloomai.py`.
- CustomTkinter library works similarly to Tkinter, and has easy to follow modulation.
- PaLM is easy to embed into python
    - AI will respond well even with a basic rough context set
    - Investigating further for optimal results

### Known Bugs
- Bug 0
    ```python
    "File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.1776.0_x64__qbz5n2kfra8p0\Lib\tkinter\__init__.py", line 3808, in insert
        self.tk.call((self._w, 'insert', index, chars) + args)
        _tkinter.TclError: wrong # args: should be ".!ctkframe2.!ctktextbox2.!text insert index chars ?tagList chars tagList ...?"
    ```
    - Seems to occurs with certain code input and command combinations. 
        - Maybe length is contributing factor? Number of entries?
    - Seems to repeat error until an empty command and code input is performed.

## Sprint Week 2 
### Tasks
- [ ] Fix bugs
    - [ ] Bug 0
- [ ] Improve Home page
    - [ ] Align text correctly
    - [ ] Make pressing 'Enter' on keyboard a trigger to run command (instead of having to press button)
    - [ ] Make text boxes display prettier text with colors and not just raw text
    - [ ] Allow user to paste output into edit box
- [ ] Create History page
    - [ ] View and clear history
- [ ] Create Tweak page
    - [ ] Allow user to write further context to custom tailor their AI assistant

### Findings

## Sprint Week 3
### Tasks
- [ ] Fix bugs
- [ ] Advanced Main features
    - [ ] Allow ability to run code directly from app
    - [ ] Add keyboard shortcuts
- [ ] Advanced History features
- [ ] Advanced Tweak features
- [ ] More settings
- [ ] Run and find more bugs

### Findings