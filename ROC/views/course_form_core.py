# -*- coding: utf-8 -*-

import numpy as np
import re

def StringTime2Array(stringtime):
	'''
	stringtime is a string, for instance, '4-6(前八周)' or '4-5(1,2,3,6-7周)'
	'''

	group = re.split(r',\s*(?![^()]*\))', stringtime)
	timeArray = np.zeros((7,6,16), np.int)
	# print group
	for item in group:
		item = item.strip()
		weekinfo = item[item.find("(")+1:item.find(")")]
		timeinfo = item[:item.find("(")]
		t1 = int(timeinfo[:timeinfo.find('-')]) - 1
		t2 = int(timeinfo[timeinfo.find('-')+1:]) - 1
		weekinfo = weekinfo[:-1]
		# print weekinfo, t1, t2
		if weekinfo == u'全':
			timeArray[t1, t2, :] = 1
		elif weekinfo == u'前八':
			timeArray[t1, t2, :8] = 1
		elif weekinfo == u'后八':
			timeArray[t1, t2, 9:] = 1
		elif weekinfo == u'单':
			timeArray[t1, t2, ::2] = 1
		elif weekinfo == u'双':
			timeArray[t1, t2, 1::2] = 1
		else:
			weekinfo = weekinfo.split(',')
			for t in weekinfo:
				mid = t.find('-')
				if mid >= 0:
					begin = int(t[:mid])-1
					end = int(t[mid+1:])
					timeArray[t1, t2, begin:end] = 1
				else:
					timeArray[t1, t2, int(t)-1] = 1
	return timeArray


def get_forms(available_time, dict, sorted_keys, courses):
	if len(sorted_keys) == 1:
		return_value = []
		for idx in range(len(dict[sorted_keys[0]])):
			time = dict[sorted_keys[0]][idx]
			criterion = available_time + time
			if not np.any(criterion > 1):
				tp = courses + [(sorted_keys[0], idx)]
				return_value.append(tp)
		return return_value
	else:
		return_value = []
		for idx in range(len(dict[sorted_keys[0]])):
			time = dict[sorted_keys[0]][idx]
			criterion = available_time + time
			if not np.any(criterion > 1):
				tp = courses + [(sorted_keys[0], idx)]
				return_value = return_value + get_forms(criterion, dict, sorted_keys[1:], tp)
		return return_value



def form_core(raw_dict, p_dict=None):
	'''
		This function performs course form Alg. for: input - python dict {'COURSE NAME': [available time]}
	where $[available time]$ is a list of all available times (stringtime is a string, for instance, '4-6(前八周)' or '4-5(1,2,3,6-7周)') 
	of course 'COURSE NAME' and produces all possible course forms as a list [course form], where $course form$ is 
	a representation of course as ('COURSE NAME', index in [available time])
	'''

	input_dict = {}
	for key in raw_dict.keys():
		input_dict[key] = []
		for i in range(len(raw_dict[key])):
			input_dict[key].append(StringTime2Array(raw_dict[key][i]))

	sorted_keys = sorted(input_dict, key=lambda k: len(input_dict[k]), reverse=False)
	timeArray = np.zeros((7,6,16), np.int)
	all_forms = get_forms(timeArray, input_dict, sorted_keys, [])

	final_result = []
	for form in all_forms:
		if len(all_forms) > 0:
			final_result.append(form)

	if len(final_result) == 0:
		return None

	final_form = []

	for i in range(len(final_result)):
		n_form = []
		for m1 in range(7):
			n_form.append([])
			for m2 in range(6):
				n_form[m1].append('')
		for c_name, c_idx in final_result[i]:
			for m1 in range(7):
				for m2 in range(6):
					if np.sum(input_dict[c_name][c_idx][m1][m2]) > 0:
						n_form[m1][m2] += '(' + c_name +' '+ raw_dict[c_name][c_idx] + ')'
		final_form.append(n_form)

	if p_dict == None:
		return final_form
	else:
		p_array = np.zeros((len(final_result),), np.float32)
		for i in range(len(final_result)):
			now_p = 0.0
			for c_name, c_idx in final_result[i]:
				now_p += p_dict[c_name][c_idx]
			p_array[i] = now_p
		sorted_order = np.argsort(-p_array)
		return [final_form[i] for i in sorted_order.tolist()]


if __name__ == '__main__':
	test_string0 = u'4-6(12周), 4-5(1,2,3,6-7周)'
	test_string1 = u'4-6(前八周), 4-5(1,2,3,6-7周)'

	test_string2 = u'4-6(后八周)'
	test_string3 = u'4-6(前八周)'
	print(StringTime2Array(test_string0))

	all_course = {u'语文':[test_string0,test_string1], u'英语':[test_string2,test_string3]}
	p_course = {u'语文':[0.5,1.0], u'英语':[0.7,0.7]}

	all_forms = form_core(all_course, p_course)
	print(all_forms)
