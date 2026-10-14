# generate_sample_dataset.py
# Builds a SYNTHETIC demo dataset (spam.csv) so the project runs out of the box.
#
# IMPORTANT: These messages are artificially generated from templates.
# This is NOT the UCI SMS Spam Collection. Use it to test that the project
# runs. For your report's real results, download the real dataset (see README)
# and replace spam.csv with it.
#
# Output format matches the Kaggle file: columns v1 (ham/spam) and v2 (text).

import csv
import random
from pathlib import Path

random.seed(42)

N_HAM = 700
N_SPAM = 250
OUT_FILE = Path(__file__).resolve().parent / 'spam.csv'

NAMES = ['Ravi', 'Priya', 'Anita', 'Karthik', 'Meena', 'Arjun', 'Divya', 'Suresh',
         'John', 'Sara', 'Mike', 'Emma', 'Kumar', 'Lakshmi', 'David', 'Nisha']
TIMES = ['tonight', 'tomorrow morning', 'this evening', 'on Friday', 'at 5 pm',
         'at 10 am', 'after lunch', 'this weekend', 'on Monday', 'at 7 pm',
         'tomorrow afternoon', 'next week']
ACTIVITIES = ['grab some coffee', 'watch the match', 'go for a walk', 'study together',
              'catch a movie', 'have dinner', 'play cricket', 'meet near the bus stand',
              'finish the assignment', 'visit grandma']
DOCS = ['project report', 'assignment', 'meeting notes', 'presentation', 'lab record',
        'invoice copy', 'class notes', 'budget sheet', 'draft document', 'timetable']
EVENTS = ['the meeting', 'the class', 'the seminar', 'the interview', 'the family function',
          'the review call', 'practice session', 'the exam', 'lunch', 'the workshop']
ROOMS = ['room 204', 'the main hall', 'the library', 'lab 3', 'the cafeteria',
         'conference room B', 'the seminar hall']
FOODS = ['rice and sambar', 'biryani', 'dosa', 'pasta', 'idli', 'fried rice', 'chapati and curry']
PLACES = ['home', 'the hostel', 'the canteen', 'my place', 'the restaurant near college']
CHORES = ['buy milk on the way home', 'pay the electricity bill', 'water the plants',
          'charge your phone', 'bring your ID card', 'lock the door', 'take your umbrella',
          'submit the form']
THANKS = ['your help yesterday', 'the notes', 'the lift this morning', 'the lovely dinner',
          'sending the file so quickly', 'covering for me', 'the birthday wishes']
HOMEWORK = ['assignment', 'lab program', 'homework', 'worksheet', 'practice test']

PRIZES = ['free iPhone', 'cash prize of 5000', 'holiday voucher', 'gift card worth 100',
          'brand new laptop', 'free cruise trip', 'shopping voucher', 'luxury watch',
          '2000 reward', 'free weekend getaway']
ACCOUNTS = ['bank', 'online banking', 'email', 'payment', 'mobile wallet', 'credit card',
            'insurance', 'social media']
PRODUCTS = ['mobile phones', 'designer shoes', 'health supplements', 'laptops',
            'watches', 'weight loss pills', 'sunglasses', 'online courses']
WORDS = ['reward', 'prize', 'secure', 'verify', 'bonus', 'offer', 'winner', 'claim',
         'account', 'deal', 'gift', 'cash']
CONTESTS = ['prize draw', 'lucky draw', 'weekly lottery', 'mega contest', 'holiday giveaway']
LOANS = ['personal loan', 'instant loan', 'credit card limit', 'cash advance']
DAYS = ['midnight', 'Sunday', 'tomorrow', 'the end of this week', 'today only']
KEYWORDS = ['WIN', 'PRIZE', 'CLAIM', 'JOIN', 'GIFT', 'CASH']


def phone():
    return random.choice(['0800', '09061', '08712', '0906', '0845']) + ' ' + \
        ''.join(random.choice('0123456789') for _ in range(3)) + ' ' + \
        ''.join(random.choice('0123456789') for _ in range(3))


def url():
    return 'http://' + random.choice(WORDS) + '-' + random.choice(WORDS) + '.example/' + \
        ''.join(random.choice('abcdefghijkmnpqrstuvwxyz23456789') for _ in range(5))


def shortcode():
    return ''.join(random.choice('0123456789') for _ in range(5))


def amount():
    return random.choice(['100', '250', '500', '1000', '2500', '5000', '10000'])


def spam_message():
    t = random.randint(0, 17)
    if t == 0:
        return f'Congratulations! You have won a {random.choice(PRIZES)}! Call {phone()} now to claim your reward. Offer ends {random.choice(DAYS)}.'
    if t == 1:
        return f'FREE entry in our {random.choice(CONTESTS)}. Text {random.choice(KEYWORDS)} to {shortcode()} to enter. T&Cs apply.'
    if t == 2:
        return f'URGENT! Your {random.choice(ACCOUNTS)} account has been suspended. Verify your details at {url()} immediately to avoid closure.'
    if t == 3:
        return f'You have been selected for a {random.choice(PRIZES)}. Reply YES to claim before {random.choice(DAYS)}.'
    if t == 4:
        return f'Get {random.choice([20, 30, 50, 70, 80])}% off {random.choice(PRODUCTS)} today only! Shop now at {url()}'
    if t == 5:
        return f'Limited offer: {random.choice(LOANS)} approved up to {amount()}. Apply now at {url()}. No credit check needed!'
    if t == 6:
        return f'Your parcel could not be delivered. Pay a small fee of {amount()[:2]} at {url()} to reschedule delivery.'
    if t == 7:
        return f'Earn {amount()} per week working from home. No experience needed. Visit {url()} and start today!'
    if t == 8:
        return f'Subject: Final notice - claim your {random.choice(PRIZES)}. Dear customer, you are our lucky winner. Click {url()} to confirm your details now.'
    if t == 9:
        return f'Your mobile number has won {amount()} in the {random.choice(CONTESTS)}. Contact {phone()} to collect your cash. Hurry!'
    if t == 10:
        return f'WINNER! As a valued customer you have been chosen to receive a {random.choice(PRIZES)}. To claim call {phone()}. Offer ends {random.choice(DAYS)}.'
    if t == 11:
        return f'Act now! {random.choice(PRODUCTS).capitalize()} at the lowest price ever. Click {url()} before stock runs out.'
    if t == 12:
        return f'Your {random.choice(ACCOUNTS)} card is blocked. Call {phone()} or login at {url()} to unblock it now.'
    if t == 13:
        return f'Subject: Exclusive investment opportunity. Double your money in {random.choice([7, 10, 14, 30])} days. Guaranteed returns. Reply now to join.'
    if t == 14:
        return f'FREE ringtone and wallpaper! Text {random.choice(KEYWORDS)} to {shortcode()}. Subscription {random.choice(["1.50", "2.00", "3.00"])} per week. Reply STOP to cancel.'
    if t == 15:
        return f'Dear customer, your {random.choice(ACCOUNTS)} password expires today. Update it at {url()} or lose access permanently.'
    if t == 16:
        return f'You are our {random.choice(["1000th", "lucky", "special"])} visitor! Claim your {random.choice(PRIZES)} at {url()} now. Do not miss out.'
    return f'Hot deal! Buy {random.choice(PRODUCTS)} and get a free gift. Call {phone()} now. Limited stock, order today.'


def ham_message():
    t = random.randint(0, 24)
    n = random.choice(NAMES)
    if t == 0:
        return f'Hey, are you free {random.choice(TIMES)}? Let us {random.choice(ACTIVITIES)}.'
    if t == 1:
        return f'Can you send me the {random.choice(DOCS)} before {random.choice(TIMES)}?'
    if t == 2:
        return f'I will be a little late for {random.choice(EVENTS)}. Please start without me.'
    if t == 3:
        return f'Do not forget to {random.choice(CHORES)}.'
    if t == 4:
        return f'Thanks for {random.choice(THANKS)}. See you {random.choice(TIMES)}.'
    if t == 5:
        return f'Meeting moved to {random.choice(TIMES)} in {random.choice(ROOMS)}. Please bring the {random.choice(DOCS)}.'
    if t == 6:
        return f'What time does {random.choice(EVENTS)} start {random.choice(TIMES)}?'
    if t == 7:
        return f'Happy birthday {n}! Have a wonderful day and enjoy the celebration.'
    if t == 8:
        return f'Reminder: {random.choice(EVENTS)} is {random.choice(TIMES)} in {random.choice(ROOMS)}.'
    if t == 9:
        return f'Dinner at {random.choice(PLACES)} {random.choice(TIMES)}? Mom is making {random.choice(FOODS)}.'
    if t == 10:
        return f'Subject: Project update. Hi {n}, please find the {random.choice(DOCS)} attached. Let me know your comments by {random.choice(TIMES)}.'
    if t == 11:
        return f'Ok, I will call you when I reach {random.choice(PLACES)}.'
    if t == 12:
        return f'Did you finish the {random.choice(HOMEWORK)}? I am stuck on question {random.randint(2, 15)}.'
    if t == 13:
        return f'Are you free to talk {random.choice(TIMES)}? I wanted to ask about {random.choice(EVENTS)}.'
    if t == 14:
        return f'We won the {random.choice(["cricket", "football", "kabaddi", "badminton"])} match today! {n} scored the winning point.'
    if t == 15:
        return f'Urgent: the {random.choice(DOCS)} needs your signature before {random.choice(TIMES)}. Please check your desk.'
    if t == 16:
        return f'Congratulations on your {random.choice(["promotion", "new job", "result", "exam success", "selection"])}, {n}! So proud of you.'
    if t == 17:
        return f'Please call me when you get this message. It is about {random.choice(EVENTS)}.'
    if t == 18:
        return f'I shared the {random.choice(DOCS)} with you. Open the link in the shared folder and add your part.'
    if t == 19:
        return f'Subject: Meeting minutes. Dear team, the minutes of {random.choice(EVENTS)} are attached. Kindly review {random.choice(TIMES)}.'
    if t == 20:
        return f'Your appointment is confirmed for {random.choice(TIMES)}. Reply C to cancel or R to reschedule.'
    if t == 21:
        return f'{n}, I left the keys with the neighbour. Pick them up {random.choice(TIMES)} and lock the door.'
    if t == 22:
        return f'Can we shift the {random.choice(["call", "meeting", "class", "practice"])} to {random.choice(TIMES)}? Something came up.'
    if t == 23:
        return f'I am at {random.choice(PLACES)} now. Where are you? Text me when you are close.'
    return f'Good morning {n}! Have a great day. Do not forget the {random.choice(DOCS)} {random.choice(TIMES)}.'


def build(generator, count):
    items = set()
    attempts = 0
    while len(items) < count and attempts < count * 200:
        items.add(generator())
        attempts += 1
    if len(items) < count:
        print(f'Warning: only {len(items)} unique messages generated (wanted {count}).')
    return sorted(items)


def main():
    ham = build(ham_message, N_HAM)
    spam = build(spam_message, N_SPAM)
    rows = [('ham', m) for m in ham] + [('spam', m) for m in spam]
    random.shuffle(rows)
    with open(OUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['v1', 'v2'])
        writer.writerows(rows)
    print(f'Wrote {len(rows)} rows to {OUT_FILE}: {len(ham)} ham, {len(spam)} spam')


if __name__ == '__main__':
    main()
