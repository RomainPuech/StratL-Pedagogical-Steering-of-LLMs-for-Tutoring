def print_logs(log):
    print("--------\n")
    for msg in log:
        print(msg)
    print("--------\n")


def generate_messages(student_messages,tutor_messages,init_message,role):
    if role == "student":
        roles = ["user","assistant"]
    else:
        roles = ["assistant","user"]

    messages = [{"role": "system", "content": init_message}]

    for i in range(min(len(student_messages),len(tutor_messages))):

        messages.append({"role": roles[0], "content": tutor_messages[i]})
        messages.append({"role": roles[1], "content": student_messages[i]})

    if role == "student" and len(student_messages) < len(tutor_messages):
        messages.append({"role": "user", "content": tutor_messages[-1]})
    elif role == "tutor" and len(student_messages) > len(tutor_messages):
        messages.append({"role": "user", "content": student_messages[-1]})

    return messages