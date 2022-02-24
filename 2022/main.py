#!/usr/local/bin/python3

from data import Guy, Project
import sys
import copy

def mentorship_score(guy, skills_to_mentor, required):
    score = 0
    for skill in skills_to_mentor:
        if skill in guy.skills and guy.skills[skill] >= skills_to_mentor[skill]:
            score += 1
    return score + ( -2 if guy.skills[required['skill']] > required['level'] else 0 )

if len(sys.argv) <= 1:
    print("Manca il nome del file")
    exit(1)

fileName = sys.argv[1]

print(f"--- START FILE {fileName} ---")

inputFileName = f"in/{fileName}.in"
outputFileName = f"{fileName}.out"

inFile = open(inputFileName, 'r')
outFile = open(outputFileName, 'w+')

N, M = [int(x) for x in inFile.readline().split()]

guys = {}
skills = {}

for i in range(N):
    name, L = inFile.readline().split()

    guy = Guy(name)
    guys[name] = guy

    for j in range(int(L)):
        skill, level = inFile.readline().split()
        level = int(level)
        guy.add_skill(skill,level)

        if not skill in skills:
            skills[skill] = {}
        if not level in skills[skill]:
            skills[skill][level] = []
        skills[skill][level].append(guy.name)

projects = {}
max_t = 0
for i in range(M):
    name, days, score, before, R = inFile.readline().split()
    max_t = max(max_t, int(before) + int(score))
    proj = Project(name, int(days), int(score), int(before))
    projects[name] = proj
    for j in range(int(R)):
        skill, level = inFile.readline().split()
        proj.add_role(skill, int(level))

t = 0

in_use_guys = set()
selected_projects = []
in_use_projects = set()

original_projects = copy.deepcopy(projects)

while True:
    for selected in selected_projects:
        if t == selected['free_at']:
        
            project = original_projects[selected['proj']]

            for i, guy in enumerate(selected['assigned']):
                in_use_guys.remove(guy)

                required = project.required[i]
                if guys[guy].skills[required['skill']] <= required['level']:

                    skills_for_required =  skills[required['skill']]
                    guy_skill_level = guys[guy].skills[required['skill']]

                    skills_for_required[guy_skill_level].remove(guy)

                    guys[guy].improve_skill(required['skill'])
                    guy_skill_level += 1
                    if guy_skill_level not in skills[required['skill']]:
                        skills_for_required[guy_skill_level] = []
                    skills_for_required[guy_skill_level].append(guy)

            in_use_projects.remove(selected['proj'])
            

    keys = list(projects.keys())
    sorted(keys, key= lambda x: projects[x].score_at_t(t), reverse=True)
    
    for pName in keys:
        p = projects[pName]
        # print(t, p.name, p.score_at_t(t))
        if p.score_at_t(t) < 0:
            del projects[p.name]
            break
        assigned = []

        skills_to_mentor = {}
        for required in p.required:
            skills_to_mentor[required['skill']] = required['level']
        
        for required in p.required:
            required_level = required['level']

            selected_guy = None

            skill_levels = skills[required['skill']].keys()
            skilled_guys = []
            for skill_level in range(required_level, max(skill_levels)+1):
                for skilled_guy in skills[required['skill']].get(skill_level, []):
                    if not skilled_guy in in_use_guys:
                        skilled_guys.append(skilled_guy)

            sorted(skilled_guys, key = lambda x: mentorship_score(guys[x], skills_to_mentor, required), reverse=True)

            if len(skilled_guys) > 0:
                selected_guy = guys[skilled_guys[0]]

                for mentored_required in p.required:
                    if mentored_required == required:
                        continue
                    if not mentored_required['skill'] in skills_to_mentor:
                        continue

                    if mentored_required['skill'] in selected_guy.skills and selected_guy.skills[mentored_required['skill']] >= mentored_required['level']:
                        del skills_to_mentor[mentored_required['skill']]
                        mentored_required['level'] = mentored_required['level'] - 1
                
                assigned.append(selected_guy.name)
                in_use_guys.add(selected_guy.name)
            else:
                break

        if len(assigned) < len(p.required):
            in_use_guys =  in_use_guys - set(assigned)
            projects[p.name] = copy.deepcopy(original_projects[p.name])
        else:
            in_use_projects.add(p.name)
            selected_projects.append({
                'proj': p.name,
                'assigned': assigned,
                'free_at': t + p.days,
                'score': p.score + min(0, p.before - (t + p.days)  )
            })
            p.selected = True
            del projects[p.name]

    if len(in_use_projects) == 0:
        break
    
    target = min([s['free_at'] for s in selected_projects if s['free_at'] > t])
    t = target
    print(f'\r{100*t/max_t:.2}%       ', end='')

score = 0
outFile.write(f"{len(selected_projects)}\n")
for selected in selected_projects:
    score += selected['score']
    outFile.write(f"{selected['proj']}\n")
    outFile.write(f"{' '.join(selected['assigned'])}\n")

print(score)



