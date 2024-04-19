import glob
import os
import shutil

from cc_resume import utils
from cc_resume import CURRENT_DIR


class Cmd:

    def __init__(self):
        self.config_dir = utils.mkdir_config('resume')
        self.config_resumes_dir = os.path.join(self.config_dir, 'resumes')
        self.config_output_dir = os.path.join(self.config_dir, 'output')
        print(f"self.config_dir={self.config_dir}")
        
        self.data_resumes = os.listdir(self.config_resumes_dir)
        self.config_file_path = os.path.join(self.config_dir, 'resume.conf')
        self.output_dir = os.path.join(self.config_dir, 'output')
        self.depend()

    def depend(self):
        project_resumes_dir = os.path.join(CURRENT_DIR, 'resumes')
        shutil.copytree(project_resumes_dir, self.config_resumes_dir, dirs_exist_ok=True)
        utils.crudini_set_config(
            self.config_file_path, 'resume', 'config_dir', self.config_dir, check_file_exist=False)
        os.makedirs(self.config_resumes_dir, exist_ok=True)
        os.makedirs(self.config_output_dir, exist_ok=True)

    def prompts(self):
        print('choose one:')
        for i, name in enumerate(self.data_resumes):
            print(f'{i+1}: {name}')
        print(f'q: exit')

    def run(self):
        length = len(self.data_resumes)
        while True:
            self.prompts()
            number = input(f'please input number[1-{length}]:')
            if not number:
                continue
            if number.lower() == 'q':
                break
            if number.isdigit() and int(number) in range(1, length+1):
                yaml_name = self.data_resumes[int(number) - 1]
                print(f'now generate pdf for {yaml_name}')
                utils.crudini_set_config(self.config_file_path, 'resume', 'name', yaml_name)
                print(f'now run "cc-resume-generate-pdf"')
                from cc_resume import main
                main.main()
                break
            else:
                print(f'error input! input must be in [0-{length - 1}]!')
                continue


def main():
    Cmd().run()
