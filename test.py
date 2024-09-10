import requests

url = "https://api.themoviedb.org/3/search/movie?query='Bahubali'"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYjExNTkwNGQxNzFmNTUyYTM1ZDcyY2VmYWNlMjk0OCIsIm5iZiI6MTcyNTk3ODI4NS4xNzE3NDYsInN1YiI6IjY2ZGZkOWFlMDAwMDAwMDAwMGE0Njk2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.o4PCjZY6YFtTYDkB47iLBPbsQPbRP9iHYaXz8e0OQhw"
}

response = requests.get(url, headers=headers)

print(response.text)