<template>
  <router-link to="/" v-bind="$attrs">
    <img src="@/assets/logos/Logo_bg.png" alt="Logo OptiTAB" class="logo logo-full" />
    <img src="/favicon.png" alt="OptiTAB" class="logo logo-icon" />
  </router-link>
</template>

<script>
export default {
  name: 'Logo',
  inheritAttrs: false,
}
</script>

<style scoped>
.logo {
  height: auto;
  object-fit: contain;
}

.logo-full {
  width: 100px;
  min-width: 100px;
  max-width: 100px;
  margin-left: 0px;
  margin-top: 2px;
}

.logo-icon {
  display: none;
  width: 36px;
  height: 36px;
  min-width: 36px;
}

@media (max-width: 880px) {
  .logo-full {
    display: none;
  }
  .logo-icon {
    display: block;
  }
}
</style>
