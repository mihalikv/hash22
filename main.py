import os
from collections import Counter, OrderedDict, defaultdict
import numpy as np
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = [
    'a_an_example.in',
    'b_better_start_small.in',
    'c_collaboration.in',
    'd_dense_schedule.in',
    'e_exceptional_skills.in',
    'f_find_great_mentors.in',
]
input_files = [os.path.join(dir_path, 'input', '{}.txt'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def process(input_file_path, output_file_path):
    with open(input_file_path) as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        num_contrib, num_projects = map(int, lines[0].split(' '))
        contributors = defaultdict(dict)
        projects = {}
        line_index = 0
        for i in range(num_contrib):
            line_index += 1
            name, num_skills = lines[line_index].split(' ')
            for j in range(int(num_skills)):
                line_index += 1
                skill, skill_level = lines[line_index].split(' ')
                contributors[name][skill] = int(skill_level)
        for i in range(num_projects):
            line_index += 1
            name, num_days, score, deadline, num_roles = lines[line_index].split(' ')
            projects[name] = {
                'num_days': int(num_days),
                'score': int(score),
                'deadline': int(deadline),
                'num_roles': int(num_roles),
                'skills_needed': []
            }
            for j in range(int(num_roles)):
                line_index += 1
                skill, skill_level = lines[line_index].split(' ')
                projects[name]['skills_needed'].append((skill, int(skill_level)))
        # print(dict(contributors))
        # print(dict(projects))
    success_projects = {}
    for project_name, project in projects.items():
        project_contributors = []
        for skill_name, skill_level in project['skills_needed']:
            for name, skills in contributors.items():
                if skill_name in skills and skills[skill_name] >= skill_level and name not in project_contributors:
                    # is good for job
                    project_contributors.append(name)
                    break
        if len(project_contributors) == len(project['skills_needed']):
            success_projects[project_name] = project_contributors

    output_lines = []
    output_lines.append(f'{len(success_projects)}\n')
    for success_project, contributors in success_projects.items():
        output_lines.append(f'{success_project}\n')
        output_lines.append(f'{" ".join(contributors)}\n')

    output_file = open(output_file_path, 'w')
    output_file.writelines(output_lines)
    output_file.close()


def main():
    for index, input_file_path in enumerate(input_files):
        process(input_file_path, output_files[index])


if __name__ == "__main__":
    main()
