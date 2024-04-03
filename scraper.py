import requests
from bs4 import BeautifulSoup
import csv


def get_route_info(
    url: str = "https://www.mountainproject.com/route/105872293/corrugation-corner?print=1",
    comments_csv="/Users/juliewang/Documents/openmountain/comments.csv",
    routes_csv="/Users/juliewang/Documents/openmountain/routes.csv",
):
    """Note, use the print=1 version to get the data in a better version"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Write the comments to the CSV file
        with open(comments_csv, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Comment", "Time"])
            for comment in soup.find_all("div", class_="comment-body"):
                # Remove Data and [Hide Comment] from the text
                t = (
                    comment.text.replace("[Hide Comment]", "")
                    .strip()
                    .rsplit("\n", 1)[0]
                )
                writer.writerow([t, comment.span.text])

        # Find all route notes
        with open(routes_csv, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Grade", "Type", "Length", "Pitches", "Score", "Votes"])
            content = soup.find("div", class_="mb-1")
            children = [x for x in content.children if x != "\n"]
            # First entry is summary in form     5.7,\n                    Trad, 300 ft (91 m), 3 pitches,\n
            grade, climb_type, length, pitches = children[0].text.split(",")[:4]
            grade, climb_type, length, pitches = (
                grade.strip(" \n"),
                climb_type.strip(" \n"),
                length.strip(" \n"),
                pitches.strip(" \n"),
            )
            score = children[1].text.strip("\n")

            # Regex that extracts 3.9 from \n\n\n\n\n\n\n\n\n    \xa0Avg: 3.9 from 1,225\n    votes\n
            score = float(
                children[1]
                .text.split("Avg: ")[1]
                .split(" from")[0]
                .strip()
                .replace(",", "")
            )
            votes = int(
                children[1]
                .text.split("from")[1]
                .split("\n")[0]
                .strip()
                .replace(",", "")
            )
            writer.writerow([grade, climb_type, length, pitches, score, votes])

            # TODO get description, protection, and location
        print("here")

    else:
        print("Failed to retrieve the webpage")


if __name__ == "__main__":
    get_route_info()
