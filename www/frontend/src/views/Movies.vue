<template>

  <!-- MAIN CONTENT -->
  <div class="main-content">
    <div class="container-fluid">

      <div class="panel-heading">
        <h3 class="panel-title sale-title">UniMovies-统一电影聚合平台！</h3>
      </div>

      <div class="type-search">
        <ul>
          <li id="type-year"><strong>按年代：</strong>
            <a v-for="year in years" @click="typeYear(year.value)">{{ year.label }}</a>
          </li>
          <li id="type-rate"><strong>按评分：</strong>
            <a v-for="rate in rates" @click="typeRate(rate.value)">{{ rate.label }}</a>
          </li>
          <li id="type-zimu"><strong>按字母：</strong>
            <a v-for="zimu in zimus" @click="typeZimu(zimu.value)">{{ zimu.label }}</a>
          </li>
        </ul>
      </div>

      <div class="row">
        <!--电影列表-->
        <div v-for="movie in movies" class="col-md-2 posi movie-item">
          <div class="thumbnail img">
            <a @click="toDetail(movie.id)" href="#">
              <img :src="movie.cover">
            </a>
          </div>

          <div class="content">
            <a @click="toDetail(movie.id)" href="#">《{{ movie.title }}》</a>
            <div class="info">
              <span v-if="movie.douban" class="douban">豆瓣</span>
              <span v-if="movie.maoyan" class="maoyan">猫眼</span>
            </div>
          </div>
        </div>
        <!--电影列表End-->
      </div>

    </div>
  </div>
  <!-- END MAIN CONTENT -->

</template>

<script>
  export default {
    name: "Movies",
    data() {
      return {
        movies: [],
        key: '',
        years: [
          {label: '全部', value: 0},
          {label: '2019', value: 2019},
          {label: '2018', value: 2018},
          {label: '2017', value: 2017},
          {label: '2016', value: 2016},
          {label: '2015', value: 2015},
          {label: '2014', value: 2014},
          {label: '2013', value: 2013},
          {label: '2012', value: 2012},
          {label: '2011', value: 2011},
          {label: '2010', value: 2010},
          {label: '2009', value: 2009},
          {label: '2008', value: 2008},
          {label: '2007', value: 2007},
          {label: '2006', value: 2006},
          {label: '2005', value: 2005},
          {label: '2004', value: 2004},
          {label: '2003', value: 2003},
          {label: '2002', value: 2002},
          {label: '2001', value: 2001},
          {label: '2000', value: 2000}
        ],
        rates: [
          {label: '9分以上', value: 9},
          {label: '8分以上', value: 8},
          {label: '7分以上', value: 7},
          {label: '6分以上', value: 6},
          {label: '5分以上', value: 5}
        ],
        zimus: []
      }
    },
    methods: {
      toDetail(id) {
        window.location.href = '/movie/' + id;
      },
      toSearch() {
        window.location.href = '/search/' + this.key;
      },
      addToCart(id) {
        let vm = this;

        this.$http.post(api.cart.addNew + id)
          .then(resp => {
            let result = resp.body;
            if (result.success) {
              BootstrapDialog.alert("添加成功！")
            } else {
              console.log(resp);
            }
          })
      },
      fetchMovies(page) {
        let vm = this;

        this.$http.get(api.movie.listMovies + page)
          .then(resp => {
            let result = resp.body;

            if (result.success) {
              vm.movies = result.data;
            } else {
              console.log(resp);
            }
          })
      }
    },
    created() {

      this.fetchMovies(1);
    },
    mounted() {
      this.movies = [
        {
          id: 1,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: false
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '/assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 3,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: false,
          maoyan: false
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        },
        {
          id: 2,
          title: '西西里的美丽传说',
          cover: '../assets/img/xxl.jpg',
          description: '当我还只是十三岁时，1941年春末的那一天，我初次见到了她那一天，墨索里尼向英法宣战，而我，得到了生命里的第一辆脚踏车',
          douban: true,
          maoyan: true
        }
      ];

      $(function () {
        function equal_cols(el) {
          let h = 0;
          $(el).each(function () {
            $(this).css({'height': 'auto'});
            if ($(this).outerHeight() > h) {
              h = $(this).outerHeight();
            }
          });
          $(el).each(function () {
            $(this).css({'height': h});
          });
        }

        equal_cols('.posi');
      });
    }
  }
</script>

<style scoped>

</style>
