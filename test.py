Students = ['student1','student2','student3','student4','student5','student6','student7','student8','student9','student10']
Marks = [45, 78, 12, 14, 48, 43, 47, 98, 35, 80]

# Students,Marks=zip(*sorted(zip(Students, Marks))) #addition to your code
students_mark_dict = dict(zip(Students, Marks))
top_5_students = {k: v for k, v in sorted(students_mark_dict.items(), key=lambda item: item[1], reverse=True)[0: 5]}
least_5_students = {k: v for k, v in sorted(students_mark_dict.items(), key=lambda item: item[1])[0:5]}
min_value = min(Marks)
max_value = max(Marks)
students_within_25_and_75 = {}
for k, v in students_mark_dict.items():
    percentile = float(v - min_value) / (max_value - min_value) * 100
    if 25 < percentile < 75:
        students_within_25_and_75[k] = v
students_within_25_and_75 = {k: v for k, v in sorted(students_within_25_and_75.items(), key=lambda item: item[1])}
print(least_5_students)
print(top_5_students)
print(students_within_25_and_75)
