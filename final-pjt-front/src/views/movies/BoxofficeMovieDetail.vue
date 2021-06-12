<template>
  <div class="font-neodgm">
    <div class="container mt-4 d-flex flex-column px-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
        <p style="color: white" class="text-start ps-2">상세 보기</p>
        <span><img src="@/assets/find.png" width="30px"></span>
      </div>
      <div>
        <div class="d-flex px-3 mb-3">
          <img :src="imgUrl" height="300px" width="200px">
          <div class="d-flex flex-column align-items-center ms-3">
            <h1 style="color: black;"> {{ movie.movie_title }}</h1>
            <div class="m-3" id="overview">
              <!-- <h4 style="color:black">줄거리</h4> -->
              <!-- <p>{{ movie.overview }}</p> -->
            </div>
            <!-- <p>개봉일 : {{ movie.release_date }}</p>
            <p>사이트 평점: {{ movie.vote_average }}</p> -->
          </div>
        </div>
      </div>
    </div> 
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name:'BoxofficeMoveDetail',
  data(){
    return {
      movie :{},
    }
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/boxoffice/'+this.$route.params.movieid,
      method:'get',
    })
      .then(res=>{
        // console.log(res.data.movie, '여긴 created')
        this.movie = res.data.movie
        // this.movie = res.data.movie
      })
      .catch(err => {
        console.log(err)
      })
  },
  methods:{
    getMovie(){
      axios({
        url:'http://127.0.0.1:8000/memovies/movies/boxoffice/'+this.$route.params.movieid,
        method:'get',
      })
        .then(res=>{
          console.log(res.data, '여긴 getMovie!')
        })
        .cathc(err=>{
          console.log(err)
        })
    },
  },
  computed:{
    imgUrl(){
      // console.log(this.movie.poster_path, '여긴 computed!')
      return this.movie.poster_path
    },
  }
}
</script>
<style>
  .likeStatus {
    color: palevioletred;
  }
  #bigbox {
    background-color: lightgrey;
    border: 3px solid black;
  }

  #topbar{
    background-color:navy;
    height:30px
  }

  .font{
    font-family: 'Noto Sans KR', sans-serif;
  }

  #comment{
    background-color:lightgrey;
    border: 3px solid black;
    color:black;
  }

  /* #overview {
    width:90%;
    padding-left:13%;
  } */
</style>