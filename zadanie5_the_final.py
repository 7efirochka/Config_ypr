import pathlib as pt
import shutil
import datetime
import time
import sys


class CLI:
    def __init__(self, vfs_path=None, script_path=None):
        self.running = True
        self.current_directory = pt.Path(vfs_path) if vfs_path else pt.Path('C:/Users/user/Desktop/conf_ypr')
        self.virtual_cwd = "myvfs$"
        self.script_path = script_path
        self.start_time = time.time()
        self.allow_files = []
        self.commands = {
            'exit': self.com_exit,
            'help': self.com_help,
            'pwd': self.com_pwd,
            'ls': self.com_ls,
            'cd': self.com_cd,
            'echo': self.com_echo,
            'clear': self.com_clear,
            'start': self.com_start,
            "vfs":self.com_vfs,
            "date": self.com_date,
            "uptime": self.com_uptime,
            'chmod': self.com_chmod
        }

    def greetings(self):
        print("Hi! This is my Shell Emulator")
        print(f"VFS path: {self.current_directory}")
        print(f"Script path: {self.script_path}")
        print("Type 'help' for available commands")
        print("Type 'exit' to quit\n")

    def show_startup_params(self):
        print("=== DEBUG: Startup Parameters ===")
        print(f"VFS Path: {self.current_directory}")
        print(f"Script Path: {self.script_path}")
        print("=================================\n")

    def com_help(self, args=None):  # NEW: добавим args для единообразия
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

    def com_clear(self, args):
        print("\n" * 100)

    def com_echo(self, args = None):
        print(*args)

    def com_date(self):
        today_date = datetime.date.today()
        print(today_date)

    def com_uptime(self):
        uptime_seconds = time.time() - self.start_time
        minutes = int(uptime_seconds // 60)
        sec = int(uptime_seconds)
        print(f"Shell uptime: {minutes:02d}:{sec:02d}")

    def com_start(self, args):
        filename = args[0]
        file_path = self.current_directory / filename

        if not file_path.exists():
            print(f"File not found: {filename}")

        if not filename in self.allow_files:
            print(f"Permission denied: {filename} is not ex ecutable")
            print("Use 'chmod +x {filename}' to make it executable")

        else:
            f = open(file_path, 'r')
            for i in f:
                command = i.strip()
                print(f"{self.display()}{command}")
                self.process_command(command)
            f.close

    def com_exit(self, args=None):
        self.running = False

    def com_vfs(self, args):
        fixed_path = pt.Path('C:/Users/user/Desktop/drygoe_konf')
        if args[0]== "load":


            if fixed_path.exists():
                self.current_directory = fixed_path

                pathh = fixed_path / 'motd.txt'
                f = open(pathh, 'r', encoding = "utf-8")
                for i in f:
                    print(i, end='')
                print('\n')
                f.close()

        elif args[0] == "init":
            if fixed_path.exists():
                self.current_directory = fixed_path

                for item in fixed_path.iterdir():
                    if item.name != "motd.txt":
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)

    def com_chmod(self, args):
        if not args or len(args) < 2:
            print("Usage: chmod <mode> <file>")
            return

        mode_str = args[0]
        filename = args[1]
        file_path = self.current_directory / filename
        if not file_path.exists():
            print(f"File not found: {filename}")
            return

        try:
            if mode_str.isdigit():
                self.allow_files.append(filename)
            else:

                if mode_str == "+x":
                    self.allow_files.append(filename)
                    print(f"Changed permissions of {filename} to {mode_str}")
                elif mode_str == "-x":
                    try:
                        self.allow_files.remove(filename)
                        print(f"Changed permissions of {filename} to {mode_str}")
                    except:
                        print(f"{filename} don't have this access")
                elif mode_str == "+r":
                    self.allow_files.append(filename)
                    print(f"Changed permissions of {filename} to {mode_str}")
                elif mode_str == "-r":
                    try:
                        self.allow_files.remove(filename)
                        print(f"Changed permissions of {filename} to {mode_str}")
                    except:
                        print(f"{filename} don't have this access")
                else:
                    print(f"Unknown mode: {mode_str}")
                    return

        except Exception as e:
            print(f"Error: {e}")

    def display(self):
        return f"{self.virtual_cwd}::{self.current_directory.name}> "



    def process_command(self, command):
        if not command.strip():
            return

        com_args = command.split()
        cmd = com_args[0]
        args = com_args[1:] if len(com_args) > 1 else []

        if cmd not in self.commands:
            print(f"ERROR: {cmd} is unknown command")
            return

        try:
            if cmd == "cd":
                if args:
                    self.com_cd(args[0])
                else:
                    print("Usage: cd <directory>")
            elif cmd == "help":
                self.com_help(args)
            elif cmd == "pwd":
                self.com_pwd(args)
            elif cmd == "ls":
                self.com_ls(args)
            elif cmd == "exit":
                self.com_exit(args)
            elif cmd == "echo":
                self.com_echo(args)
            elif cmd == "clear":
                self.com_clear(args)
            elif cmd == "date":
                self.com_date()
            elif cmd == "uptime":
                self.com_uptime()

        except Exception as e:
            print(f"Error executing command '{command}': {e}")

    def main(self):
        self.show_startup_params()
        self.greetings()


        while self.running:
            try:
                print(self.display(), end="")
                user_input = input().strip()

                if not user_input:
                    continue


                com_args = user_input.replace('-', ' ').split()
                cmd = com_args[0]
                if cmd == "chmod":
                    com_args = user_input.split()
                args = com_args[1:] if len(com_args) > 1 else []

                if cmd not in self.commands:
                    print(f"ERROR: {cmd} if unknown command")
                    return 0

                if cmd == "cd":

                    if args:
                        self.com_cd(args[0])
                    else:
                        print("Usage: cd <directory>")

                elif cmd == "start":
                    self.com_start(args)
                elif cmd == "help":
                    self.com_help(args)
                elif cmd == "pwd":
                    self.com_pwd(args)
                elif cmd == "ls":
                    self.com_ls(args)
                elif cmd == "exit":
                    self.com_exit(args)
                elif cmd == "echo":
                    self.com_echo(args)
                elif cmd == "clear":
                    self.com_clear(args)
                elif cmd == "vfs":
                    self.com_vfs(args)
                elif cmd == "date":
                    self.com_date()
                elif cmd == "uptime":
                    self.com_uptime()
                elif cmd == "chmod":
                    self.com_chmod(args)

            except KeyboardInterrupt:
                print("Use 'exit' to quit")
            except EOFError:
                print("Use 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")


def parse_arguments():
    vfs_path = None
    script_path = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ['--vfs-path', '-v']:
            if i + 1 < len(sys.argv):
                vfs_path = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: Missing value for {sys.argv[i]}")
                i += 1
        elif sys.argv[i] in ['--script', '-s']:
            if i + 1 < len(sys.argv):
                script_path = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: Missing value for {sys.argv[i]}")
                i += 1
        else:
            print(f"Warning: Unknown argument {sys.argv[i]}")
            i += 1

    return vfs_path, script_path


vfs_path, script_path = parse_arguments()
c = CLI(vfs_path, script_path)
c.main()
