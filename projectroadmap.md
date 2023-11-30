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
    ```
        _tkinter.TclError: wrong # args: should be ".!ctkframe2.!ctktextbox2.!text insert index chars ?tagList chars tagList ...?"
    ```
    - Seems to occurs with certain code input and command combinations. 
        - Maybe length is contributing factor? Number of entries?
    - Seems to repeat error until an empty command and code input is performed.

## Sprint Week 2 
### Tasks
- [ ] Fix bugs
    - [ ] Bug 0
- [x] Improve Home page
    - [x] Align text correctly
    - [ ] Make pressing 'Enter' on keyboard a trigger to run command (instead of having to press button)
    - [ ] Make text boxes display prettier text with colors and not just raw text
    - [x] Create overhead toolbar 
    - [x] Allow user to paste output into edit box
        - [x] Strip the default formatting that ai surrounds the code with when swapping over to input box
    - [x] Allow user to save input as a file
    - [x] Allow user to open text/code file into input space
    - [x] **Allow user to execute code directly from the app**
- [x] Create History page
    - [x] View and clear history
- [ ] Create Tweak page
    - [ ] Allow user to write further context to custom tailor their AI assistant

### Findings
- Creating keyboard functionality proved to be more difficult than expected
- Allowing code to be represented with the proper color-coding may be near-impossible with Tkinter alone
    - Will investigate other library options for this feature
- Executing code within the app using exec() function was challenging 
    - exec() function was problematic without correct local and global variable definitions
- Opening and saving textbox as a file was easier than expected
- The internal GUI layout is crucial to the ease of modification
    - A well laid foundation allows for much faster progress
    - Was able to make small changes swiftly allowing me to focus on larger features and problems
- History functionality may be improved using a method other than simply appending to text file 

## Sprint Week 3
### Tasks
- [x] Fix bugs
- [ ] Advanced Main features
    - [ ] Add keyboard shortcuts
    - [ ] Add ability to have multiple files open at once in sepreate taps
- [ ] Advanced History features
- [ ] Add Tweak features
- [ ] More settings
- [ ] Run and find more bugs

### Findings
- 11/27/23 | Bug 0 was the result of AI generation `ai_result` coming back empty, and insert function to output textbox `self.out_textbox.insert()` was returning error when no result could be retrieved.
    - Fixed temporarily by replacing `ai_result` with `f"{ai_result}` so a missing ai generation would come back as `none` and not empty
    - Looking into why ai generation is coming back empty. *May have to do with input size?*