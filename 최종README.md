# 영화 페이지 설계 프로젝트

### 주제 - "그때 그 영화" 

: 레트로 디자인의 웹사이트를 구성하고, 그에 맞게 n년전의 박스오피스 순위를 나열해서 그 영화들을 추천하는 기능을 갖춘다.



### 페이지 설계

- 메인 페이지
  - 기존 영화들 나열
  - 영화에 좋아요 기능
- 영화 상세 페이지
  - 영화에 대한 댓글 기능
  - 코멘트와 더불어 평점 매기기 가능
  - 영화의 상세페이지에는 유투브 리뷰의 영상이 표시된다.
- 게시판
  - 영화에 따른 리뷰글 생성 가능
  - 리뷰글에 코멘트 생성가능
- 추천 페이지 
  - 영화 추천으로서 박스오피스 API를 조회해서 n년전 영화 순위를 나열해 추천한다.
- 회원가입
  - 아이디, 비밀번호 뿐만아니라 age, MBTI를 입력해서 추가적인 추천기능에 반영할 수 있게 한다.
- 프로필
  - 프로필에는 로그인한 사용자의 댓글과 좋아요한 영화, 영화의 리뷰를 확인할 수 있다.



### 역할 -백엔드

5/20 

- 모델 ERD 설계
- 게시판 구현 - 리뷰 CRUD, 리뷰의 댓글 CRUD 구현

5/21

- 박스오피스 API DB에 넣어서 프론트에 넘겨주기
- 박스오피스 API를 통해서 추천페이지 구현
- 영화의 댓글기능 (구현 중)



# 5/20

- 모델 ERD 설계

- 게시판의 구현 - 리뷰생성 + 리뷰의 댓글 생성

-----------

### ERD

- ERD 다이어그램 툴 : Draw.io  사용

![image-20210521211516426](최종README.assets/image-20210521211516426.png)



### Community

- 커뮤니티-리뷰생성

![image-20210520173840191](최종README.assets/image-20210520173840191.png)



- 커뮤니티-리뷰리스트

![image-20210520173909679](최종README.assets/image-20210520173909679.png)



- 커뮤니티-리뷰디테일

![image-20210520173928977](최종README.assets/image-20210520173928977.png)



- 커뮤니티-리뷰- 댓글생성

![image-20210520174959373](최종README.assets/image-20210520174959373.png)



- 커뮤니티-리뷰- 댓글확인

![image-20210520175012495](최종README.assets/image-20210520175012495.png)



# 5/21

- 박스오피스 API DB에 넣어서 프론트에 넘겨주기
- 박스오피스 API를 통해서 추천페이지 구현
- 영화의 댓글기능 (구현 중)

------

### Box office API

박스오피스 API 를 불러와서 장고에서 데이터를 가공하고 프론트에 넘겨주는게 계획이었다.

api는 쉽게 구할수있었다.

https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do

- 과정 

  0. 나는 프론트에게 1년치 박스오피스 데이터를 줘야한다. 그런데 데이터는 일별 박스오피스이다.

     `for`문을 돌려서 20200521 ~ 20210521 를 순차적으로 나타내야하는데

     이때 `datetime`을  이용해서 31일에서 1일로 가는 날짜의 진행을 잘 넘길수있었다.

  ```python
  today = datetime.now()
      start_day = today + timedelta(days=-(365*5)) # 5년전부터 시작
      for count in range(10): # ex)10일
          start_day = start_day + timedelta(days=1) # 다음날의 박스오피스
          day= str(start_day)[0:10].replace("-","")
         
  ```

  

  1. 박스 오피스 API를 가져온다

  ```python
  box_office = 		requests.get(f'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={day}')
  # REST 방식 API 요청
  
  box_office = box_office.json()['boxOfficeResult']
  # 받은 API를 json화
  ```

  2. API에서 영화들의 필요한 요소만을 모델에 넣는다.

  ```python
  now_show_range = box_office.get('showRange')[:8]
          for movie in box_office['dailyBoxOfficeList']:
            	cnt+=1
              new_movie = BoxofficeMovie(
                      pk = cnt,
                      movie_title=movie.get('movieNm'),
                      show_range =now_show_range,
                      rank=movie.get('rank'),
                  )
              new_movie.save()
      movies = BoxofficeMovie.objects.all()
  ```

  3. 시리얼라이저화 시켜주고 프론트에 넘긴다.

  ```python
  BoxOffice = serializers.serialize('json', movies)
  return HttpResponse(BoxOffice, content_type='application/json')
  ```

  

일단 배운 방식으로 진행을 하였는데  데이터를 받아오는데 상당한(?아마?) 시간이 걸린다.

의문을 가지고 내가 한 방식을 스택오버플로우에 올렸는데 

돌아오는 답변은 지금 한방식은 구식적인 방식이고 현대적인 방식으로 DRF 사이트를 넘겨줬다.

:grey_question::grey_question::grey_question::grey_question::grey_question::grey_question::grey_question:

아마 DRF 를 좀더 살펴보면 API를 다루는 방식이 있는듯하다.



- 메인 페이지 - 박스오피스 1~10위 까지의 데이터

![메인페이지-boxoffice](최종README.assets/메인페이지-boxoffice-1621698580192.png)



### Recommend 

이미 박스오피스 API를 불러오는 방법과 `datetime`을 다룰줄 알기 때문에

n년전 박스오피스를 넘기는것은 쉬웠다.



- 추천알고리즘 - 현재시간으로 부터 n년전의 박스오피스 1~10위

![추천알고리즘](최종README.assets/추천알고리즘.png)



# 5/22

- 영화 댓글 기능 구현
- 좋아요 기능 (진행중)

---------



- 영화 - 댓글 생성

  ![image-20210523004908989](최종README.assets/image-20210523004908989.png)

- 영화 - 댓글 리스트

  ![image-20210523004846111](최종README.assets/image-20210523004846111.png)

- 영화 -댓글 디테일

![image-20210523004807000](최종README.assets/image-20210523004807000-1621698589924.png)





# 5/23

- 영화 좋아요 기능 구현
- 영화 유저별 추천 페이지 구현
- 데이터 로드 속도 개선
- Vue 유저별 추천페이지 구현 (진행중)

----------









------------

### 느낀점

5/20

- 프로젝트의 컨셉과 추가기능을 애기하면서 웹사이트의 모습이 구체화되는걸 보면 재미있었다.  

- 본격적으로 깃헙을 통한 협업을 통해서 진행했는데 후에 팀프로젝트나, 현업에서 도움될만한 경험일것이다.

- ERD 생성을 하면서 확신이 안들때도 있어서 미숙한걸 느꼈지만 이는 실제로 구현을 진행하면서 고쳐나가도록 한다.

5/21

- API를 다루는 과정에서 아는게 많지 않아 처음부터 막막했으나, 검색과 민철이 형의 도움으로 박스오피스의  API를 프론트로 무사히 넘겨 줄수있었다.  :dancing_women: 갓민철! 갓민철! 갓민철! :dancing_men:
- 한번 API를 넘겨줘보니 추천알고리즘은 어렵지않았다.
- 한100개의 영화데이터를 넘겨주고 프론트에서 이를 끌어오는데 상당한 시간이 걸린다. 이부분을 최소화 해야한다. 

5/22

- 영화 댓글기능은 리뷰게시판 구현하듯 무난하게 구현하였다. :happy:

- 중간에 댓글기능에 대해서 나현이가 영화의 상세페이지와 함계 댓글도 보내달라고 했었는데 

  메인페이지에 있는 영화들을 각가의 댓글을 달라는것인줄 알고 구현못하고 동동거렸다. 

  그런데 제대로 요구하는 걸 이해했으면 충분히 할수있었다.  아쉽...:cry: 

- 요구하는 것을 정확히 세세하게 파악하고 요구해야 된다는걸 느꼈다. 또한 보이스톡 없이 진행하다보니 소통의 어려움을 많이 느꼈다. 오프라인 하고싶다.....:sob:

- 좋아요 기능 구현하는데 왜안될까?? 

  - 일단 포스트맨에서 성환형한테 로그인한채로 진행하는걸 배웠는데 왜 안될까...
  - username, user.id , user_id , pk 뭐를 받아야되는걸까 머리가 아찔하다. :weary: