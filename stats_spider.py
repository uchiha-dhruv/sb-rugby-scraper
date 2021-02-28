from typing import List
import scrapy
from datetime import datetime


def player_pos(player_positions):
    final_positions: List[int] = []
    for item in player_positions:
        if item == 'Full Back':
            final_positions.append(15)
        elif item == 'Right Wing':
            final_positions.append(14)
        elif item == 'Center':
            if 13 not in final_positions:
                final_positions.append(13)
            else:
                final_positions.append(12)
        elif item == 'Left Wing':
            final_positions.append(11)
        elif item == 'Outside Half':
            final_positions.append(10)
        elif item == 'Scrum Half':
            final_positions.append(9)
        elif item == 'Prop':
            if 1 not in final_positions:
                final_positions.append(1)
            else:
                final_positions.append(3)
        elif item == 'Hooker':
            final_positions.append(2)
        elif item == 'Lock':
            if 4 not in final_positions:
                final_positions.append(4)
            else:
                final_positions.append(5)
        elif item == 'Blindside Flanker':
            final_positions.append(6)
        elif item == 'Openside Flanker':
            final_positions.append(7)
        elif item == 'No. 8':
            final_positions.append(8)

    return final_positions


def match_date(extracted_date):
    dt_object = datetime.strptime(extracted_date, "%d %b %Y")
    day = dt_object.strftime("%d")
    month = dt_object.strftime("%m")
    year = dt_object.strftime("%Y")
    new_date = day + month + year
    return new_date


def final_written_date(extracted_date):
    dt_object = datetime.strptime(extracted_date, "%d %b %Y")
    date_value = dt_object.strftime("%d")
    if date_value == '01' or date_value == '21' or date_value == '31':
        output = dt_object.strftime("%A, %B %dst, %Y")
    elif date_value == '02' or date_value == '22':
        output = dt_object.strftime("%A, %B %dnd, %Y")
    elif date_value == '03' or date_value == '23':
        output = dt_object.strftime("%A, %B %drd, %Y")
    else:
        output = dt_object.strftime("%A, %B %dth, %Y")

    return output


class RugbyStatSpider(scrapy.Spider):
    name = 'stats'
    with open("C:\\Links\\links19-20.txt",
              "r") as file:
        start_urls = [url.strip() for url in file.readlines()]

    def parse(self, response):
        team1 = response.css(".matchSquads:nth-child(10) .playerName::text, .matchSquads:nth-child(7) .playerName::text").extract()
        team2 = response.css(".matchSquads:nth-child(11) .playerName::text, .matchSquads:nth-child(8) .playerName::text").extract()
        player_name = team1 + team2
        team1_pos = response.css(".matchSquads:nth-child(10) .profileLink::text, .matchSquads:nth-child(7) .profileLink::text").extract()
        team2_pos = response.css(".matchSquads:nth-child(11) .profileLink::text, .matchSquads:nth-child(8) .profileLink::text").extract()
        team1_positions = player_pos(team1_pos)
        team2_positions = player_pos(team2_pos)
        player_position = team1_positions + team2_positions
        extracted_date = response.css(".matchStatsInt:nth-child(1) p::text").extract_first()
        date = match_date(extracted_date)
        written_date = final_written_date(extracted_date)
        score = response.css(".paddingNone::text").extract_first()
        score = score.strip()
        score = score.split("-")
        hometeamscore = score[0]
        awayteamscore = score[1]
        venue = response.css(".matchStatsInt:nth-child(3) p::text").extract_first()
        team1_name = response.css("h2.floatLeft::text").extract_first()
        team2_name = response.css("h2.floatRight::text").extract_first()

        row_data = zip(player_name, player_position)

        # Making extracted data row-wise
        for item in row_data:
            # create a dictionary to store the scraped info
            scraped_info = {
                # key:value
                'Team Name': team1_name if item[0] in team1 else team2_name,
                'Date': date,
                'Player Name': item[0],
                'Position': item[1],
                ' ': ' ',
                'Written Date': written_date,
                'Venue': venue,
                'Score': hometeamscore if item[0] in team1 else awayteamscore,
                'Round #': ' ',
                'Competition': 'Pro14',
                '  ': ' ',
                '   ': ' ',
                '    ': ' ',
                'Home/away': 'H' if item[0] in team1 else 'A',
                'Opposition Team': team2_name if item[0] in team1 else team1_name

            }

            # yield or give the scraped info to scrapy
            yield scraped_info
