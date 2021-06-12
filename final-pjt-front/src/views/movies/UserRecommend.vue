<template>
  <div class="font-neodgm">
    <div class="container mt-5 p-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">나만의 추천 영화</p>
      <span><img src="@/assets/profile.png" width="20px" class="ms-2"></span>
      </div>
      <h2 style="text-align:center; color:black;">{{username}}님을 위한 추천 영화</h2>
      <div>
        <hr>
        <h3 v-if="!movieList" style="text-align:center; color:black;">
          평점을 입력하신 영화가 없습니다.
        </h3>
        <div v-else class="row ms-5">
          <MovieItem v-for="movie in movieList" :key="movie.movie_title" :movie="movie" @click="getMovieDetail(movie.id)"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode"
import axios from 'axios'
import MovieItem from '@/components/MovieItem'
export default {
  name:'UserRecommend',
  data(){
    return {
      movieList:[],
      userid:'',
      username:'',
    }
  },
  components:{
    MovieItem,
  },
  props:{
    isLogin:{
      type:Boolean
    }
  },
  created(){
    const token = localStorage.getItem('jwt')
    this.userid= jwt_decode(token).user_id
    this.username= jwt_decode(token).username
    // console.log(this.userid)
    // console.log(token)
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/'+this.userid+'/recommend/',
      method:'get',
      headers:{
          Authorization: `JWT ${localStorage.getItem('jwt')}`
      },
    })
      .then(res=>{
        console.log(res.data.movies)
        this.movieList = res.data.movies
        // console.log(res.data, '새로받아오는 데이터!')
        // res.data.forEach(element => {
        //   console.log(element, '여기에 담긴것은 요소여! movie와 같응게')
        //   console.log(element.pk, '여기에 담긴것은 요소여! movie.pk와 같응게')
        //   console.log(element.fields, '여기에 담긴것은 요소여! fields와 같응게')
        // })
      })
      .catch(err=>{
        // console.log(this.$route.params.userid)
        console.log(err)

      })
  },
}
</script>

<style>
  #bigbox {
    background-color: lightgrey;
    border: 3px solid black;
  }
  #topbar{
    background-color:navy;
    height:30px
  }

</style>