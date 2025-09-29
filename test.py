def com_cd(self, target):
    new_path = self.current_directory / target
    self.current_directory = new_path.resolve()

    if not self.current_directory.exists():
        return f"No such directory: {target}"

    return self.current_directory