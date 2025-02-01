import pandas as pd
from requests import get, RequestException
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class LetterboxdScraper(BeautifulSoup):
    def __init__(self, user, headers, base_url="https://letterboxd.com"):
        self.user = user
        self.headers = headers
        self.base_url = base_url
        self.names = []
        self.links = []
        self.rating = []
        self.like = []

        try:
            response = get(f"{self.base_url}/{self.user}/films/page/1", headers=self.headers)
            super().__init__(response.text, 'html.parser')
        except RequestException:
            raise Exception("Erro na requisição.")

        if self.title and self.title.string == "Letterboxd - Not Found":
            raise ValueError("Usuário não encontrado no Letterboxd.")


    def scrape_page(self, page_number):
        response = get(f"{self.base_url}/{self.user}/films/page/1", headers=self.headers)
        site = BeautifulSoup(response.text, 'html.parser')
        for item in site.find_all('li', {"class": "poster-container"}):
            # Extraindo o nome do filme
            name_match = re.search(r'img alt="(.*?)"', str(item))
            # Extraindo o link do filme
            link_match = re.search(r'data-target-link="(.*?)"', str(item))
            # Extraindo nota do filme
            rating_span = item.find('span', class_='rating')
            # Extraindo like do filme
            like_match = item.find('span', class_='like')

            if rating_span:
                # Contar quantas estrelas existem no texto
                num_stars = rating_span.text.count('★') + rating_span.text.count('½')/2
                self.rating.append(num_stars)
            else:
                self.rating.append(None)
            
            if like_match:
                self.like.append(1)
            else:
                self.like.append(0)
                

            if name_match and link_match:
                self.names.append(name_match.group(1))
                self.links.append(f"{self.base_url}{link_match.group(1)}")


    def get_number_pages(self):
        paginate = self.find_all('li', {'class': 'paginate-page'})
        if paginate:
            string = str(paginate[-1])
            match = re.search(r'>(\d+)<', string)
            return int(match.group(1)) if match else 1
        return 1

    def scrape_all_pages(self):
        total_pages = self.get_number_pages()

        def process_page(page):
            self.scrape_page(page)

        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(process_page, range(1, total_pages + 1)))

    def movie_dataframe(self):
        return pd.DataFrame({
            "Name": self.names,
            "Rating":self.rating,
            "Like":self.like,
            "Link": self.links
        })
    
    def extract_movie_data(self):
        def fetch_data(row):
            film_id, _, _, url  = row
            try:
                response = get(url, headers=headers, timeout=10)
                site = BeautifulSoup(response.text, 'html.parser')
                response2 =  get(url+"fans/", headers=headers, timeout=10)
                site2 = BeautifulSoup(response2.text, 'html.parser')

                if 'Not Found' in str(site.title):
                    return film_id, None, None, None, None

                # Extract data
                try:
                    meta_string = str(site.find('meta', {'name': 'twitter:data2'}))
                    avr_rating = re.search(r'[0-9]\.[0-9][0-9]', meta_string).group(0)
                except:
                    avr_rating = None
                
                try:
                    year = re.findall(r">([0-9]+)<", str(site.findAll('div', {"class":"releaseyear"})[1]))[0]
                except:
                    year = None
                
                try:
                    duration = re.search(r'[0-9]+', str(site.find('p', {'class': 'text-link text-footer'}))).group(0)
                except:
                    duration = None

                try:
                    genre_section = site.find('div', {'class': 'text-sluglist capitalize'})
                    genre = [x.text for x in genre_section.find_all('a')]
                except:
                    genre = []

                try:
                    lang = site.select_one('a[href^="/films/language"]').text.strip()
                except:
                    lang = None

                try:
                    members = re.findall(r'title="([0-9,]+)',str(site2.findAll("li", {"class":"js-route-watches"})[0]))[0]
                except:
                    members = None
                
                try:
                    fans = re.findall(r'title="([0-9,]+)',str(site2.findAll("li", {"class":"js-route-fans"})[0]))[0]
                except:
                    fans = None

                try:
                    likes = re.findall(r'title="([0-9,]+)',str(site2.findAll("li", {"class":"js-route-likes"})[0]))[0]
                except:
                    likes = None

                try:
                    lists = re.findall(r'title="([0-9,]+)',str(site2.findAll("li", {"class":"js-route-lists"})[0]))[0]
                except:
                    lists = None

                try:
                    reviews = re.findall(r'title="([0-9,]+)',str(site2.findAll("li", {"class":"js-route-reviews"})[0]))[0]
                except:
                    reviews = None

                return film_id, avr_rating, year, duration, genre, lang, members, fans, likes, lists, reviews

            except RequestException:
                return film_id, None, None, None, None, None, None, None, None, None, None


        # Run the function in parallel
        with ThreadPoolExecutor(max_workers=15) as executor:
            results = list(tqdm(executor.map(fetch_data, self.movie_dataframe().values), total=len(self.movie_dataframe())))

        # Process results into DataFrame
        columns = ['Name', 'Avr_Rating', 'Year', 'Duration', 'Genre', 'Language', 'Members', 'Fans', 'Likes', 'Lists', 'Reviews']
        return pd.DataFrame(results, columns=columns)

if __name__ == "__main__":

    user = "gabrielcooutin"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    scraper = LetterboxdScraper(user=user, headers=headers)
    scraper.scrape_all_pages()
    df = scraper.extract_movie_data()
    print(df)
    
    # df.to_csv(f"data/{user}_data.csv", index=False)  
