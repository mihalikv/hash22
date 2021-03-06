import os
from collections import Counter, OrderedDict, defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = [
    # 'a_an_example.in',
     'b_better_start_small.in',
    # 'c_collaboration.in',
    # 'd_dense_schedule.in',
    # 'e_exceptional_skills.in',
    # 'f_find_great_mentors.in',
]
input_files = [os.path.join(dir_path, 'input', '{}.txt'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def sign(value):
    return value if value > 0 else 0


def weight(day, deadline, score, duration):
    return score - sign(deadline - (day+duration))


def get_scores_at_day(day, projects):
    projects_ord = []
    for project_name, project in projects.items():
        score = weight(
            day,
            deadline=project['deadline'],
            score=project['score'],
            duration=project['num_days']
        )
        projects_ord.append((project_name, score))
    return list(filter(lambda x: x[1] > 0, sorted(projects_ord, key=lambda p: p[1], reverse=True)))


def process(input_file_path, output_file_path):
    with open(input_file_path) as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        num_contrib, num_projects = map(int, lines[0].split(' '))
        contributors = defaultdict(lambda: defaultdict(dict))
        contributors_by_skill = defaultdict(list)
        projects = {}
        line_index = 0
        for i in range(num_contrib):
            line_index += 1
            name, num_skills = lines[line_index].split(' ')
            for j in range(int(num_skills)):
                line_index += 1
                skill, skill_level = lines[line_index].split(' ')
                contributors[name]['skills'][skill] = int(skill_level)
                contributors[name]['delay'] = 0
                contributors_by_skill[skill].append((name, skill_level))
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
        for name in contributors_by_skill.keys():
            contributors_by_skill[name] = list(map(lambda item: item[0], sorted(contributors_by_skill[name], key=lambda x: x[1], reverse=False))) # od najvacsieho
        # print(dict(contributors))
        # print(dict(projects))
    success_projects = {}

    is_possible_continue = True
    day_number = 0

    while is_possible_continue:
        ids_to_delete = []

        projects_of_the_day = get_scores_at_day(day_number, projects)
        can_all_do_it = True
        for name, contributor_data in contributors.items():
            is_available = day_number > contributor_data['delay']
            if not is_available:
                can_all_do_it = False
        print(day_number)
        # print(len(projects_of_the_day))
        for project_of_the_day in projects_of_the_day:
            project_name, score = project_of_the_day
            project = projects[project_name]
            project_contributors = []
            upgrade_skill_to_contributor = {}
            project_skills = defaultdict(list)
            for skill_name, skill_level in project['skills_needed']:
                skill_was_assigned = False
                for name in contributors_by_skill[skill_name]:
                    # for name, contributor_data in contributors.items():
                    contributor_data = contributors[name]
                    is_available = day_number > contributor_data['delay']
                    if not is_available:
                        continue
                    skills = contributor_data['skills']
                    has_skill = skill_name in skills and skills[skill_name] >= skill_level
                    mentor = None
                    for skill_level_mentor, mentor_name in project_skills[skill_name]:
                        if skill_level <= skill_level_mentor:
                            mentor = mentor_name
                    has_mentor = (skill_name in skills and skills[skill_name] == (skill_level - 1)) and bool(mentor)
                    not_in_project = name not in project_contributors
                    if (has_skill or has_mentor) and not_in_project and is_available:
                        # is good for job
                        skill_was_assigned = True
                        project_contributors.append(name)
                        for mentor_skill, mentor_skill_level in skills.items():
                            project_skills[mentor_skill].append((mentor_skill_level, name))
                        if has_mentor and mentor in upgrade_skill_to_contributor:
                            del upgrade_skill_to_contributor[mentor]
                        if (skills[skill_name] == skill_level or skills[skill_name] + 1 == skill_level) and skills[skill_name] < 10:
                            upgrade_skill_to_contributor[name] = skill_name
                        break
                if not skill_was_assigned:
                    break
            if len(project_contributors) == len(project['skills_needed']):
                success_projects[project_name] = project_contributors
                for contributor_name in project_contributors:
                    contributors[contributor_name]['delay'] += project['num_days']
                for contributor_name, skill_name in upgrade_skill_to_contributor.items():
                    contributors[contributor_name]['skills'][skill_name] += 1
                ids_to_delete.append(project_name)

        if len(ids_to_delete) == 0 and can_all_do_it:
            print(f'Tu sme boli {can_all_do_it}')
            is_possible_continue = False

        if len(projects_of_the_day) == 0:
            print(f'Tu sme boli2 {projects_of_the_day}')
            is_possible_continue = False

        if len(ids_to_delete) == 0:
            delays = [item['delay'] for item in contributors.values() if item['delay'] >= day_number]
            # print(f'delays {delays}')
            if not delays:
                is_possible_continue = False
            else:
                min_delay = min(delays)
                day_number = max(min_delay, day_number + 1)
        else:
            print(f'ids_to_delete {ids_to_delete}')
            day_number += 1

        for id_to_delete in ids_to_delete:
            del projects[id_to_delete]


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
