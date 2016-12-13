#!/usr/bin/env python3
import sys
import math

# This Program will evaluate a string of mathematical sequences 
# into numeric form.

def is_num(n):
	for i in range(ord('0'), ord('9') + 1):
		if ord(n) == i:
			return True
	return False
	
def is_allnum(n):
	for i in range(len(n)):
		if not (is_num(n[i]) or n[i] == '.' or (n[i] == '-' and i == 0)):
			return False
	return True

def parseOp(exp):
	op_index = -1
	if is_allnum(exp):
		return float(exp)
	for i in range(len(exp)):
		if not (is_num(exp[i]) or exp[i] == '.' or (exp[i] == '-' \
                    and (i == 0 or not is_num(exp[i-1])))):
			op_index = i

	num1 = float(exp[:op_index])
	num2 = float(exp[op_index+1:])
	if exp[op_index] == '+':
		ans = num1 + num2
	elif exp[op_index] == '-':
		ans = num1 - num2
	elif exp[op_index] == '*':
		ans = num1 * num2
	elif exp[op_index] == '/':
		ans = num1 / num2
	elif exp[op_index] == '^':
		ans = num1 ** num2
	return ans
	
def get_ops(exp):
	op_index = []
	for i in range(len(exp)):
		if not (is_num(exp[i]) or exp[i] == '.' or \
                        (exp[i] == '-' and (i == 0 or not is_num(exp[i-1])))):
			op_index.append(i)
	return op_index	

def edmas(exp, ops, op_index):
	i = 0
	while i < len(op_index):
		if exp[op_index[i]] == ops[0] or exp[op_index[i]] == ops[1]:
			begin = 0
			end = 0
			if i != 0:
				begin = op_index[i - 1] + 1
			if i + 1 >= len(op_index):
				end = len(exp) - 1
			else:
				end = op_index[i + 1] - 1
			exp = exp[:begin] + str(parseOp(exp[begin:end + 1])) + exp[end + 1:]
			op_index = get_ops(exp)
			i -= 1
		i += 1
	return exp
	
def next_bracket(exp, start):
	depth = 0
	for i in range(start, len(exp)):
		if exp[i] == '(':
			depth += 1
		if exp[i] == ')':
			depth -= 1
			if depth == 0:
				return i
	return -1

def parse(exp):
	op_index = []
	ans = 0.0
	next_b = -1
	i = 0
	const_names = 'pi','e'
	const_vals = math.pi, math.e
	for j, const_name in enumerate(const_names):
		while const_name in exp:
			if exp[i:i + len(const_name)] == const_name:
				exp = exp.replace(const_name,str(const_vals[j]))
				i = 0
			i += 1
		i = 0
	ops = 'sqrt','ln','log','asin','sin','acos','cos','atan','tan','degrees','radians','factorial'
	fcts = math.sqrt, math.log, math.log10, math.asin, \
		math.sin, math.acos, math.cos, math.atan, math.tan, math.degrees, math.radians, math.factorial
	for j, op in enumerate(ops):
		while op in exp and i < len(exp):
			if exp[i:i+len(op)] == op:
				nextb = next_bracket(exp,i)
				substr = exp[i+len(op) + 1:nextb]
				exp = exp.replace(exp[i:nextb+1], str(fcts[j](float(parse(substr)))))
				
				#print (exp)
				i = 0
			i+= 1
		i = 0
	i = 0
	while '(' in exp:
		if exp[i] == '(':
			next_b = next_bracket(exp, i)
			#print(exp[i+1:next_b])
			exp = exp.replace(exp[i:next_b+1],parse(exp[i+1:next_b]))
			#print (exp)
			i = 0
		i += 1
	op_index = get_ops(exp)
	#print(op_index)
	exp = edmas(exp,'^$', op_index)
	op_index = get_ops(exp)
	exp = edmas(exp,'*/', op_index)
	op_index = get_ops(exp)
	exp = edmas(exp,'+-', op_index)
	return exp
	
def remove_whitespace(string):
	dummy = ''
	for c in string:
		if c != ' ':
			dummy += c
	return dummy

def main():
	exp = ''
	if len(sys.argv) == 1:
		exit(0)
	if sys.argv[1] == '-i':
		print ("Copyright 2013, Abel MacNeil. Last updated May 8, 2013")
		while exp != 'exit':
			try:
				exp = input()
			except KeyboardInterrupt:
				print ("Bye.")
				exit(0)
			try:
				if exp != 'exit':
					print('=', parse(remove_whitespace(exp)))
			except ValueError:
				print ("Result is too large.")
	else:
		exp = sys.argv[1]
		try:
			print(exp,' = ', parse(remove_whitespace(exp)))
		except ValueError:
			print ("Result is too large.")
			
			
if __name__ == "__main__":
	main()
