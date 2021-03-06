# RecSys Challenge 2018 - Team: DataHolics

*"This year’s challenge focuses on music recommendation, specifically the challenge of automatic playlist continuation.
By suggesting appropriate songs to add to a playlist, a Recommender System can increase user engagement by making
playlist creation easier, as well as extending listening beyond the end of existing playlists."*

You can find more about the challenge [here](http://www.recsyschallenge.com/2018/).

## Como contribuir?

Você pode contribuir da forma que achar melhor, é **muitíssimo recomendado para a organização do projeto**
que seguintes passos:

1. Cheque o [backlog](https://docs.google.com/spreadsheets/d/1sWLoWOEsVdKcs909zruygCF536TNPqjvdw7sDaf3q1s/edit?usp=sharing) do projeto e as demais tabelas que tem titúlo relacionado com a sua task.  
    
    1.1. Caso uma task similar a sua já exista e não tenha dono: coloque na planilha que você é o responsável pela task.
    
    1.2. Caso uma task similar a sua já exista e tenha dono: coloque na planilha que você também é responsável pela task e
    sincronize com os demais responsáveis (**é possível que já exista um canal no slack para discutir essa task**).
  
    1.3. Se uma task similar não existir crie no backlog, adicione que você é responsável e seja feliz :smile:!

2.  Ao implementar sua task lembre: é importante que os demais integrantes do grupo **entendam e possam reexecutar** seu código :heart: :heart: :heart: :heart: :heart: :heart: !

    2.1. Adicione um README contendo: O que faz o código? Como rodar? Algo mais que os demais deveriam saber?
  
    2.2. Tente manter o código comentado, uma boa prática é um comentário no topo de cada arquivo explicando para que
         esse arquivo serve.
  
    2.3. Mantenha contato com as pessoas relacionadas com sua task!

3. A cada reunião iremos atualizar o backlog e o que foi feito a cada semana. Por isso é importante que vá as reuniões
ou repasse a alguém que poderá ir o que você fez e as dificuldades que encontrou.

> Dúvidas? **Use o Slack!** Esse é nosso canal de comunicação oficial.

### Quer contribuir, mas não sabe muito bem com o que pode ajudar?

Uma ajuda muito útil é analisar e descrever os dados! Há várias tasks disponíveis [neste link](https://docs.google.com/spreadsheets/d/1sWLoWOEsVdKcs909zruygCF536TNPqjvdw7sDaf3q1s/edit?usp=sharing). (Se for implementar alguma das tasks siga o procedimento explicado acima)

## The Task

As part of this challenge, Spotify will be releasing a public dataset of playlists,
consisting of a large number of playlist titles and associated track listings.
The evaluation set will contain a set of playlists from which a number of tracks have been withheld.
The task will be to predict the missing tracks in those playlists.

## The Dataset

### Original dataset 
It can be found [here](https://recsys-challenge.spotify.com/details).

### Our processed dataset
Three files (tracks_unique.csv, playlist.csv and play_track.csv)
Can be found here [here](https://drive.google.com/drive/folders/1l1i6VuDQ-e6HTm2TK-fFYT60XzECodgd)

You can also process the original dataset by yourself by running

* src/scripts/**to_csv.py**
* src/scripts/**csv_unique.sh**

### About the dataset

You can find our data analysis at [eda_reports/](eda_reports/), below is the official data summary:
```
number of playlists 1000000
number of tracks 66346428
number of unique tracks 2262292
number of unique albums 734684
number of unique artists 295860
number of unique titles 92944
number of playlists with descriptions 18760
number of unique normalized titles 17381
avg playlist length 66.346428
top playlist titles
  10000 country
  10000 chill
   8493 rap
   8481 workout
   8146 oldies
   8015 christmas
   6848 rock
   6157 party
   5883 throwback
   5063 jams
   5052 worship
   4907 summer
   4677 feels
   4612 new
   4186 disney
   4124 lit
   4030 throwbacks
   3886 music
   3513 sleep
   3500 vibes
top tracks
  46574 HUMBLE. by Kendrick Lamar
  43447 One Dance by Drake
  41309 Broccoli (feat. Lil Yachty) by DRAM
  41079 Closer by The Chainsmokers
  39987 Congratulations by Post Malone
  35202 Caroline by Aminé
  35138 iSpy (feat. Lil Yachty) by KYLE
  34999 Bad and Boujee (feat. Lil Uzi Vert) by Migos
  34990 Location by Khalid
  34922 XO TOUR Llif3 by Lil Uzi Vert
  33699 Bounce Back by Big Sean
  32391 Ignition - Remix by R. Kelly
  32336 No Role Modelz by J. Cole
  32059 Mask Off by Future
  31492 No Problem (feat. Lil Wayne & 2 Chainz) by Chance The Rapper
  31374 I'm the One by DJ Khaled
  31119 Jumpman by Drake
  31106 goosebumps by Travis Scott
  30678 Fake Love by Drake
  30485 Despacito - Remix by Luis Fonsi
top artists
 847160 Drake
 413297 Kanye West
 353624 Kendrick Lamar
 339570 Rihanna
 316603 The Weeknd
 294667 Eminem
 272116 Ed Sheeran
 250734 Future
 243119 Justin Bieber
 241560 J. Cole
 230857 Beyoncé
 223509 The Chainsmokers
 212772 Chris Brown
 203047 Calvin Harris
 198905 Twenty One Pilots
 197855 Lil Uzi Vert
 195907 Post Malone
 192478 Big Sean
 187029 Maroon 5
 185520 JAY Z
numedits histogram
  92252 2
  81820 3
  71973 4
  61978 5
  53085 6
  46860 7
  41210 8
  36629 9
  32810 10
  29907 11
  26947 12
  24941 13
  22800 14
  20834 15
  19000 16
  17817 17
  16551 18
  15305 19
  14217 20
  13486 21
last modified histogram
  19018 2017-10-30
  15495 2017-10-29
  11640 2017-10-26
  11083 2017-10-28
   9994 2017-10-27
   9727 2017-10-25
   9142 2017-10-24
   8588 2017-10-23
   7953 2017-10-22
   6980 2017-10-19
   6407 2017-10-21
   5986 2017-10-18
   5979 2017-10-20
   5792 2017-10-17
   5653 2017-10-16
   5375 2017-10-15
   4840 2017-10-12
   4483 2017-10-14
   4460 2017-10-11
   4431 2017-10-13
playlist length histogram
  15057 20
  14177 15
  13876 21
  13856 16
  13685 17
  13629 18
  13602 22
  13531 19
  13250 24
  13149 23
  13077 30
  13043 14
  13031 25
  12834 26
  12513 28
  12502 27
  12332 29
  12318 13
  12016 12
  11882 31
num followers histogram
 754219 1
 149600 2
  46939 3
  19591 4
   9813 5
   5360 6
   3305 7
   2143 8
   1512 9
   1006 10
    825 11
    632 12
    479 13
    359 14
    328 15
    290 16
    235 17
    207 18
    162 19
    138 20
```
