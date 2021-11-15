from tkinter import *
import math

# --------------------------- CONSTANTS ---------------------------

# Hexcodes for colors
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

# Name of font to be used throughout program
FONT_NAME = "Courier"

# Length of times for timer
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# --------------------------- GLOBAL VARIABLES  ---------------------------

# Number of times the timer has reached 0
reps = 0

# Name of window.after timer (to be used later)
my_timer = None


# --------------------------- TIMER RESET ---------------------------
def timer_reset():
    global reps
    global my_timer

    # Reset number of reps
    reps = 0

    # Stop my_timer from running
    window.after_cancel(my_timer)

    # Reset the timer_text to display empty clock 00:00
    canvas.itemconfig(timer_text, text="00:00")

    # Reset title_label to display the title of program, Timer
    title_label.config(font=(FONT_NAME, 55, "bold"), text="Timer", bg=YELLOW, fg=GREEN)

    # Re-enable clicking start button
    start_button.config(state=NORMAL)


# --------------------------- TIMER MECHANISM ---------------------------
def timer_start():
    global reps

    # Increase number of reps, as the clock has reset
    reps += 1

    # Disable start button so we can't click on it multiple times
    start_button.config(state=DISABLED)

    # Convert seconds to minutes
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # If 8 reps complete (4 work sessions), we have a long break
    if reps % 8 == 0:
        countdown(long_break_sec)
        title_label.config(text="Break", fg=RED)

    # If 2 additional reps complete (1 additional work session) then we have a short break
    elif reps % 2 == 0:
        countdown(short_break_sec)
        title_label.config(text="Break", fg=PINK)

    # Else work time
    else:
        countdown(work_sec)
        title_label.config(text="Work")


# --------------------------- COUNTDOWN MECHANISM ---------------------------
# Count = total number of seconds in the timer
def countdown(count):
    global my_timer

    # Convert seconds to number of minutes to be displayed
    minutes = math.floor(count / 60)

    # Convert total number of seconds to seconds to be displayed
    seconds = count % 60

    # If less than 10 seconds left, add a 0 before on the display; else display number of min and number of seconds
    if seconds < 10:
        canvas.itemconfig(timer_text, text=f"{minutes}:0{seconds}")
    else:
        canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")

    # If the count is above zero, continue timer and reduce count by 1
    if count > 0:
        my_timer = window.after(1000, countdown, count - 1)

    # If count == 0
    else:
        # Bring window to the front of screen, sound bell
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
        window.bell()

        # Start the timer again with the new reps value
        timer_start()

        # Check marks will display for each work session completed
        marks = ""

        # Total number of work sessions = reps / 2
        work_sessions = math.floor(reps / 2)

        # For each work session display a check mark
        for i in range(0, work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# --------------------------- UI SETUP ---------------------------
window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50, bg=YELLOW)
window.minsize(500, 300)

title_label = Label(font=(FONT_NAME, 55, "bold"), text="Timer", bg=YELLOW, fg=GREEN)
title_label.grid(column=1, row=0)

tomato_img = PhotoImage(file="tomato.png")
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(101, 130, text="00:00", font=(FONT_NAME, 30, "bold"), fill="white")
canvas.grid(column=1, row=1, pady=25)

start_button = Button(text="Start", command=timer_start)
start_button.grid(column=0, row=3)
reset_button = Button(text="Reset", command=timer_reset)
reset_button.grid(column=3, row=3)

check_marks = Label(font=(FONT_NAME, 10), bg=YELLOW, fg=GREEN)
check_marks.grid(column=1, row=3)

window.columnconfigure(0, weight=1)  # column on left
window.columnconfigure(2, weight=1)  # column on right
window.rowconfigure(0, weight=1)     # row above
window.rowconfigure(2, weight=1)     # row below

window.mainloop()
