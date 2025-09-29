import pathlib as pt

class CLI:
    def __init__(self):
        self.running = True
        self.current_directory = pt.Path('C:/Users/user/Desktop/conf_ypr')
        self.virtual_cwd = "myvfs$"
        self.commands = {
            'exit': self.com_exit,
            'help': self.com_help,
            'pwd': self.com_pwd,
            'ls': self.com_ls,
            'cd': self.com_cd,
            'echo': self.com_echo,
            'clear': self.com_clear
        }

    def greetings(self):
        print("Hi! This is my Shell Emulator")
        print("Type 'help' for available commands")
        print("Type 'exit' to quit\n")

    def com_help(self):
        print("Available commands:")
        print("  exit      - terminate shell")
        print("  help      - show this help")
        print("  pwd       - show current directory")
        print("  ls [dir]  - list directory contents")
        print("  cd [dir]  - change directory")
        print("  echo [text] - print text")
        print("  clear     - clear screen")

    def com_cd(self, target):
        if target == "..":
            if self.current_directory != self.current_directory.parent:
                self.current_directory = self.current_directory.parent
            return self.current_directory

        new_path = self.current_directory / target
        resolved_path = new_path.resolve()

        if not resolved_path.exists():
            print(f"No such directory: {target}")

        self.current_directory = resolved_path
        return self.current_directory

    def com_ls(self, args):
        if args:
            target_dir = self.current_directory / args[0]
        else:
            target_dir = self.current_directory

        if not target_dir.exists():
            print(f"No such directory: {args}")
        target_dir = target_dir.resolve()

        for item in target_dir.iterdir():
            print(item.name)



    def com_pwd(self, args):
        print("pwd", args)
        return

    def com_clear(self, args):
        print("clear", args)
        return

    def com_echo(self, args):
        print(*args)
        return

    def com_exit(self):
        self.running = False
        return 0

    def display(self):
        return f"{self.virtual_cwd}::{self.current_directory.name}> "

    def main(self):
        while self.running:
            print(self.display(), end="")
            user_input = input().strip()

            if not user_input:
                continue

            com_args = user_input.split()
            cmd = com_args[0]
            args = com_args[1:]

            if cmd not in self.commands:
                print("Unknown command")
                continue

            if cmd == "exit":
                self.commands[cmd]()
            else:
                self.commands[cmd](args)


c = CLI()
c.greetings()
c.main()
