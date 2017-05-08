import random

# get ordinal number, e.g. 1st, 2nd, 3rd, 4th, 5th, etc.
def get_ord_num(n):
	if n == 1:
		on = "1st"
	elif n == 2:
		on = "2nd"
	elif n == 3:
		on = "3rd"
	else:
		on = "%dth" % n

	return on


def get_powerball_ticket():
	while True:
		first_name = raw_input("Enter your first name: ")
		last_name = raw_input("Enter your last name: ")
		first_name = first_name.strip()
		last_name = last_name.strip()

		if first_name.isalpha() and last_name.isalpha():
			name = (first_name, last_name)
			break
		else:
			print "Please enter a valid first and last name!"

	numbers = []
	for i in range(6):
		i += 1
		ord_num = get_ord_num(i)	

		if i == 1:
			prompt_text = "Select %s # (1 thru 69): " % ord_num
		elif i == 6:
			prompt_text = "Select Power Ball # (1 thru 26): "
		else:
			prompt_text = "Select %s # (1 thru 69 excluding %s): " % (ord_num, ', '.join(map(str, numbers)))

		while True:
			try:
				number = int(raw_input(prompt_text))

				if i != 6 and (number < 1 or number > 69):
					print "Please enter a number 1 thru 69!"
				elif i == 6 and (number < 1 or number > 26):
					print "Please enter a number 1 thru 26!"
				elif number in numbers:
					print "Your number selections must be unique!"
				else:
					break
			except ValueError:
				print "Please enter a valid number 1 thru 69!"

		numbers.append(number)

	return {"name": name, "numbers": numbers}


def collect_tickets():
	ticket_collection = []

	while True:
		ticket = get_powerball_ticket()
		ticket_collection.append(ticket)
		while True:
			try:
				yn = str.lower(raw_input("Would you like to enter another employee? (y/n): "))
				if yn == "y" or yn == "n":
					break
				else:
					print "Please enter 'y' or 'n'"
			except TypeError:
				print "Please enter 'y' or 'n'"

		if yn == "n":
			break

	return ticket_collection


def display_employees(tc):
	for t in tc:
		print "%s %s %s Powerball: %d" % (t["name"][0], t["name"][1], " ".join(map(str, t["numbers"][:5])), t["numbers"][5])


def draw_numbers(ticket_numbers):
	# Requirements:
	# - Calculate frequency of each selected number
	# - Use the most common numbers as the lottery numbers
	# - If there is a tie, randomly select the tied number between the two
	# - Determine powerball separately
	# Note: I am not taking order into consideration. I could not discern this from the prompt.
	winning_numbers = []

	# a little python magic to transpose list of lists
	# from ticket numbers grouped by employee to grouped by
	# each number chosen 1st, each number chose 2nd, etc. (slots)
	numbers_by_slot = zip(*ticket_numbers)
	powerballs = numbers_by_slot[5]

	# we can combine all but the lottery number choices into one list
	# and break down by frequency counts
	chosen_numbers = [item for sublist in numbers_by_slot[:5] for item in sublist]
	number_counts = {i: chosen_numbers.count(i) for i in chosen_numbers}
	
	# organize dictionary by list of lottery numbers with given count
	counts_d = {}
	for key in number_counts:
		freq = number_counts[key]
		if freq not in counts_d:
			counts_d[freq] = []
		counts_d[freq].append(key)

	# get winning numbers
	max_dups = max(counts_d.keys())
	while max_dups > 0 or len(winning_numbers) < 5:
		if max_dups in counts_d: 
			# how many winning numbers are left TBD?
			num_left = 5 - len(winning_numbers)

			# try to get that many from the current list
			curr_num = counts_d[max_dups]

			# shuffle the list and pop values off
			random.shuffle(curr_num)
			winning_numbers = winning_numbers + curr_num[:num_left]

		max_dups -= 1

	# get powerball, same algo
	powerball_counts = {i: powerballs.count(i) for i in powerballs}
	pb_counts_d = {}
	for key in powerball_counts:
		freq = powerball_counts[key]
		if freq not in pb_counts_d:
			pb_counts_d[freq] = []
		pb_counts_d[freq].append(key)

	pb_max_dups = max(pb_counts_d.keys())
	max_pb_num = pb_counts_d[pb_max_dups]
	random.shuffle(max_pb_num)

	winning_numbers.append(max_pb_num[0])

	return winning_numbers