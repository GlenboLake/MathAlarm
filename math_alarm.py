import random
import threading
import tkinter


class Application(tkinter.Frame):
    ARG_COUNT = 3

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.pack(padx=10, pady=10, fill=tkinter.BOTH)

        self.problems_remaining = 3
        self.remaining_text = tkinter.StringVar()
        self.remaining_text.set('Problems left: {}'.format(self.problems_remaining))
        self.equation = tkinter.StringVar()
        self.solution = None
        self.new_problem()
        # Create widgets
        # Problem countdown label
        self.counter = tkinter.Label(self, textvariable=self.remaining_text)
        self.counter.pack()
        # Text box for math problems
        self.problem = tkinter.Label(self, textvariable=self.equation, font=('Helvetica', 20))
        self.problem.pack(padx=20, pady=20, fill=tkinter.BOTH)
        # Frame containing answer box and submit button
        self.submission = tkinter.Frame(self)
        self.submission.pack()
        # User's submission area
        self.user_answer = tkinter.Entry(self.submission)
        self.user_answer.bind('<Return>', self.ret)
        self.user_answer.pack(side='left')
        # Submit button
        self.submit = tkinter.Button(self.submission)
        self.submit["text"] = "Submit"
        self.submit["command"] = self.check_answer
        self.submit.pack(side='left')
        # Text entry field should start with focus
        self.user_answer.focus()

    def new_problem(self):
        equation = ''
        while True:
            numbers = [str(random.randint(2, 9)) for _ in range(self.ARG_COUNT)]
            ops = [random.choice('+-*/') for _ in range(self.ARG_COUNT - 1)]
            equation = [''] * (2 * self.ARG_COUNT - 1)
            equation[::2] = numbers
            equation[1::2] = ops
            equation = ' '.join(equation)
            print('Generated {}'.format(eval(equation)))
            try:
                int(str(eval(equation)))
            except ValueError:
                pass
            else:
                break
        self.equation.set(equation)
        self.solution = str(eval(equation))

    def ret(self, _):
        self.check_answer()

    def check_answer(self):
        print('In thread {}'.format(threading.get_ident()))
        correct = self.user_answer.get() == self.solution
        print(correct)
        if correct:
            self.problems_remaining -= 1
            if self.problems_remaining == 0:
                self.master.destroy()
            else:
                self.new_problem()
                self.user_answer.delete(0, tkinter.END)


def prevent_close():
    pass

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Do math')
    root.minsize(400, 300)
    root.protocol("WM_DELETE_WINDOW", prevent_close)
    app = Application(root)
    app.mainloop()
