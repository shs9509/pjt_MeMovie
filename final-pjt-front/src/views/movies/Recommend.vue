<template>
  <div class="font-neodgm container">
    <div class="container mt-4 p-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">1년전 오늘 박스오피스</p>
      <span><img src="@/assets/movie.png" width="30px" class="ms-1"></span>
      </div>
      <div class="row">
        <BoxOfficeItem v-for="movie in boxOffice_OneYears" :key="movie.id" :movie="movie"/>
      </div>
    </div>
    <div class="container mt-4 p-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">3년전 오늘 박스오피스</p>
      <span><img src="@/assets/movie.png" width="30px" class="ms-1"></span>
      </div>
      <div class="row">
        <BoxOfficeItem v-for="movie in boxOffice_ThreeYears" :key="movie.id" :movie="movie"/>
      </div>
    </div>
    <div class="container mt-4 p-0" id="bigbox">
      <div id="topbar" class="mb-3 mx-0 d-flex">
      <p style="color: white" class="text-start ps-2">5년전 오늘 박스오피스</p>
      <span><img src="@/assets/movie.png" width="30px" class="ms-1"></span>
      </div>
      <div class="row">
        <BoxOfficeItem v-for="movie in boxOffice_FiveYears" :key="movie.id" :movie="movie"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import BoxOfficeItem from '@/components/BoxOfficeItem'
export default {
  name:'Recommend',
  data(){
    return {
      movieList:[],
    }
  },
  components:{
    BoxOfficeItem,
  },
  created(){
    axios({
      url:'http://127.0.0.1:8000/memovies/movies/recommend/',
      method:'get',
    })
      .then(res=>{
        this.movieList = res.data
        // console.log(res.data)
      })
      .catch(err=>{
        console.log(err)
      })
  },
  computed: {
    boxOffice_OneYears: function () {
      return this.movieList.slice(0, 10)
    },
    boxOffice_ThreeYears: function () {
      return this.movieList.slice(10, 20)
    },
    boxOffice_FiveYears: function () {
      return this.movieList.slice(20, 30)
    },
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