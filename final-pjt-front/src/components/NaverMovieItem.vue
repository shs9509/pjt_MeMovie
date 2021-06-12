<template>
  <div class="col-2 font-neodgm d-flex flex-column" @click="getMovieDetail(movie.id)">
      <img :src="poster_path" alt="movie_poster" style="width:150px; height:100px;">
      <h5 class="mt-2 text-center me-5" style="padding-right:20px;">{{movie.movie_title}}</h5>
  </div>
</template>

<script>
export default {
  name:'NaverMovieItem',
  props:{
    movie:{
      type:Object,
    }
  },
  computed:{
    poster_path(){
      return this.movie.poster_path
    }
  },
  methods:{
    getMovieDetail(movieid){
      this.$router.push({ name:'NaverMovieDetail' ,params:{movieid:movieid}})
    },
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR&display=swap');
@import url('//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css');
<link rel="stylesheet" href="//cdn.jsdelivr.net/gh/Dalgona/neodgm-webfont@1.521/neodgm/style.css">

.font-neodgm { 
  font-family: 'NeoDunggeunmo'; 
}
</style>