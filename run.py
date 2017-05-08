import powerball

ticket_collection = powerball.collect_tickets()

print "Done entering employees into the Powerball drawing."

powerball.display_employees(ticket_collection)

winning_numbers = powerball.draw_numbers([ticket["numbers"] for ticket in ticket_collection])

print "Powerball winning numbers: "
print "%s Powerball: %d" % (" ".join(map(str, winning_numbers[:5])), winning_numbers[5])