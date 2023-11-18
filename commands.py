import os
import logging

class Command:
    def execute(self, **kwargs):
        raise NotImplementedError

class GrepCommand(Command):
    def execute(self, filename, directory):
        logging.info(f"Executing Grep command: Searching for {filename} in {directory}")
        for root, dirs, files in os.walk(directory):
            if filename in files:
                result = True
                break
        else:
            result = False
        logging.info(f"Grep command result: {'Pass' if result else 'Fail'}")

class MvLastCommand(Command):
    def execute(self, src_directory, des_directory):
        logging.info(f"Executing MvLast command: Moving the most recent file from {src_directory} to {des_directory}")
        files = [f for f in os.listdir(src_directory) if os.path.isfile(os.path.join(src_directory, f))]
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(src_directory, x)))
            src_path = os.path.join(src_directory, latest_file)
            des_path = os.path.join(des_directory, latest_file)
            os.rename(src_path, des_path)
            logging.info(f"MvLast command result: Pass")
        else:
            logging.info("MvLast command result: Fail - No files to move")

class CategorizeCommand(Command):
    def execute(self, directory, threshold_size):
        logging.info(f"Executing Categorize command: Splitting files in {directory} based on size")

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        inner_dir_small = os.path.join(directory, "small_files")
        inner_dir_large = os.path.join(directory, "large_files")

        os.makedirs(inner_dir_small, exist_ok=True)
        os.makedirs(inner_dir_large, exist_ok=True)

        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.getsize(file_path) < int(threshold_size[:-2]) * 1024:  # Assuming threshold_size is in KB
                os.rename(file_path, os.path.join(inner_dir_small, file))
            else:
                os.rename(file_path, os.path.join(inner_dir_large, file))

        logging.info("Categorize command result: Pass")

class CommandFactory:
    @staticmethod
    def create_command(command_type):
        if command_type == 'Grep':
            return GrepCommand()
        elif command_type == 'MvLast':
            return MvLastCommand()
        elif command_type == 'Categorize':
            return CategorizeCommand()
        else:
            raise ValueError(f"Unknown command type: {command_type}")