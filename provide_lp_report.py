import datetime
from dateutil import parser
import operator
import pytz
from launchpadlib.launchpad import Launchpad


engineers = ['tnurlygayanov', 'akuznetsova', 'ylobankov', 'vrovachev',
             'esikachev', 'vgusev', 'svasheka', 'ogubanov', 'obutenko',
             'kkuznetsova', 'kromanenko', 'vryzhenkin', 'agalkin']
raiting = []

cachedir = "~/.launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)

one_week_ago_date = datetime.datetime.now() - datetime.timedelta(weeks=16)

created_on_this_week_total = 0
line = "-" * 137

for engineer in engineers:
    bugs_score = 0
    p = launchpad.people[engineer]

    print "\n\n {0} ".format(p.display_name)
    print line
    s = "| {0}\t\t| {1}\t| {2}\t\t| {3}\t\t| {4}\t\t\t\t\t\t\t|"
    print s.format("ID", "Priority", "Status", "Assigned To", "Link")
    print line

    list_of_bugs = p.searchTasks(status=["New", "Incomplete", "Invalid",
                                         "Won't Fix", "Confirmed", "Triaged",
                                         "In Progress", "Fix Committed",
                                         "Fix Released", "Opinion", "Expired"],
                                 bug_reporter=p,
                                 modified_since=one_week_ago_date)
    created_on_this_week = []

    for bug in list_of_created_bugs:
        bug_created_date = parser.parse(bug.date_created.ctime())

        if bug_created_date > parser.parse(one_week_ago_date.ctime()):
            created_on_this_week.append(bug)

            assigned_to = "None" if not bug.assignee else bug.assignee.name
            if len(assigned_to) < 6:
                assigned_to += "\t"
            if len(assigned_to) < 14:
                assigned_to += "\t"

            status = bug.status
            if len(status) < 7:
                status += "\t"
            if len(status) < 14:
                status += "\t"

            web_link = bug.web_link
            if len(web_link) < 45:
                web_link += "\t"

            importance = bug.importance
            if len(importance) < 5:
                importance += "\t"

            s = "| {0:d}\t| {1:s}\t| {2:s}\t| {3:s}\t| {4:s}\t|"
            print s.format(bug.bug.id, importance, status, assigned_to,
                           web_link)
            created_on_this_week_total += 1

            if bug.status not in ["Incomplete", "Invalid", "Won't Fix",
                                  "Opinion", "Expired"]:
                bug_score = 1
                if bug.importance in ["High", "Critical"]:
                    bug_score = 2 * bug_score
                if bug.status == "In Progress":
                    bug_score = 2 * bug_score
                if bug.status in ["Fix Committed", "Fix Released"]:
                    bug_score = 3 * bug_score
                # if engineer fixed this bug:
                if bug.assignee is not None and bug.assignee.name == engineer:
                    bug_score = 2 * bug_score
                bugs_score += bug_score

    raiting.append({"name": p.display_name,
                    "bugs_total": len(created_on_this_week),
                    "score": bugs_score})

    print line
    print "Total bugs found during the last week:", len(created_on_this_week)

s = "\n\nTotal bugs found during the last week by MOS QA team:"
print s, created_on_this_week_total

line = "-" * 73
print "\n\n\nRaiting:"
print line
s = "| {0:s}\t\t\t| {1:s}\t| {2:s}\t|"
print s.format("Engineer", "Total Bugs Count", "Total Score")
print line
raiting.sort(key=operator.itemgetter('score'), reverse=True)

for engineer in raiting:
    name = engineer['name']
    if len(name) < 13:
        name += '\t'

    s = "| {0:s}\t\t| {1:d}\t\t\t| {2:d}\t\t|"
    print s.format(name, engineer['bugs_total'], engineer['score'])

print line
