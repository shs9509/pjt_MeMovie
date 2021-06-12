<template>
  <div>
    <div class="my-3">
      <h1 class="retro">메인 페이지</h1>
    </div>
    <ul class="row">
      <MovieItem v-for="movie in movieList.tmdb" :key="movie.movie_title" :movie="movie" @click="getMovieDetail(movie.id)"/><hr>
      <NaverMovieItem v-for="movie in movieList.naver" :key="movie.movie_title" :movie="movie" @click="getMovieDetail(movie.id)"/><hr>
      <BoxofficeMovieItem v-for="movie in movieList.boxoffice" :key="movie.movie_title" :movie="movie" @click="getMovieDetail(movie.id)"/>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import MovieItem from '@/components/MovieItem'
import NaverMovieItem from '@/components/NaverMovieItem'
import BoxofficeMovieItem from '@/components/BoxofficeMovieItem'
import VueSlickCarousel from 'vue-slick-carousel'

export default {
  name:'Home',
  components:{
    MovieItem,
    NaverMovieItem,
    BoxofficeMovieItem,
  },
  data(){
    return {
      movieList:{},
    }
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/',
      method:'get',
    })
      .then(res=>{
        this.movieList = res.data
        console.log(typeof(res.data))
        console.log(res.data.tmdb)
      })
      .catch(err=>{
        console.log(err)
      })
  },
}
</script>

<style>

</style>