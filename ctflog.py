# Simple CTF challenge journal.
## TODO: add total time used function for export. Improve formatting. Search function? Tagging inputs?
# Remove s command and only use m?


import os
from datetime import datetime

# Change this to where you want to save the .md file
SAVE_DIR = "/home/steffen/Documents/CTFlogs"


#  -ANSI colors-
R       = "\033[0m"  #Resets color
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
BOLD    = "\033[1m"

#helper function for wrapping text in ansi color
def color(text, code):
    return f"{code}{text}{R}"

# Predefined color functions
def red(text): return color(text, RED)
def green(text): return color(text, GREEN)
def yellow(text): return color(text, YELLOW)
def blue(text): return color(text, BLUE)
def magenta(text): return color(text, MAGENTA)
def cyan(text): return color(text, CYAN)
def white(text): return color(text, WHITE)
def bold(text): return color(text, BOLD)


# Defines startup inputs. ".strip" to remove whitespaces
challenge = input("Challenge name: ").strip()
diff = input("Difficulty: ").strip()
timeestimate = input("Challenge time estimate: ")
target = input("target IP: ")           

# Replaces spaces with "_" for safe file naming
filename = challenge.replace(" ", "_") + ".md"

# Stores steps and flags in lists as plain text
steps = []  
flags = []  


def now():
    return datetime.now().strftime("%d/%m/%y %H:%M")

# Multiline step function for pasting/ making long entries
def add_multiline():
    print("Paste text (e.g., nmap results). End with a line containing only: end")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "end":
                break
            lines.append(line)
        except EOFError:
            break
    if lines:
        steps.append(f"[{now()}]\n" + "\n".join(lines))
        print(f"[added {len(lines)} lines]")


print("\nCommands:")
print("  s  -> add a step")
print("  m  -> add/paste multi-line block step (nmap, gobuster, etc.)")
print("  f  -> add a flag")
print("  p  -> print current summary")
print("  x  -> export .md file and quit\n")


#          ---Main command loop---
while True:
    try:  #Accidental ctrl + c measure
        cmd = input("> ").strip().lower()
    except KeyboardInterrupt:
        print("\nctrl + c detected. Exit? y/n")
        choice = input("> ").strip().lower()
        if choice == "y":
            break        # exit loop and close program
        else:
            continue     # Continue loop, in this case "n"
    if cmd == "s":
        txt = input("Step (short text): ").strip()
        if txt:
            steps.append(f"[{now()}] {txt}")
            print("[added]")
    elif cmd == "m":
        add_multiline()
    elif cmd == "f":
        txt = input("Flag: ").strip()
        if txt:
            flags.append(f"[{now()}] {txt}")
            print("[added]")
    elif cmd == "p":
        print("\n=========================== SUMMARY ===========================")
        print(f"Challenge name: {challenge}")
        if diff:
            print(f"Difficulty: {diff}")
        if timeestimate:
            print(f"Time estimate: {timeestimate}")
        if target:
            print(f"Target: {red(target)}")
        print(f"\n{GREEN}Steps:{R}")
        if steps:
            for i, s in enumerate(steps, 1):
                print(f"{GREEN}  {i}{R}. {s}\n---------------------------------------------------------------")
            print("===============================================================")
        else:      
            print("  (none)")
        print(f"\n{BLUE}Flags:{R}")
        if flags:
            for f in flags:
                print(f"  - {f}")
        else:
            print("  (none)")
        print("===============================================================\n")
    elif cmd == "x":
        lines = []
        lines.append(f"# {challenge}\n")
        if diff:
            lines.append(f"- **Difficulty:** {diff}\n")
        lines.append(f"- **Time Estimate:** {timeestimate}\n")
        lines.append(f"- **Target IP:** {target}\n")
        lines.append(f"- **Exported:** {now()}\n")
        lines.append("\n## Steps\n")
        if steps:
            for i, s in enumerate(steps, 1):
                lines.append(f"{i}. {s}\n")
        else:
            lines.append("- (none)\n")
        lines.append("\n## Flags\n")
        if flags:
            for f in flags:
                lines.append(f"- {f}\n")
        else:
            lines.append("- (none)\n")

        ## Save function. Checks if directory exists
        save_path = os.path.join(SAVE_DIR, filename)
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as fp:
            fp.write("".join(lines))
        print(f"Exported to {save_path}")
        break

    else:
        print("Commands: s (step), f (flag), p (print), x (export & quit)")
