import os
import xml.dom.minidom


def test(commmand):
    return 'test OK :) good job.'


def get_queue():
    """Returns the SGE queue.

       If you want to quickly test this function on local machines without
       SGE, you can use this line instead of calling `qstat` (poor meren's
       test mode):

            f = open('barhalbot/examples/qstat.xml')

       But then you really shouldn't commit that to the repository :p
       """

    f = os.popen('qstat -u \* -xml')

    dom = xml.dom.minidom.parse(f)

    jobs = dom.getElementsByTagName('job_info')
    run = jobs[0]

    joblist = run.getElementsByTagName('job_list')

    queue = {'pending': {}, 'running': {}}
    jobs_list = []

    for r in joblist:
        state = r.getAttribute('state')
        job = r.getElementsByTagName('JB_name')[0].childNodes[0].data.replace('snakejob.', '')
        owner = r.getElementsByTagName('JB_owner')[0].childNodes[0].data
        slots = int(r.getElementsByTagName('slots')[0].childNodes[0].data)

        try:
            start_time = r.getElementsByTagName('JAT_start_time')[0].childNodes[0].data
        except:
            start_time = None

        jobs_list.append((owner, job, slots, state, start_time), )

        if state in queue:
            if owner in queue[state]:
                queue[state][owner]['num_jobs'] += 1
                queue[state][owner]['num_slots'] += slots
            else:
                queue[state][owner] = {'num_jobs': 1, 'num_slots': slots}

    return queue, jobs_list



def queue_list():
    queue, jobs_list = get_queue()

    response = ""

    if not len(queue['running']):
        response += "There are no running jobs. "
    else:
        running_jobs = sorted(queue['running'].items(), key=lambda x: x[1]['num_slots'], reverse=True)
        response += "There are *%d jobs running that use %d slots*. Here are the culprits: %s. " % \
                (sum([_[1]['num_jobs'] for _ in running_jobs]),
                 sum([_[1]['num_slots'] for _ in running_jobs]),
                 ', '.join(['*%s* (_%d jobs using %d slots_)' % (e[0], e[1]['num_jobs'], e[1]['num_slots']) for e in running_jobs]))

    if not len(queue['pending']):
        response += "Aaaaaaaand there are no pending jobs. "
    else:
        pending_jobs = sorted(queue['pending'].items(), key=lambda x: x[1]['num_slots'], reverse=True)
        response += "There are also *%d jobs pending* that need %d slots in total. They belong to %s. " % \
                (sum([_[1]['num_jobs'] for _ in pending_jobs]),
                 sum([_[1]['num_slots'] for _ in pending_jobs]),
                 ', '.join(['*%s* (_%d jobs needing %d slots_)' % (e[0], e[1]['num_jobs'], e[1]['num_slots']) for e in pending_jobs]))

    return(response)


def queue_list_user(username):
    queue, jobs_list = get_queue()

    users_with_jobs = set([e[0] for e in jobs_list])
    if username not in users_with_jobs:
        return('But *%s* does not have any jobs in the queue :/ %s: %s.' % \
                    (username, 'These people do' if len(users_with_jobs) > 1 else "This one does", ', '.join(users_with_jobs)))

    response = []
    jobs_sorted = [j for j in sorted(jobs_list, key=lambda x: x[3], reverse=True) if j[0] == username]

    max_num_jobs_to_display = 5
    num_jobs_to_be_displayed = 0
    for (owner, job, slots, state, start_time) in jobs_sorted:
        num_jobs_to_be_displayed += 1

        if num_jobs_to_be_displayed > max_num_jobs_to_display:
            response.append(' .. _and %d more jobs in the list_.' % (len(jobs_sorted) - max_num_jobs_to_display))
            break
        else:
            response.append("`%s` _(%d %s, %s%s)_" % (job, slots, 'slots' if slots > 1 else 'slot', state, ' since %s' % start_time.replace('T', ', ') if start_time else ''))

    return ("*%s's %d %s*: %s." % (username, len(response), 'jobs' if len(response) > 1 else 'job', ', '.join(response)))


def queue(command):
    sub_commands = {'null': queue_list,
                    'user': queue_list_user}

    s = command.split()

    if len(s) > 3 or len(s) == 2:
        return "The 'queue' command is upset with you. Try 'queue' or 'queue user USERNAME'."

    if len(s) == 1:
        return sub_commands['null']()

    if s[1] not in sub_commands:
        return "Well, the 'queue' command does not recognize the subcommand '%s'." (s[1])
    else:
        return sub_commands[s[1]](s[2])


simple_commands = {
    'hey': 'hai!',
    'yo': ':)',
    'hi': 'hi!',
}

complex_commands = {
    'test': test,
    'queue': queue,
}

