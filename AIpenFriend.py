from get_email import get_matching_messages
from send_email import reply_to_email
from watch_emails import load_threads, save_threads

def watch_and_respond():
    print("👀 Watching inbox and responding to known senders...\n")
    matching_messages = get_matching_messages(max_results=10)
    thread_data = load_threads()

    if not matching_messages:
        print("📭 No matching emails found.")
        return

    for msg in matching_messages:
        email = msg['email']
        subject = msg['subject']

        if email in thread_data:
            thread_id = thread_data[email]
            print(f"📎 Reusing saved thread for {email}: {thread_id}")
        else:
            thread_id = msg['threadId']
            thread_data[email] = thread_id
            print(f"📌 Saving new thread for {email}: {thread_id}")
            save_threads(thread_data)

        print(f"🔁 Replying to {email} | Subject: {subject}")
        reply_to_email(to_email=email, thread_id=thread_id, subject=f"Re: {subject}", original_message_id=msg['messageIdHeader'])


if __name__ == '__main__':
    watch_and_respond()