import praw
import subprocess
from playwright.sync_api import sync_playwright
import random

how_many_post_check = 10

answers = []
the_car = []
ums = {
    1: "I think it's a",
    2: "pretty sure that's a",
    3: "I'm guessing that's a",
    4: "It looks like that's a",
    5: "Could be a",
    6: "It looks to me like that's a",
}

def getting_info(link):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(permissions=['clipboard-read', 'clipboard-write', 'accessibility-events'])
        page = context.new_page()
        page.goto(link)
        
        screenshot_path = "screenshot.png"
    
        look = page.get_by_alt_text('r/spotted - ', exact=False)
        look.nth(0).screenshot(path=screenshot_path)

        subprocess.run(["osascript", "-e", f'set the clipboard to (read (POSIX file "{screenshot_path}") as JPEG picture)'])
        
        page.goto("https://www.google.com/")
        # if page.frame_locator("iframe[name=\"callout\"]").get_by_label("Not now") != None:
        #     page.frame_locator("iframe[name=\"callout\"]").get_by_label("Not now").click()
        # else: pass
        page.click('svg.Gdd5U')
        page.click('div.BH9rn')
        
        page.keyboard.press("Meta+V")
        if page.locator('h2.DeMn2d') != None:
            car = page.locator('h2.DeMn2d').text_content()
        else:
            car = page.locator("div.DeMn2d").text_content()
        
        the_car.append(car)
        print(car)

        num = random.randint(1, 6)
        answer = f"{ums[num]} {car}"
        answers.append(answer)
        return answer

reddit = praw.Reddit(
    client_id="#",
    client_secret="#",
    user_agent="#",
    username = "#",
    password = "#",
)

def get_links():
    subreddit = reddit.subreddit("spotted")
    flair_text = 'UNKNOWN'
    submission_urls = []

    for submission in subreddit.new(limit=80):
        if submission.link_flair_text == flair_text:
            submission_url = "https://www.reddit.com" + submission.permalink
            submission_urls.append(submission_url)
            if len(submission_urls) == how_many_post_check:
                break

    return submission_urls

def check_comment(link):
    url = link
    sub = reddit.submission(url=url)

    for comment in sub.comments:
        if isinstance(comment, praw.models.Comment):
            if the_car[0] in comment.body and comment.author == 'Unlucky_Resolution46':
                print("Already commented.")
                exit()

    print(f"You commented: {answers[0]}")
    sub.reply(answers[0])
    answers.pop(0)

def main():
    submission_urls = get_links()
    if submission_urls:
        for url in submission_urls:
            getting_info(url)
            check_comment(url)
    else:
        print("No new posts")

if __name__ == '__main__':
    main()

    # make it so it dosent quit when its been commented otherwise you can't run it multiple times
    # make it check the comment first then get the info