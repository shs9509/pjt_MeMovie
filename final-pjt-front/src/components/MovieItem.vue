<template>
  <div class="col-3 font-neodgm d-flex flex-column" @click="getMovieDetail(movie.id)">
      <img :src="poster_path" alt="movie_poster" style="width:200px; height:300px;">
      <h5 class="mt-2 text-center me-5" style="padding-right:20px;">{{movie.movie_title}}</h5>
  </div>
</template>

<script>
export default {
  name:'movieItem',
  props:{
    movie:{
      type:Object,
    }
  },
  computed:{
    poster_path(){
      // if (this.movie.models === 'movies.tmdbmovie'){
      const tmdb_url = 'https://image.tmdb.org/t/p/w500/'
      // }
      return (tmdb_url + this.movie.poster_path)
    }
  },
  methods:{
    getMovieDetail(movieid){
      this.$router.push({ name:'MovieDetail' ,params:{movieid:movieid}})
    },
  },
}
</script>

<style>
  .imgSize{
    width:300px;
    height:400px;
  }

</style>