<template>

  <!-- WRAPPER -->
  <div id="wrapper">

    <!-- NAVBAR -->
    <nav class="navbar navbar-default navbar-top nav-custom">
      <div class="brand">
        <a href="/index"><img src="./assets/img/unimovies.png" width="150" alt="UniMovies Logo"
                              class="img-responsive logo"></a>
      </div>
      <div class="container-fluid">
        <form class="navbar-form navbar-left">
          <div class="input-group">
            <input v-model="key" type="text" value="" class="form-control" placeholder="电影名称 ...">
            <span @click="toSearch" class="input-group-btn"><button type="button"
                                                                    class="btn btn-primary">搜索</button></span>
          </div>
        </form>
        <div id="navbar-menu">
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown"><img src="./assets/img/user.png" class="img-circle"
                                                                              alt="Avatar">
                <!--                            <span>{{ username }}</span> -->
                <span>用户</span>
                <i class="icon-submenu lnr lnr-chevron-down"></i>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/order"><i class="lnr lnr-cog"></i> <span>我的订单</span></a></li>
                <li><a href="/api/account/logout"><i class="lnr lnr-exit"></i> <span>退出</span></a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- END NAVBAR -->

    <!-- MAIN -->
    <div class="main">
      <!-- MAIN CONTENT -->
      <router-view/>
      <!-- END MAIN CONTENT -->
    </div>
    <!-- END MAIN -->

    <div class="clearfix"></div>
    <footer>
      <div class="container-fluid">

      </div>
    </footer>

  </div>
  <!-- END WRAPPER -->

</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  @import "./assets/vendor/bootstrap/css/bootstrap.min.css";
  @import "./assets/vendor/bootstrap-dialog/css/bootstrap-dialog.min.css";
  @import "./assets/vendor/font-awesome/css/font-awesome.min.css";

  @import "./assets/css/main.css";
  @import "./assets/css/common.css";

</style>
