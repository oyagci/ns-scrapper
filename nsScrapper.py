import requests
from lxml import html
from bs4 import BeautifulSoup
import os

def main():

    # Fill those fields
    email = ""
    password = ""

    if email == "" or password == "":
        print("")
        print(" +---------------------------------------+")
        print(" | Please fill email and password first! |")
        print(" +---------------------------------------+")
        print("")
        exit()

    login_url = "https://sso.teachable.com/secure/7615/users/sign_in?clean_login=true&reset_purchase_session=1"
    session_requests = requests.session()
    result = session_requests.get(login_url)
    tree = html.fromstring(result.text)

    csrf_token = list(set(tree.xpath("/html/head/meta[@name='csrf-token']/@content")))[0]
    authenticity_token = list(set(tree.xpath("/html/body/div/div/div/div/div/div/div/div/form/input[@name='authenticity_token']/@value")))[0]

    payload = {
            'authenticity_token': authenticity_token,
            'user[school_id]': '7615',
            'user[email]': email,
            'user[password]': password,
    }

    result = session_requests.post(
                login_url,
                headers = {
                    'Referer': login_url
                },
                data = payload
            )
    url = 'http://courses.nihongoshark.com/courses/147895/lectures/2224887'
    result = session_requests.get(
                url,
                data=payload,
                headers = dict(referer = url)
            )

    soup = BeautifulSoup(result.text, "html.parser")
    links_a = soup.find_all(class_="allNDLCourseImgs")[0].find_all("a")
    links = []

    for link in links_a:
        links.append(link['href'])

    for link in links:
        result = session_requests.get(link)

        soup = BeautifulSoup(result.text, "html.parser")
        html_links = soup.find_all("link")
        
        for link in html_links:
            if 'stylesheet' in link['rel']:
                link['href'] = 'https:' + link['href']
                break

        html_link = soup.find_all('a', class_='item')
        prefix = 'http://courses.nihongoshark.com'

        for a in html_link:

            result = session_requests.get(prefix + a['href'])
            soup = BeautifulSoup(result.text, "html.parser")
            html_links = soup.find_all("link")
            
            for link in html_links:
                if 'stylesheet' in link['rel']:
                    link['href'] = 'https:' + link['href']
                    break

            data = soup.prettify()
            title = soup.find_all("title")[0].text
            title = title.replace("/", "-")
            print(title)
            file = open(os.path.normpath(title) + ".html", 'w')
            file.write(data)
            file.close()

    url = "http://courses.nihongoshark.com/courses/147895/lectures/2224887"

    result = session_requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    array = soup.find_all("tr")
    eepurls = []
    for cell in array:
        a = cell.find_all("a")[0]
        eepurls.append(a['href'])

    for eepurl in eepurls:
        result = session_requests.get(eepurl)
        soup = BeautifulSoup(result.text, "html.parser")
        title = soup.find_all("title")[0].text
        title = title.replace("/", "-")
        print(os.path.normpath(title))
        file = open(os.path.normpath(title + ".html"), 'w')
        file.write(soup.prettify())
        file.close()
        

if __name__ == '__main__':
    main()
