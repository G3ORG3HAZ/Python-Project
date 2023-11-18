import argparse
import json
import logging

from commands import CommandFactory
import sys

def read_config(file_path):
    with open(file_path, 'r') as f:
        config_data = json.load(f)
    return config_data

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(description="Command Automation george is a command line tool to automate commands")
    parser.add_argument("-s", "--script", help="Path to script file", required=True)
    parser.add_argument("-o", "--output", help="Path to output log file", required=True)
    args = parser.parse_args()

    script_path = args.script
    output_path = args.output
    config_path = "C:\\Users\\G3ORG3HAZ\\Desktop\\python_proj\\config.json"

    # Read configuration
    config = read_config(config_path)

    # Setup logging
    setup_logging(output_path)

    # Initialize command factory
    command_factory = CommandFactory()

    with open(script_path, 'r') as script_file:
        num_lines = sum(1 for line in script_file)
        if(num_lines > int(config['Max_commands'])):
            logging.info("Too many commands in script file")
            return

    # Read and execute commands from the script
    with open(script_path, 'r') as script_file:
        for line in script_file:
            parts = line.strip().split()
            command_type = parts[0]
            command_args = parts[1:]

            command = command_factory.create_command(command_type)
            if(command_type == "Categorize"):
                command.execute(directory=command_args[0], threshold_size=config['threshold_size'])
            elif(command_type == "Grep"):
                command.execute(filename=command_args[0], directory=command_args[1])
            else:
                command.execute(src_directory=command_args[0], des_directory=command_args[1])

if __name__ == "__main__":
    main()
