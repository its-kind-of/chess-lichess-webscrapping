# importing the packages
import scrapy
from scrapy.crawler import CrawlerProcess


# Chess game scraper class
class ChessGamesScraper(scrapy.Spider):
    # spider name
    name = 'chess_games_scraper'

    # base url
    base_url = 'https://lichess.org/@/Kingscrusher-YouTube/all?page='

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    # start crawling
    def start_requests(self):
        for page in range(1, 38):
            next_page = self.base_url + str(page)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_game_list)

    # parse game list
    def parse_game_list(self, response, **kwargs):
        # extracting the game links
        games = response.css('a.game-row__overlay::attr(href)').getall()

        # loop over game links
        for game in games:
            yield response.follow(url=game, headers=self.headers, callback=self.parse_game)
            #break

    def parse_game(self, response):
        # extract pgn
        pgn = response.css('div.pgn::text').get()

        # write pgn game to file
        with open('kingscrusher.pgn', 'a', encoding='utf-8') as f:
            f.write(pgn + '\n\n\n')


# main driver
if __name__== '__main__':
    process = CrawlerProcess()
    process.crawl(ChessGamesScraper)
    process.start()





















