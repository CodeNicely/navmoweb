from pandas import DataFrame
from register.models import user_data

refrence_id=[]
first_name=[]
last_name=[]
number=[]
email=[]
parent_father=[]
parent_mother=[]
dob=[]
tshirt_size=[]
address=[]
school=[]
grade=[]
gender=[]
exam_centre_1=[]
exam_centre_2=[]
exam_group_1=[]
exam_group_2=[]
flag_exam_centre_1=[]
flag_exam_centre_2=[]
flag_exam_group_1=[]
flag_exam_group_2=[]
flag_workshop=[]
flag_mpe_student=[]
image=[]

for o in user_data.objects.all():
	refrence_id.append(o.refrence_id)
	first_name.append(o.first_name)
	last_name.append(o.last_name)
	number.append(o.number)
	email.append(o.email)
	parent_father.append(o.parent_father)
	parent_mother.append(o.parent_mother)
	dob.append(o.dob)
	tshirt_size.append(o.tshirt_size)
	address.append(o.address)
	school.append(o.school)
	grade.append(o.grade)
	gender.append(o.gender)
	exam_centre_1.append(o.exam_centre_1)
	exam_centre_2.append(o.exam_centre_2)
	exam_group_1.append(o.exam_group_1)
	exam_group_2.append(o.exam_group_2)
	flag_exam_centre_1.append(o.flag_exam_centre_1)
	flag_exam_centre_2.append(o.flag_exam_centre_2)
	flag_exam_group_1.append(o.flag_exam_group_1)
	flag_exam_group_2.append(o.flag_exam_group_2)
	flag_workshop.append(o.flag_workshop)
	flag_mpe_student.append(o.flag_mpe_student)
	image.append(o.image) 
json_data={}
json_data['refrence_id']=refrence_id
json_data['first_name']=first_name
json_data['last_name']=last_name
json_data['number']=number
json_data['email']=email

json_data['parent_father']=parent_father
json_data['parent_mother']=parent_mother
json_data['dob']=dob
json_data['tshirt_size']=tshirt_size
json_data['address']=address

json_data['school']=school
json_data['grade']=grade
json_data['gender']=gender
json_data['exam_centre_1']=exam_centre_1
json_data['exam_centre_2']=exam_centre_2

json_data['exam_group_1']=exam_group_1
json_data['exam_group_2']=exam_group_2
json_data['flag_exam_centre_1']=flag_exam_centre_1
json_data['flag_exam_centre_2']=flag_exam_centre_2
json_data['flag_exam_group_1']=flag_exam_group_1

json_data['flag_exam_group_2']=flag_exam_group_2
json_data['flag_workshop']=flag_workshop
json_data['flag_mpe_student']=flag_mpe_student
json_data['image']=image

df = DataFrame(json_data)
df.to_excel('user_data.xlsx', sheet_name='sheet1', index=False)

